// ============================================================
// THE PAINTINGS
// One block per year. The site sorts the years itself, newest
// first, so the order here does not matter. Paintings show in the
// order they are listed within each year.
//
// Each painting:
//   file      the full-size image, e.g. "works/2024/01.jpg"
//             (a smaller copy in works/2024/thumbs/01.jpg is used
//             in the grid if it exists)
//   title     Danish title (leave "" if it has none)
//   titleEn   English title (optional; the Danish one is used if empty)
//   medium    e.g. "Olie på lærred"      mediumEn: "Oil on canvas"
//   size      e.g. "70 × 50 cm"
//   status    "available" (til salg), "sold" (solgt),
//             "private" (privateje) or "" (nothing shown)
//   featured  true on ONE painting to show it at the top of the site
//
// Fill this file by running:  python3 tools/import_squarespace.py
// ============================================================

window.WORKS = [
  // {
  //   year: "2024",
  //   works: [
  //     { file: "works/2024/01.jpg", title: "Selvportræt", titleEn: "Self-portrait",
  //       medium: "Olie på lærred", mediumEn: "Oil on canvas", size: "60 × 50 cm",
  //       status: "available", featured: true }
  //   ]
  // }
];
