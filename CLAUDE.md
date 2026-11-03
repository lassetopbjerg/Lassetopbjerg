# lassetopbjerg.com — project notes for Claude Code

Lasse Topbjerg Storgaard's own website (painter, Mols, Denmark), moving from Squarespace to GitHub Pages, the same setup as his retreat page (repo `lassetopbjerg/retreat`, see that repo's CLAUDE.md). Lasse writes in Danish or English, so answer in the language he uses.

## Status (3 Nov 2026)

Step 1 done 3 Nov 2026: 65 paintings from 9 years (2015 to 2023–2024) imported into works/ and works.js; images over 2500px were shrunk. Titles, sizes and status are still empty.

The site is built and tested with demo images, and pushed to GitHub (3 Nov 2026), but it has **no paintings yet**. The old Squarespace site is still live, so do NOT cancel Squarespace or move the domain until the new site is live and Lasse has checked it.

### Steps, in order

1. **Import the paintings from Squarespace.** Run on Lasse's PC, since it needs normal internet:
   ```bash
   python3 tools/import_squarespace.py --dry-run   # lists years and image counts
   python3 tools/import_squarespace.py             # downloads into works/<year>/ (+ thumbs/) and writes works.js
   ```
   The script is tested against fake Squarespace pages only. If it finds no years or wrong images, look at the real HTML of https://www.lassetopbjerg.com/portfolio and the year pages, then adjust `find_year_pages()` / `image_urls()`. Images that also appear on the portfolio index (the logo) are skipped on purpose. `tools/import-sources.tsv` records where each file came from.
   If Lasse has better originals on his PC, use those instead and keep the same `works/<year>/NN.jpg` layout. Make thumbs about 750px wide in `works/<year>/thumbs/`, and keep large files at 2500px or less.
2. **Fill in works.js with Lasse:** title (Danish, plus English if different), medium, size, and status `available` / `sold` / `private` / `""`. Mark ONE painting `featured: true` for the top of the site; otherwise the newest painting is used. Never invent titles or sizes. Leave a field empty if Lasse doesn't know it.
3. **Portrait:** put a photo of Lasse at `portrait.jpg` (shown in "Om"). Without it, the About section is text only, which also works.
4. **Repo and publishing:** the repo is `lassetopbjerg/Lassetopbjerg` (created by Lasse on 3 Nov 2026), and GitHub Pages serves `main`, folder `/`, at https://lassetopbjerg.github.io/Lassetopbjerg/. Pushing to `main` updates the site. Check it on a phone after each change. Since a project page lives in a subfolder, all paths in the site are relative; keep them that way.
5. **Move the domain lassetopbjerg.com.** First find out where it is registered (Squarespace → Settings → Domains). Either keep it there without a website plan or transfer it to one.com (where malerefugium.dk is). DNS: four A records for `@` to 185.199.108.153 / .109.153 / .110.153 / .111.153 and `www` CNAME to `lassetopbjerg.github.io`; remove Squarespace's own records for `@` and `www`. Only once `http://lassetopbjerg.com` resolves to GitHub: add a `CNAME` file containing `lassetopbjerg.com`, check Settings → Pages shows a green DNS check, then tick Enforce HTTPS. (Lesson from malerefugium.dk: adding the CNAME file before DNS works makes the github.io address forward to a domain that doesn't load.)
   Also check whether any email uses the domain (MX records) before changing DNS. Lasse uses Gmail, so probably not.
6. **Cancel Squarespace** only after the site is live on lassetopbjerg.com. Note the renewal date first.
7. Done 3 Nov 2026: all retreat links point to https://malerefugium.dk/.

## Structure

- `index.html`: the whole site. Settings are at the top in `window.SITE` (email, phone, retreatUrl).
- `works.js`: the list of paintings, one block per year.
- `works/<year>/NN.jpg` and `works/<year>/thumbs/NN.jpg`: the images.
- `portrait.jpg`: optional.
- `tools/import_squarespace.py`: the one-time import from Squarespace (standard library only).

## How the site works

- **Same look as the retreat page:** dark umber ground #17120E, ivory text #EEE5D6, gold accent #C8A35E, Cinzel for names and labels and Source Serif 4 for running text. No italics or bold.
- **Menu at the top** (sticky): name on the left; Værker / Work · Malerefugium / Retreat (link to the retreat page) · Om / About; DK and GB flags. On phones the name sits on its own row with the menu below.
- **Danish and English in one file.** Elements carry `lang="da"` or `lang="en"`, and `html[data-show]` hides the other language. Language choice: `#english`/`#dansk` in the link, then the last flag choice (localStorage), then the browser language (Scandinavian languages get Danish). Every text change must be made in BOTH languages. Gallery labels come from the `T` dictionary in the script.
- **Gallery, newest year first.** The script sorts years by their highest 4-digit number, so "2023–2024" comes before "2023" and the order in works.js doesn't matter. Each year is a native `<details>` fold-out showing a row of up to 6 thumbnails, the year and a count. The newest year is open by default. Inside: a grid of paintings with title and "Til salg" when available.
- **Single painting view:** a full-screen `<dialog>` with the large image, title, year · medium · size, status, and one action: "Spørg om maleriet" (mailto with the title in the subject); "Spørg om et lignende" for sold works, and no button for private ones. Previous/next by buttons, arrow keys or swipe; Esc closes.
- **Graceful fallbacks:** a missing thumb falls back to the full image, and a missing image hides itself. With no paintings, the gallery shows a short message. Without a portrait, About is a single text column.
- **Om / About** with the contact block at the bottom (`#kontakt`): email and phone. Lasse's Instagram is not shown because it isn't active.

## Design principles (Lasse's own, follow them)

Lasse's principles: attention and clarity first; what is left out matters as much as what is in. Whitespace isolates the one main action. Few choices at once, and details are revealed progressively. Recognition over recall (thumbnails, not bare year numbers). Honest status (available/sold) and graceful fallbacks. Every element must justify its existence; never show placeholder brackets. Works at 390px phone width with no horizontal scroll. The full redesign brief is in the retreat repo at `notes/website-redesign-brief.md`.

## Content facts (confirmed by Lasse)

- Paints in oil in the old masters' tradition: figures, portraits, the landscape around Mols / Nationalpark Mols Bjerge.
- Studied with Jan-Ove Tuv at the Nerdrum Museum in Stavern in 2026. Jan-Ove teaches Malerefugium på Mols, 12–16 June 2027.
- Original paintings for sale; takes mural commissions.
- Contact: lassetopbjerg@gmail.com, +45 31 17 75 06.

## Still open

- Squarespace domain registration and renewal date (Lasse to check).
- Portrait photo.
- Titles, sizes and status for the paintings.
- Which painting to feature at the top.
- A share image (1200x630) like the retreat page's, once there is a featured painting.
