# Reference Image Index

These are the ground-truth visual references for the nothing-design skill. Read at least 3 before designing.

## Neumorphic chrome (containers, buttons, shadows)

- **IMG_3647.JPG** — Neumorphism spec sheet (3 squares). Background `#F0F0F3`, drop shadow values (-10px -10px 30px #FFFFFF + 10px 10px 30px #AEAEC0 @ 40%), inner shadow values. The canonical spec — match these shadows exactly.
- **IMG_3644.JPG** — Neumorphism circles spec. Three circles showing drop, inner, and combined inner+outer shadows with named layers (Shadow 2, Shadow 4). Useful for understanding inset/pressed state.
- **IMG_3645.JPG** — Neumorphic search bar variations (4 different shapes: pill, rectangular, with/without separated icon button).
- **04F544BA-F50F-4BFE-835C-8BFCC03293E3.GIF** — Animated tab switcher (Recent / Archived) showing hover and active-press transitions. The active tab gets a deeper inset; the bar lifts with `shadow/raised`.
- **88FF202B-5ACF-4B15-8F25-4B84F7DA8C46.GIF** — Animated radio buttons (a/close, b/remove, c/delete, d/all of the above) demonstrating press-down inset behavior on click.

## Nothing OS-style content (typography, icons, layout)

- **IMG_3621.jpg** — Nothing-style radio app: "PLAY KISS FM FOR ME". Pixel font heading, dot-matrix audio visualizer, FM tuner strip. Shows the pure Nothing content vibe.
- **IMG_3636.JPG** — Nothing OS Equaliser screen. Shows: pixel heading "EQUALISER", black pill button ("SIMPLE" active) + outlined pill ("ADVANCED"), neumorphic circular control with draggable dots, neumorphic pill buttons in a 2×2 grid, full-width black pill primary CTA ("CUSTOM").
- **IMG_3627.JPG** — Nothing Ear (1) quick start guide. 9-panel grid layout with pixel-font headings (01/02/03/04/05/06), all-caps monospaced body, generous whitespace. Single red accent dot in panel 06. Reference for grid-based information layouts.
- **IMG_3633.JPG** — Nothing OS Dual Connection settings screen. Pixel heading, monospaced body, toggle switch, thin divider, checkbox list. Reference for settings/list layouts.
- **IMG_3643.JPG** — "17" stat screen with single orange accent dot. Massive pixel numeral, fine vertical-line graph below, neumorphic stat tiles at bottom. Best example of the orange-accent-dot rule (one dot, perfectly placed).
- **IMG_3635.jpg** — Dark-mode recorder UI. Orange accents on a black background (volume/gain sliders, REC indicator, level meters). Counter-example showing how the aesthetic works inverted — useful if user ever asks for dark mode.

## Hybrid examples (neumorphic chrome + Nothing content)

- **IMG_3642.JPG** — Music player with neumorphic card containing pixel "9/08 6 PM" heading, neumorphic sub-card with audio track info, large analog-style neumorphic clock, neumorphic pill controls. Strong example of the combined aesthetic.
- **IMG_3646.JPG** — "visual.study" stats screen. Massive pixel "17" with orange dot, fine-line area chart, neumorphic pill labels and stat cards at bottom. Hybrid composition.

## Adjacent styles (for context, not direct emulation)

- **IMG_3626.jpg** — MUTEK MX festival website. Editorial typography, rotated text, dark/light split. Not neumorphic — shows the Nothing-adjacent monospaced editorial direction.
- **IMG_3640.JPG** — Instagram story cards with bold orange usage. Shows what NOT to do (orange as block fill) — but useful for typography proportions.
- **IMG_3641.jpg** — Cyrillic project listing. Heavy display numerals, monospaced body. Layout-only inspiration.
- **IMG_3632.JPG** — TUESDAY recording app. Pixel heading, neumorphic stat cards, RED button (not our orange). Layout reference; ignore the red color.
- **IMG_3638.JPG** — Dark weather dashboard for "TBILISI". Cream + black cards on dark background. Layout grid is useful; color treatment is for the dark-mode case.

## How to use these

When triggered, read 3–5 images covering:
1. At least one **chrome spec** (IMG_3647 or IMG_3644)
2. At least one **pure Nothing content** screen (IMG_3621 or IMG_3636)
3. At least one **hybrid composition** (IMG_3642 or IMG_3646)
4. The **interactive GIFs** if hover/press behavior is relevant to what you're building

Don't try to read all of them — pick what's most relevant to the screen type the user asked for.
