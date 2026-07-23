# Cookbook Panels — Design Tokens

Exact values for the house style. The 2D column is the original Figma source;
the 3D column is what the panels were actually built with in Blender.

## Scale & coordinate mapping

- **1 web px = 0.01 Blender units** (`S = 0.01`).
- Y is flipped (web Y is down, Blender Y is up). For a panel `H` px tall:
  `D2B(wx, wy) = (wx * S, (H - wy) * S)`.
- Panel heights: **left/title = 283 px**, **right/ingredients = 360 px**.
- Two of the blob SVGs are rotated 90° in the 2D layout (the card and the
  strip) — rotate them 90° about Z before fitting. The segments SVG is not
  rotated.

## Colors (2D source, sRGB hex)

| Token        | Hex       | Used for                                  |
|--------------|-----------|-------------------------------------------|
| base         | `#C5D0D4` | panel body (becomes satin metal in 3D)    |
| ink          | `#0E1525` | primary text (ingredient names, body)     |
| title        | `#313156` | headers + dividers (2D)                    |
| meta         | `#8A9492` | secondary text (amounts, "5 portions…")   |
| divider      | `#C9D2D0` | thin separator lines in the ingredient list|
| purple       | `#BEBDF2` | glyph tiles / hourglass top bulb           |
| purple-px    | `#BCBCF6` | stepper pixel icons, filled strip segments |
| empty        | `#E7ECED` | empty strip segments / hourglass bottom    |
| glow         | `rgba(255,255,255,0.5)` blur 2.556px | the "slight glow" on purple px |

## 3D Materials (Blender Principled BSDF)

Create once with `make_materials()`. Exact final values:

| Material   | Base color | Metallic | Roughness | Specular | Emission        | Notes |
|------------|-----------|----------|-----------|----------|-----------------|-------|
| `M_Satin`  | `#CCCFD4` | 1.0      | 0.28–0.34 | 0.5      | —               | anisotropic 0.4; brushed aluminium for panels |
| `M_Purple` | `#5A36A8` | 0.0      | 0.38      | 0.5      | `#5A36A8` @ 0.18 | glyph tiles + highlighted segment; the "glow" |
| `M_Title`  | `#5A36A8` | 0.0      | 1.0       | **0.0**  | —               | header text + divider; **fully matte** |
| `M_Meta`   | `#0D0D0D` | 0.0      | 1.0       | **0.0**  | —               | body text; black, **fully matte** |
| `M_Seg`    | `#E7ECED` | 0.0      | 0.5       | 0.5      | —               | empty/grey strip segments |
| `M_Floor`  | `#29292B` | 0.0      | 0.6       | 0.5      | —               | dark studio floor (contrast for metal) |
| `M_Softbox`| `#E7E7E7` | 0.0      | 0.5       | 0.5      | white @ 6.0     | overhead reflection card / key |

The header/title purple `#5A36A8` is a darker, slightly-violet shade of the 2D
lavender — used consistently for the header text, the divider, the pixel-pot
glyph, and the highlighted strip tile so they read as one color family.

Matte text (`M_Title`, `M_Meta`) **must** have Specular = 0 and Roughness = 1,
or the color washes out when viewed straight-on (specular highlight).

## Typography

- **Font:** JetBrains Mono (2D uses Medium for headers, Regular for body). In
  Blender it currently falls back to the default `Bfont`; **load JetBrains Mono
  `.ttf` and assign it for fidelity** (`font` on the text data).
- Text objects: `align_x = LEFT`, `align_y = BOTTOM_BASELINE`, positioned at the
  baseline via `D2B`.
- **Thickness** comes from the curve `offset` (fattens strokes without a bold
  font), not from a heavier typeface.
- **Protrusion** comes from `extrude` (curve depth). Header protrudes fully;
  body text barely protrudes (nearly flat).

Final house sizes (left/title panel), after the user's two +20% bumps:

| Element | size  | offset | extrude | material |
|---------|-------|--------|---------|----------|
| Header  | 0.1786| 0.0058 | 0.018   | `M_Title` |
| Body    | 0.0893| 0.0032 | 0.0012  | `M_Meta`  |

Web-derived originals (before the bumps), for reference / proportion: header
`size 0.124`, body `size 0.062`. Multiply by ~1.44 to reach the house sizes.

## Geometry constants

- **Panel thickness:** 0.08 BU (solidify). Optional generously-rounded top-edge
  bevel (flat plateau kept) for a softer, pebble-like card.
- **Edge rounding on tiles/cubes:** Bevel **modifier**, width **0.006**,
  **2 segments**, `limit_method='ANGLE'`, angle 30°, `use_clamp_overlap=True`.
  This rounds all sharp edges a bit. (An edit-mode bevel on short vertical edges
  clamps to nothing — use the angle-limited modifier instead.)
- **Pixel-glyph (pot):** 16-col grid, tiles flattened to ~**0.042** tall, raised
  so they sit on the surface and rise from it (`M_Purple`). Grid pattern is in
  `build_panel.py` (`POT_GLYPH`).
- **Strip segments:** raised so their **tops reach the glyph-tile height
  (z ≈ 0.04)** while staying seated on the surface (scale Z, then re-seat).
  Empty = `M_Seg`; highlight one tile (e.g. the bottom one) with `M_Purple`.
- **Flush seating:** drop each top object so its bottom = panel-top − 0.002
  (2 mm sink) so there's no floating gap.

## Mesh cleanup (critical)

SVG import → convert-to-mesh → solidify produces heavily redundant geometry:
hundreds of duplicate/coincident verts, T-junctions, and overlapping collinear
edges. It looks fine while flat but shows as tangled crisscross edges once a tile
is raised or beveled. `clean_mesh()` fixes it:

1. `remove_doubles(0.0018)` — weld coincident verts.
2. `dissolve_limited(4–5°)` — collapse collinear/coplanar redundancy (below the
   bevel's ~15–30° steps, so rounding survives).
3. `dissolve_degenerate` + `delete_loose` — drop slivers and stray edges.
4. Detect remaining T-junction verts (a vert sitting mid-edge) and
   `dissolve_verts` them; repeat the weld.
5. `fill_holes` + `normals_make_consistent`.

Target: 0 non-manifold, 0 holes, 0 T-junctions, 0 overlapping edges.

## Lighting & render

- Engine EEVEE with **`scene.eevee.use_raytracing = True`** (metal needs traced
  reflections).
- **Dark world** (~`#0E0E12`, strength ~1) + a **bright emissive softbox** plane
  overhead + a moderate area key. Metal reads as silver-with-highlights only
  with this contrast; on a bright uniform world it looks flat white.
- A dark floor plane gives a contact shadow and darkens lower reflections.
- For checking colors/edges instead of metal, a brighter close-up render is fine.
