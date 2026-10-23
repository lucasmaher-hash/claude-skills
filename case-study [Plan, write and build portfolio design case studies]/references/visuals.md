# Visuals

Lead rule: **every image answers a question the text would otherwise have to answer.** What is
only pretty costs attention.

## The 30-second path

Someone who only scrolls reads headings, captions and images. Those three layers alone must tell
the story:

1. Hero: the product in use, ideally moving. No flat single screen on white.
2. One-liner + fact bar right below.
3. Before/after of the key decision.
4. One moving image of the core interaction.
5. Result as a number or an honest sentence.

Test: go through images + captions only. If the story breaks, an image or caption is missing.

## Image types

- **Before/after side by side**: the most valuable single image in any case study with a real
  decision. Same screens, same crop, same size. Slider if the page can do it cheaply.
- **Process images that show it was messy**: sketchbook, discarded variants, whiteboard. This
  builds credibility, it doesn't make the page look untidy.
- **Detail triplet per feature** (YesCheff): one main image/video, three smaller labelled states.
  Repeated, it gives a calm rhythm.
- **Product in context**: in a hand, in the room, at the moment of use (Calmsphere's hand + phone).
- **Product history** (old versions, Wayback Machine) when improving something that exists.
- **Labelled callout / exploded view** for physical products (Calmsphere's part callouts).

## Charts and diagrams

Draw only when a relationship would otherwise cost paragraphs.

| Type | When | Reference |
|---|---|---|
| Spectrum / axis | User groups between two poles, a strategy follows | Yuan's Hoarders vs Nomads |
| System small → large | Own model with terms that build on each other | Mercury's Module → Flow → Space |
| Options comparison | Several ways, one chosen; criteria as columns | Im's licence / T4 / T1 |
| Funnel / drop-off | Where users get lost and where design steps in | Im's 17 % drop-off |
| Single stat bar with brace | One finding with its parts (62 % texted, 38 % never tried → 83 % failed) | Unify problem section |
| 2×2 | Only if your product sits ALONE in one quadrant and it forces a decision (Calmsphere). A positioning quadrant with no decision reads as a generic deck slide | Calmsphere vs rejected Unify attempt |
| Pie / share of use | What people actually used; reorders the page | Unify results |
| Timeline | Versions, iterations, pivot points | Yuan's Apple Music history |

Rules for every chart:
- **One message per chart**, stated as a sentence in the title or caption.
- **Direct labels**, no legends.
- **Highlight what counts** (the chosen option, the relevant group, the drop-off) in the accent
  colour; everything else grey.
- **Drawn in the page's own style** (markup/SVG), never a spreadsheet screenshot. Keep each value
  in one place so swapping in real data is a number change.
- No pixel/decorative font inside a statistic: numbers are read, not decorated.

## Motion

- **Motion only where the thing itself moves**: gestures, transitions, state changes.
  Layout, brand, type and colour stay stills. (Yuan: 7 GIFs each, all on interactions.)
- 3–8 s seamless loops showing one thing; first and last frame match.
- No recording artefacts: wrong status-bar time, cursor, screen dimming at the end.
- Real or slightly slowed speed, never sped up.
- Launch/promo films as their own section at the end: proof it exists.
- Web: MP4 (H.264) not GIF, `autoplay muted loop playsinline`, poster frame, play only while
  on screen, respect `prefers-reduced-motion`.

## Captions

The second reading layer, and wasted on most portfolios.
- **Caption states the finding, not the content.** Weak: "Now Playing screen". Strong: "Double-tap
  to like, because users already tap the cover."
- Personality only where it comes from the subject. Short functional captions are fine for
  detail triplets.

## Rhythm and layout

- Never more than two paragraphs without an image.
- Repeat the same building block per feature; the reader learns it once.
- One climax: the key decision gets the biggest image.
- Scroll-driven effects sparingly; the page must read without JS and with reduced motion.
- Measured spacing from a strong reference (Jessica Im, imjiwoo.com, at 1440 px): body 18 px /
  1.4–1.55, subheads 28 px, stat numbers 48 px over 18 px labels, ~240–280 px between major
  sections, 40–80 px between sub-sections, 40 px label → heading and text → media, ~19 px
  heading → text. Cramped case studies read as unfinished.
- Long lines: inset the text column on wide screens (~60–75 characters per line).

## Accessibility and weight

- Alt text for every image that says what it shows; no essential text only inside images.
- Compress video (H.264, CRF ~23–26, check SSIM), set posters, lazy-load near viewport.
