#!/usr/bin/env python3
"""
Copy the paintings from the old Squarespace site into this project.

Run it from the project folder, on a computer with normal internet access:

    python3 tools/import_squarespace.py --dry-run   # only list what it finds
    python3 tools/import_squarespace.py             # download everything

What it does:
  1. Opens https://www.lassetopbjerg.com/portfolio and finds the year links
     (2015, 2016, ... 2023-2024).
  2. Opens each year page and collects the images on it.
  3. Downloads each image twice from Squarespace's image server:
     a large copy  -> works/<year>/01.jpg
     a small copy  -> works/<year>/thumbs/01.jpg   (used in the grid)
  4. Writes works.js with one entry per painting. Titles, sizes and
     status are left empty for you (or Claude Code) to fill in.

It skips files that are already downloaded, so it is safe to run again.
Only uses Python's standard library.
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

BASE = "https://www.lassetopbjerg.com"
INDEX_PATH = "/portfolio"
UA = "Mozilla/5.0 (X11; Linux x86_64) site-export-script"
FULL_SIZE = "2500w"
THUMB_SIZE = "750w"

YEAR_RE = re.compile(r"^\s*((?:19|20)\d{2})(?:\s*[-–/]\s*((?:19|20)\d{2}))?\s*$")
IMG_RE = re.compile(r"https?:(?:\\?/){2}images\.squarespace-cdn\.com(?:\\?/)[^\s\"'<>)\\]*(?:\\/[^\s\"'<>)\\]*)*")
FILENAME_LIKE = re.compile(r"^(img|dsc|pxl|photo|image|screenshot)?[_\-\s]?\d+.*$|\.(jpe?g|png|heic|webp)$", re.I)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fetch(url, binary=False, tries=3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                return data if binary else data.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return None
            err = e
        except Exception as e:  # network hiccup
            err = e
        time.sleep(1.5 * (attempt + 1))
    print(f"  ! could not fetch {url}: {err}", file=sys.stderr)
    return None


class LinkParser(HTMLParser):
    """Collects (href, visible text) for every <a>."""

    def __init__(self):
        super().__init__()
        self.links, self._stack = [], []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._stack.append([dict(attrs).get("href", ""), ""])

    def handle_data(self, data):
        for item in self._stack:
            item[1] += data

    def handle_endtag(self, tag):
        if tag == "a" and self._stack:
            href, text = self._stack.pop()
            self.links.append((href, " ".join(text.split())))


def year_label(text):
    m = YEAR_RE.match(text or "")
    if not m:
        return None
    return m.group(1) + ("–" + m.group(2) if m.group(2) else "")


def find_year_pages(index_html, index_json):
    """Returns [(label, absolute url)] in page order, without duplicates."""
    found, seen = [], set()

    p = LinkParser()
    p.feed(index_html or "")
    for href, text in p.links:
        label = year_label(text)
        if label and href and not href.startswith(("mailto:", "tel:", "#")):
            url = urllib.parse.urljoin(BASE, href.split("?")[0])
            if url not in seen:
                seen.add(url)
                found.append((label, url))

    # Fallback: Squarespace's JSON view of the collection
    if not found and index_json:
        try:
            data = json.loads(index_json)
            for item in data.get("items", []):
                label = year_label(item.get("title", ""))
                if label and item.get("fullUrl"):
                    url = urllib.parse.urljoin(BASE, item["fullUrl"])
                    if url not in seen:
                        seen.add(url)
                        found.append((label, url))
        except ValueError:
            pass
    return found


def clean_img_url(u):
    u = html.unescape(u).replace("\\/", "/")
    u = u.split("?")[0].split("#")[0]
    if u.startswith("http://"):
        u = "https://" + u[len("http://"):]
    return u.rstrip("/")


def image_urls(*texts):
    out, seen = [], set()
    for t in texts:
        for m in IMG_RE.findall(t or ""):
            u = clean_img_url(m)
            # Skip the bare host and folder-only URLs
            if u.count("/") < 4 or u in seen:
                continue
            seen.add(u)
            out.append(u)
    return out


def titles_from_json(text):
    """Map image URL -> title, from Squarespace's ?format=json, when a real title is set."""
    titles = {}
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return titles

    def walk(o):
        if isinstance(o, dict):
            url = o.get("assetUrl") or o.get("imageUrl")
            title = (o.get("title") or "").strip()
            if url and title and not FILENAME_LIKE.search(title):
                titles[clean_img_url(url)] = title
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    return titles


def ext_of(url):
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
    return ext if ext in (".jpg", ".jpeg", ".png", ".webp", ".gif") else ".jpg"


def folder_name(label):
    return label.replace("–", "-")


def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return True
    data = fetch(url, binary=True)
    if not data:
        return False
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    return True


def js_string(s):
    return json.dumps(s, ensure_ascii=False)


def write_works_js(years, path):
    lines = [
        "// Imported from lassetopbjerg.com (Squarespace) by tools/import_squarespace.py.",
        "// Fill in title, medium, size and status for each painting. See the notes",
        "// at the top of works.js in the repo for what each field means.",
        "",
        "window.WORKS = [",
    ]
    years = sorted(years, key=lambda y: max(int(n) for n in re.findall(r"\d{4}", y[0])), reverse=True)
    for yi, (label, works) in enumerate(years):
        lines.append("  {")
        lines.append(f"    year: {js_string(label)},")
        lines.append("    works: [")
        for wi, w in enumerate(works):
            comma = "," if wi < len(works) - 1 else ""
            lines.append(
                f"      {{ file: {js_string(w['file'])}, title: {js_string(w.get('title', ''))}, titleEn: \"\", "
                f"medium: \"\", mediumEn: \"\", size: \"\", status: \"\" }}{comma}"
            )
        lines.append("    ]")
        lines.append("  }" + ("," if yi < len(years) - 1 else ""))
    lines.append("];")
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def works_js_is_empty(path):
    if not os.path.exists(path):
        return True
    with open(path, encoding="utf-8") as f:
        code = re.sub(r"//.*", "", f.read())
    return re.search(r"window\.WORKS\s*=\s*\[\s*\]", code) is not None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="only list what would be downloaded")
    args = ap.parse_args()

    print(f"Reading {BASE}{INDEX_PATH} ...")
    index_html = fetch(BASE + INDEX_PATH)
    if not index_html:
        sys.exit("Could not open the portfolio page. Is the Squarespace site still online?")
    index_json = fetch(BASE + INDEX_PATH + "?format=json")

    pages = find_year_pages(index_html, index_json)
    if not pages:
        sys.exit("Found no year links on the portfolio page. The page layout may have changed; "
                 "ask Claude Code to look at the HTML and adjust find_year_pages().")

    # Images that appear on the index page too (logo, social images) are not paintings.
    shared = set(image_urls(index_html, index_json))

    years = []
    for label, url in pages:
        page_html = fetch(url) or ""
        page_json = fetch(url + "?format=json") or ""
        urls = [u for u in image_urls(page_html, page_json) if u not in shared]
        titles = titles_from_json(page_json)
        print(f"  {label:<10} {len(urls):>3} images   {url}")
        works = []
        for i, u in enumerate(urls, 1):
            name = f"{i:02d}{ext_of(u)}"
            works.append({
                "src": u,
                "file": f"works/{folder_name(label)}/{name}",
                "thumb": f"works/{folder_name(label)}/thumbs/{name}",
                "title": titles.get(u, ""),
            })
        years.append((label, works))

    total = sum(len(w) for _, w in years)
    print(f"\n{len(years)} years, {total} images in total.")
    if args.dry_run:
        print("Dry run: nothing downloaded.")
        return

    failed = 0
    for label, works in years:
        for w in works:
            ok_full = download(f"{w['src']}?format={FULL_SIZE}", os.path.join(ROOT, w["file"]))
            ok_thumb = download(f"{w['src']}?format={THUMB_SIZE}", os.path.join(ROOT, w["thumb"]))
            if not ok_full:
                failed += 1
            print(f"  {'✓' if ok_full and ok_thumb else '!'} {w['file']}")

    # Keep a record of where every image came from
    with open(os.path.join(ROOT, "tools", "import-sources.tsv"), "w", encoding="utf-8") as f:
        f.write("file\tsquarespace_url\n")
        for _, works in years:
            for w in works:
                f.write(f"{w['file']}\t{w['src']}\n")

    target = os.path.join(ROOT, "works.js")
    if not works_js_is_empty(target):
        target = os.path.join(ROOT, "works.imported.js")
        print(f"\nworks.js already has paintings in it, so the list was written to {os.path.basename(target)} instead.")
    write_works_js(years, target)
    print(f"\nDone. Wrote {os.path.relpath(target, ROOT)}." + (f" {failed} images failed to download." if failed else ""))
    print("Next: open index.html in a browser and check the gallery, then fill in titles and status in works.js.")


if __name__ == "__main__":
    main()
