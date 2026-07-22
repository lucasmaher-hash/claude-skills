# Stopwatch Timer — 2D spec

The 2D source for the stopwatch/timer modal (Figma `stopwatch` frame, 419.621 × 388.334 px). Use this to build it in 3D, applying the same house materials/scale from `design-tokens.md`. All px are within the 419.621 × 388.334 modal unless noted; convert with `D2B(wx, wy)` using **H = 388.334**.

## Layout overview

- **Stopwatch blob background** — `assets/stopwatch_blob.svg`, the organic two-ear shape. → satin metal.
- **White center ring** — circle at center (r ≈ 138), holds the timer display and purple progress segments.
- **Purple segmented ring** — 20 equal segments (dash 85%, gap 15%) around the white ring. Fills up as the countdown runs (via stroke-dashoffset animation in web version).
- **Inner gray center circle** — r ≈ 97.38, contains the time display.
- **Close button** — bottom-left ear: 5×5 pixel grid forming an X (rotated plus pattern).
- **Play/Stop button** — top-right ear: toggles between triangle (play, 5 dots) and square (stop, 3 dots).
- **Time display** — center, JetBrains Mono Medium, size 41.964px, color `#313156`, text "00:35" or countdown.

## Materials & colors

| Element | Color | Material (3D) |
|---------|-------|---|
| Blob body | `#c5d0d4` | M_Satin |
| White ring | `#f4f6f6` | Emit or white (see below) |
| Gray inner circle | `#c5d0d4` | M_Satin |
| Purple segments | `#bebdf2` | M_Purple |
| Time text | `#313156` | M_Title |

For 3D: The white ring (r=138) is a simple plane or cylinder, non-metallic. The gray inner circle can be the same satin material as the blob body. The purple segments sit on top, raised slightly (same height as pixel-glyphs on the left panel, ≈ 0.04 BU tall).

## Build order (suggested)

1. **Stopwatch blob body** → import `stopwatch_blob.svg`, fit to design size, solidify, clean, apply M_Satin.
2. **White center ring** → create a cylinder or plane at r=138 (inner edge, not filled; just the ring area), apply white material (non-metallic).
3. **Gray inner center circle** → r ≈ 97.38, apply M_Satin.
4. **Purple segmented ring** — build as 20 raised tiles or as a single circle with bevel (see below). Apply M_Purple, seat flush on the white ring.
5. **Center time text** — matte text, M_Title material, centered in the inner gray circle.
6. **Button glyphs** — pixel dots forming the close (X) and play (triangle)/stop (square) icons, positioned on the ears, M_Purple, raised.
7. **Lighting** — same setup as left panel: dark world, bright softbox, ray tracing.

## Ring construction (3D implementation)

The stopwatch uses **20 discrete raised tiles** arranged in a circle (Option B from above):
- Each segment is a small raised cube positioned radially around the center
- Height: ~0.042 BU (matches pixel-glyph height on left panel)
- Material: M_Purple with emission glow
- Positioned at radius ~1.67 BU (the purple ring in the web version)
- Each tile can be individually highlighted or colored as the countdown progresses

This matches the web version's stroke-dasharray effect with discrete visual boundaries.

## Scale & positioning

- **Panel size:** 419.621 × 388.334 px
- **Scale:** 1 web px = 0.01 Blender units (same as left/right panels)
- **Blob position:** Centered in the 419.621 × 388.334 design rect
- **White ring center:** (≈ 209.7, ≈ 193.9) in design px → `D2B(209.7, 193.9, 388.334)` in BU
- **Inner gray circle center:** Same as white ring center
- **Time text:** Centered in the inner gray circle (r ≈ 97.38)
- **Close button (X):** Bottom-left ear, centered in that bulge, rotated –44.38°
- **Play/Stop button:** Top-right ear, centered in that bulge

All elements sit flush on the blob's flat top (seated with `seat_flush()`, small 0.002 sink so no gaps).
