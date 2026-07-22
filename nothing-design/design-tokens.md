# Design Tokens — Nothing-Design

All exact values. Set these up as **local variables in Figma** before placing any visual element. Bind every fill, stroke, shadow color, corner radius, and font size to the variable, not a hardcoded value.

## Color palette

| Token | Hex | Usage |
|---|---|---|
| `bg/surface` | `#F0F0F3` | Page background AND container fill (neumorphism requires container = background) |
| `bg/white` | `#FFFFFF` | Light shadow side; occasional inset highlights |
| `bg/black` | `#1A1A1A` | Primary text, black pill buttons, icons |
| `text/primary` | `#1A1A1A` | All headings, body text |
| `text/secondary` | `#8E8E93` | Muted labels, metadata, secondary info |
| `text/tertiary` | `#C7C7CC` | Disabled / very-de-emphasized text |
| `divider` | `#1A1A1A` @ 1px stroke, or `#8E8E93` for softer | Thin lines only — never thicker than 1px |
| `shadow/dark` | `#AEAEC0` | Bottom-right shadow on neumorphic elements |
| `shadow/light` | `#FFFFFF` | Top-left highlight on neumorphic elements |
| `accent/orange` | `#FF5C00` | Nothing orange. Use SPARINGLY — 1–2 elements per screen max |

No other colors. No blues, greens, purples, gradients. Monochrome + the one orange.

## Shadow recipes

Build each as a Figma **effect style** so you can reuse and update centrally.

### `shadow/raised` — default state for cards, buttons, surfaces
- Drop shadow: X=`8`, Y=`8`, Blur=`18`, Spread=`0`, Color=`#AEAEC0` at `65%`
- Drop shadow: X=`-8`, Y=`-8`, Blur=`18`, Spread=`0`, Color=`#FFFFFF` at `100%`

### `shadow/raised-sm` — small elements (toggles, icon buttons, chips)
- Drop shadow: X=`5`, Y=`5`, Blur=`12`, Spread=`0`, Color=`#AEAEC0` at `65%`
- Drop shadow: X=`-5`, Y=`-5`, Blur=`12`, Spread=`0`, Color=`#FFFFFF` at `100%`

### `shadow/raised-lg` — large hero containers, modals
- Drop shadow: X=`10`, Y=`10`, Blur=`24`, Spread=`0`, Color=`#AEAEC0` at `65%`
- Drop shadow: X=`-10`, Y=`-10`, Blur=`24`, Spread=`0`, Color=`#FFFFFF` at `100%`

### `shadow/hover` — hover state (deeper, more extruded)
- Drop shadow: X=`10`, Y=`10`, Blur=`24`, Spread=`0`, Color=`#AEAEC0` at `80%`
- Drop shadow: X=`-8`, Y=`-8`, Blur=`18`, Spread=`0`, Color=`#FFFFFF` at `100%`
- (Optionally) Y-translate the layer by `-2` for an extra lift cue

### `shadow/pressed` — active/pressed inset
- Inner shadow: X=`5`, Y=`5`, Blur=`10`, Spread=`0`, Color=`#AEAEC0` at `60%`  ← dark at top-left
- Inner shadow: X=`-5`, Y=`-5`, Blur=`10`, Spread=`0`, Color=`#FFFFFF` at `100%`  ← light at bottom-right
- (Container fill stays #F0F0F3)

## Typography

Three fonts only — `OCR-A BT` is a locally installed font (must be installed on the machine running Figma); `VT323` and `Roboto` are bundled in `fonts/` for portability.

Bundled font files in `fonts/`:
- `VT323-Regular.ttf`
- `Roboto-Regular.ttf`, `Roboto-Medium.ttf`, `Roboto-Bold.ttf`

**`OCR-A BT Regular`** — locally installed, not available via Figma's built-in font picker or plugin `listAvailableFontsAsync`. Must be installed on the OS. When building via plugin, text style metadata can be set but `loadFontAsync` will fail — apply the font manually via the Figma desktop app if the plugin can't load it. Load with `figma.loadFontAsync({ family: 'OCR-A BT', style: 'Regular' })`.

### Font families
- **Display** (page titles, hero headings): `OCR-A BT Regular` — monospaced OCR typeface, technical and editorial at once. Tight negative tracking gives it a cold, precise character that fits the Nothing-OS aesthetic.
- **Pixel labels / terminal** (small all-caps labels, monospace data, device-readout feel): `VT323` — narrow terminal-pixel font.
- **Body / UI text** (paragraphs, descriptions, secondary labels, button text): `Roboto` — clean modern sans. Available in Regular / Medium / Bold.

Use OCR-A BT sparingly — typically **one** display heading per screen. VT323 carries the smaller pixel-styled labels and button text (UPPERCASE). Roboto handles everything readable.

### Type scale
| Token | Font | Size | Weight | Letter-spacing | Case | Use |
|---|---|---|---|---|---|---|
| `display/xl` | OCR-A BT | 56px | Regular (400) | -4% | Original | Hero headings, splash titles |
| `display/lg` | OCR-A BT | 44px | Regular (400) | -4% | Original | Page titles (most common display) |
| `display/md` | OCR-A BT | 32px | Regular (400) | -4% | Original | Section headings |
| `display/sm` | VT323 | 24px | Regular (400) | 0 | UPPER | Card headings, smaller pixel callouts |
| `label/lg` | VT323 | 16px | Regular (400) | 5% | UPPER | Section labels, pixel-style button text |
| `label/md` | VT323 | 14px | Regular (400) | 5% | UPPER | Small labels, metadata |
| `label/sm` | Roboto | 12px | Medium (500) | 8% | UPPER | Tiny UI labels where pixel font would be illegible |
| `body/lg` | Roboto | 16px | Regular (400) | 0 | Original | Primary body paragraphs |
| `body/md` | Roboto | 14px | Regular (400) | 0 | Original | Default body / button text |
| `body/sm` | Roboto | 12px | Regular (400) | 0 | Original | Secondary descriptions |

### Casing
- `display/*` (OCR-A BT) renders in **original/mixed case** — the monospaced OCR character reads cleanly in title case.
- `label/*` (VT323 + the smallest Roboto label) renders in **UPPERCASE** with positive tracking — that's where the pixel-style device-readout feel lives.
- `body/*` uses **original case** for readability.

### Line-height
- Display: 1.05–1.1 (tight, lets multi-line headings stack densely)
- Body: 1.5–1.6 (generous for legibility)

## Spacing scale (use for padding, gap, margin)

Base unit = 4px. Use these tokens only:

| Token | Px |
|---|---|
| `space/1` | 4 |
| `space/2` | 8 |
| `space/3` | 12 |
| `space/4` | 16 |
| `space/5` | 24 |
| `space/6` | 32 |
| `space/7` | 48 |
| `space/8` | 64 |
| `space/9` | 96 |

### Spacing rules
- Inside a neumorphic container: minimum `space/5` (24px) padding on all sides
- Between sections on a page: `space/6` (32px) to `space/7` (48px)
- Between sibling items in a list: `space/3` (12px) to `space/4` (16px)
- **Page outer padding (mobile): `space/6` (32px) MINIMUM, `space/7` (48px) preferred. Desktop: `space/8` (64px) or more.** Smaller values clip neumorphic shadows at the screen edge — see the shadow safe-area rule below.

Whitespace is a feature, not waste. When in doubt, add more.

### Shadow safe-area rule (critical for neumorphism)

Neumorphic shadows extend ~15–55 px outward from a node's bounding box. If the node sits flush against a clipping parent (page frame, card frame), the shadow gets cut off and the element looks broken.

Two hard rules to prevent this:

1. **EVERY frame in the ancestor chain of a neumorphic element must set `clipsContent = false`.** This is not just the page-level frame — it applies to ALL container frames: the page frame, every intermediate group frame (buttonsGroup, headingRow, card-content rows, list wrappers), and any auto-layout wrapper. Figma frames default to `clipsContent: true`, which silently clips any shadow that extends past the frame's bounding box. **If even one ancestor in the chain clips, the shadow gets cut.** Set `clipsContent = false` on every container as you build it — make it part of muscle memory, not an afterthought. Transparent fills do NOT prevent clipping; clipping is about the box, not the fill.
2. **Page outer horizontal padding must be ≥ shadow blur radius + 8 px breathing room** for any neumorphic element placed full-width.

Practical clearance table:
| Shadow used on full-width children | Min page horizontal padding |
|---|---|
| `shadow/raised-sm` (18 px blur) | `space/6` (32 px) minimum, `space/7` (48 px) safer |
| `shadow/raised` (35 px blur) | `space/7` (48 px) minimum, `space/8` (64 px) safer |
| `shadow/raised-lg` (45 px blur) | `space/8` (64 px) minimum |
| `shadow/hover` (45 px blur, used on hover) | Same as `shadow/raised-lg` — plan for hover even if the resting shadow is smaller |

Rule of thumb: if you use `shadow/raised` or larger on full-width buttons, page padding is `space/7` (48 px). If you stick to `shadow/raised-sm`, you can drop to `space/6` (32 px). **Never `space/5` (24 px) for mobile page padding** — contrast-boosted shadows need breathing room.

## Corner radius

| Token | Px | Use |
|---|---|---|
| `radius/sm` | 8 | Tiny chips, tags |
| `radius/md` | 16 | Buttons, small cards |
| `radius/lg` | 24 | Standard cards and containers (most common) |
| `radius/xl` | 32 | Hero containers, modals |
| `radius/pill` | 9999 (fully rounded) | Pill buttons, switches, search bars |

## Borders / strokes

- Strokes are rare. Neumorphism uses shadow, not stroke, to define edges.
- Allowed: 1px stroke `#1A1A1A` for thin dividers between sections.
- Allowed: 1px stroke `#1A1A1A` outlining outlined-style pill buttons (the "Advanced" variant in the Nothing Equaliser reference).
- Never: thick borders, dashed borders, double borders.

## Iconography

- Outline-style icons only, 1.5px stroke, monochrome.
- Pixel-grid icons (matching Nothing's icon set vibe) preferred when available.
- Icon size: 16px (small), 20px (default), 24px (large).
- Color: `#1A1A1A` (primary) or `#8E8E93` (muted).

## Dot-matrix patterns

A signature element. Use for:
- Data visualizations (bar charts, audio waveforms, sparklines)
- Decorative ambient fills (low-opacity behind content)
- Status indicators / loading states

Specs:
- Dot diameter: 4px (default), 3px (dense), 6px (large)
- Grid spacing: 8px center-to-center (1.5–2× dot diameter)
- Color: `#1A1A1A` for active dots, `#C7C7CC` for inactive/background dots
- Build as a component with a configurable matrix (e.g., 32 cols × 16 rows) so you can scale up/down

## Accent orange usage rules

`#FF5C00` is a precious resource. Rules:

1. **Max two orange elements per screen.** Often just one.
2. Acceptable orange elements: a single dot (status, decoration), a single key numeral or word, a thin underline beneath a heading, a small recording-indicator dot.
3. **Forbidden**: orange as a button fill, orange as a large block, orange text in body copy, orange icons (other than a tiny accent dot).
4. The orange should feel like it's pointing at something — drawing the eye to the one thing that matters most on the screen.
