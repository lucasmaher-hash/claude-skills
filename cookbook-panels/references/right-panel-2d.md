# Right "Ingredients" Panel — 2D spec

The 2D source for the right panel (Figma `right panel`, 317 × 360 px). Use this
to build it in 3D next, applying the same house materials/scale from
`design-tokens.md`. All px are within the 317×360 panel unless noted; convert
with `D2B(wx, wy)` using **H = 360**.

## Layout overview

- **Right card blob** — `assets/right_blob.svg` (rotated −90° in 2D), occupies the
  right ~2/3 of the panel. Holds the ingredient list + stepper. → satin metal.
- **Hourglass** — on the left ~1/3: `assets/hourglass_outer.svg` (outer blob,
  rotated −90°), `assets/hourglass_top_bulb.svg` (purple `#BEBDF2`, glowing) and
  `assets/hourglass_bottom_bulb.svg` (empty `#E7ECED`). The bulbs are the same
  teardrop (90.519 × 120.146); the top one is flipped 180°. → top bulb `M_Purple`,
  bottom bulb `M_Seg`/empty.
- **Ingredients panel** — rounded-rect (radius 7.497px, clipped) at inset
  `16.11% 3.47% 3.9% 32.49%` of the right panel (≈ x 103→306, width 203).

## Ingredient rows

Each row: right-aligned **amount** + left **name** + optional small **descriptor**
below the name. Columns inside the ingredients panel:

- amount: `left 27.31, width 53.55, text-align right`, `M_Meta` color, 7.497px.
- name:   `left 87.28, width 101.2`, `ink #0E1525` (→ `M_Meta` black), 7.497px.
- descriptor: `left 87.28`, `M_Meta`, 5.355px, sits ~9.6px below the name.

| Ingredient        | Amount | name top | descriptor        |
|-------------------|--------|----------|-------------------|
| Penne             | 500 g  | 69.24    | rigate (78.88)    |
| Chopped tomatoes  | 500 g  | 94.94    | from the can (104.58) |
| Chicken broth     | 300 g  | 120.64   | —                 |
| Cream             | 200 g  | 146.35   | —                 |
| Bacon             | 120 g  | 172.05   | diced (181.69)    |
| Spinach           | 100 g  | 197.75   | chopped (207.39)  |
| Peas              | 50 g   | 223.45   | —                 |

Dividers (`#C9D2D0`, h 0.535): a header divider at top **55.31**, and two more
at **221.04** (after Spinach) and **246.75** (after Peas). NOTE: in the final web
build the user removed the bottom two dividers — keep only the header divider
unless asked otherwise.

Amounts scale with the portions count (base 5): `grams * portions / 5`, rounded
to the nearest 5 g.

## Portions stepper

Top of the ingredients panel (`Frame 3`, x 42, width 157.34, height 40.32):

- Pill: border 1px black, **radius 22px**, horizontal padding 6px, gap 9px.
- Center label: **"5 PEOPLE"** (`{n} PEOPLE`, or "PERSON" if 1), medium,
  **10.71px**, `ink #0E1525` (→ matte). 
- Minus button (left) and Plus button (right): each a ~37–38 × 40px hit area with
  a transparent "plate" (`rgba(14,21,37,0)`) and small pixel glyphs forming a − / +
  out of `#BCBCF6` rounded pixels (radius 0.87) with the white glow
  (`0 0 2.436px rgba(255,255,255,0.55)`). → `M_Purple` for the px in 3D.

For 3D: the stepper is decorative geometry (raised pill outline + purple pixel
icons + matte label), seated flush like the rest. The − pixels are a single
horizontal row; the + pixels are a plus sign (see the 2D node for exact offsets,
or just lay out a clean − and + on the same pixel grid).

## Build order (suggested)

1. Right card blob + hourglass outer blob → import, fit (H=360), solidify, clean,
   satin material.
2. Hourglass bulbs (top purple/glow, bottom empty), seated in the hourglass.
3. Ingredients: build text rows (amounts `M_Meta`, names `M_Meta` black,
   descriptors `M_Meta` small) — all matte, barely-protruding extrude like the
   left panel's body text.
4. Header divider (thin raised bar, `M_Title` or a neutral).
5. Portions stepper: pill outline + purple pixel − and +, matte "N PEOPLE" label.
6. Seat everything flush; bevel any raised tiles; metal lighting.

Keep the same scale (0.01), the same materials, and the same matte-text /
clean-mesh / metal-contrast rules from `design-tokens.md`.
