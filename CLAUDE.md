# lassetopbjerg.com — project notes for Claude Code

Lasse Topbjerg Storgaard's own website (painter, Mols, Denmark), moved from Squarespace to GitHub Pages; same setup and look as his retreat page (repo `lassetopbjerg/retreat`, live on https://malerefugium.dk). Lasse writes in Danish or English, so answer in the language he uses.

## Status (4 Nov 2026)

- **Live on https://lassetopbjerg.com** since 3 Nov 2026. Repo `lassetopbjerg/Lassetopbjerg`, Pages from `main`, folder `/`; the `CNAME` file holds the domain; HTTPS is enforced. Pushing to `main` updates the site (check it on a phone after each change). Keep all paths relative.
- **Domain:** still registered at Squarespace Domains (paid until 2027-04-26). DNS there: four A records for the root to 185.199.108.153 / .109.153 / .110.153 / .111.153 and `www` CNAME to `lassetopbjerg.github.io`; the Squarespace Defaults preset is deleted.
- **Paintings:** 65 paintings from 9 years (2015 to 2023–2024) imported from Squarespace on 3 Nov 2026 into `works/<year>/NN.jpg` (+ `thumbs/`); images over 2500px were shrunk. Titles, sizes and status in works.js are still empty.
- **Portrait:** `portrait.jpg` is the photo from the old contact page (Lasse talking in front of his paintings), 1200x1800.
- Retreat links (menu, footer) go to https://malerefugium.dk/ via `retreatUrl` in `window.SITE`.

## Next steps

1. **Fill in works.js with Lasse:** title (Danish, plus English if different), medium, size, and status `available` / `sold` / `private` / `""`. ONE painting is marked `featured: true` for the top of the site; otherwise the newest painting is used. Never invent titles or sizes; leave a field empty if Lasse doesn't know it.
2. **Transfer the domain to one.com** (where malerefugium.dk is): unlock it and get the auth code at Squarespace, start the transfer at one.com, then recreate the same DNS records there (four A records + `www` CNAME) and switch off one.com's own standard A records; leave MX alone.
3. **Cancel the Squarespace website plan** once the transfer is done and the site still loads on lassetopbjerg.com. Note the renewal date first.
4. **Share image** (1200x630, like the retreat page's `works/share.jpg`) plus `og:image` / `og:url` tags, once a featured painting is chosen. The site has no share tags yet.

## Structure

- `index.html`: the whole site. Settings at the top in `window.SITE` (email, phone, retreatUrl).
- `works.js`: the list of paintings, one block per year.
- `works/<year>/NN.jpg` and `works/<year>/thumbs/NN.jpg`: the images (some are .png / .jpeg as they came from Squarespace).
- `portrait.jpg`: the portrait in Om / About.
- `tools/import_squarespace.py`: the one-time import from Squarespace (done); `tools/import-sources.tsv` records where each image came from. New paintings are added by hand: image in `works/<year>/`, a ~750px-wide copy in `thumbs/`, large files at 2500px or less, and one line in works.js.

## How the site works

- **Same look as the retreat page:** dark umber ground #17120E, ivory text #EEE5D6, gold accent #C8A35E, Cinzel for names and labels and Source Serif 4 for running text. No italics or bold.
- **Menu at the top** (sticky): name on the left; Værker / Work · Malerefugium / Retreat · Om / About; DK and GB flags. On phones the name sits on its own row with the menu below.
- **Danish and English in one file.** Elements carry `lang="da"` or `lang="en"`, and `html[data-show]` hides the other language. Language choice: `#english`/`#dansk` in the link, then the last flag choice (localStorage), then the browser language (Scandinavian languages get Danish). Every text change must be made in BOTH languages. Gallery labels come from the `T` dictionary in the script.
- **Salon design (redesign A, live since 8 Nov 2026).** The previous design is saved as git tag `foer-salon-design`; to go back: `git checkout foer-salon-design -- index.html`, then commit and push (later text changes must be redone). The draft is the artifact https://claude.ai/artifact/WnURjE6RVbGg9tFGFxxTob; its About text is out of date, so don't copy from it.
- **Hero:** the `featured` painting (currently the woman lying down, `works/2023-2024/02.png`) in a gilt frame on a softly lit wall, then name, intro and button. The whole first screen should fit on a 1366 × 768 laptop.
- **Under Værker, no text, just the paintings (Lasse, 8 Nov 2026):** no intro sentence, no year labels under the band and no count of works. Year names appear only in the year index and the year headings.
- **Band of paintings** (Lasse may call it a bridge or piano): one vertical slice per year, oldest to newest, widening on hover (not on phones); a slice jumps to its year. `band` in `window.SITE` lists the painting used for each year; the 2023–2024 slice is deliberately the snake painting (`03.jpg`), since the wide woman painting would crop badly.
- **Gallery, newest year first.** The script sorts years by their highest 4-digit number, so "2023–2024" comes before "2023" and the order of the blocks in works.js doesn't matter; inside a year, the order in works.js is the order shown. A sticky year index marks the current year. Each year is a salon hang (CSS columns) where paintings keep their own proportions, with title (when filled in) and "Til salg" when available.
- **Single painting view:** a full-screen `<dialog>` with the large image, title (or "Uden titel"), year · medium · size, status, and one action: "Spørg om maleriet" (mailto with the title in the subject); "Spørg om et lignende" for sold works, and no button for private ones. Previous/next by buttons, arrow keys or swipe; Esc closes.
- **Graceful fallbacks:** a missing thumb falls back to the full image, and a missing image hides itself. With no paintings, the gallery shows a short message. Without a portrait, About is a single text column.
- **Om / About** with the contact block at the bottom (`#kontakt`): email and phone. Lasse's Instagram is not shown because it isn't active.

## Design principles (Lasse's own, follow them)

Lasse's principles: attention and clarity first; what is left out matters as much as what is in. Whitespace isolates the one main action. Few choices at once, and details are revealed progressively. Recognition over recall (thumbnails, not bare year numbers). Honest status (available/sold) and graceful fallbacks. Every element must justify its existence; never show placeholder brackets. Works at 390px phone width with no horizontal scroll. The full redesign brief is in the retreat repo at `notes/website-redesign-brief.md`.

## Content facts (confirmed by Lasse)

- NOT "in the old masters' tradition" (Lasse corrected this 3 Nov 2026). Works in many materials, mainly acrylics and oils. Background in visionary art, trained with many prominent teachers (no names given yet). Now leans more and more towards a classical approach: the human figure, archetypal symbolism, storytelling. Inspired by the old masters; strives for creative freedom; studying the old masters and nature gives him the tools to keep growing as an artist and a human. Lives in Mols by Nationalpark Mols Bjerge. Show ALL paintings, including the visionary work.
- The About text does not mention Jan-Ove (paragraph removed 3 Nov 2026 at Lasse's request); the retreat is reached through the menu and footer.
- Original paintings for sale; takes commissions; murals need not be mentioned (Lasse, 8 Nov 2026). No line above email and phone in the contact block.
- The Danish About text is Lasse's own wording (8 Nov 2026), so keep it as written. The English About text is deliberately not a translation of it: Lasse chose the earlier English version, with "mythical storytelling". Don't re-sync them unless he asks.
- Contact: lassetopbjerg@gmail.com, +45 31 17 75 06.

## Still open

- Titles, sizes and status for the 65 paintings.
- A proper photo of the woman lying down: the current file is a low-resolution Instagram screenshot (782 × 297, cropped 8 Nov 2026 to remove an arrow button and the room around it), and it is the first thing on the site.
- Domain transfer to one.com and cancelling Squarespace (steps above).
- Share image and share tags.
- Names of the teachers Lasse trained with, if he wants them in About.
