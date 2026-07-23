---
name: cookbook-panels
description: >-
  Build "cookbook" UI panels as physical 3D objects in Blender — the organic
  blob-shaped cards with a satin-metal finish, raised purple pixel-glyphs, a
  segmented progress strip, and matte extruded text. Use this WHENEVER the user
  wants to create, extend, or restyle one of these panels in Blender (e.g.
  "build the right/ingredients panel", "make another step panel", "add a panel
  like the title one", "recreate this cookbook screen in 3D"), or asks for the
  panel's design tokens (colors, fonts, materials, dimensions). It carries the
  exact house style — colors, font sizes, materials, scale convention, and the
  hard-won mesh-cleanup / lighting gotchas — so new panels match without
  rediscovering them. Trigger even if the user doesn't say "skill".
---

# Cookbook Panels (Blender)

These panels come from a 2D cookbook UI (Figma) rebuilt as tactile 3D objects.
A panel is an organic **blob-shaped card** in **satin/brushed aluminium**, with
content sitting on its flat top: **matte extruded text**, a **raised purple
pixel-glyph**, and a **segmented strip**. Everything is driven through the
Blender MCP (`execute_blender_code`).

This skill exists because building one of these from scratch is full of traps —
the source SVG shapes import as filthy, overlapping meshes; metal looks like
flat plastic unless the environment has contrast; matte text washes out unless
specular is killed. The tokens and the bundled builder encode all of that.

**Now includes the stopwatch timer modal** — a secondary container with a blob
background, white center ring, 20 purple progress segments, and interactive
buttons (play/stop, close) built as pixel glyphs.

## Files

- `scripts/build_panel.py` — the parametric builder + all reusable utilities
  (SVG import+clean, house materials, pixel-glyph, flush seating, bevel, metal
  lighting). **Read it before building** — call its functions rather than
  re-deriving them. Includes `build_left_panel()`, `build_right_panel()` (stub),
  and `build_stopwatch()`.
- `references/design-tokens.md` — every color, font size, material spec, and
  geometry constant, with the 2D→3D mapping. Read when you need an exact value.
- `references/right-panel-2d.md` — the 2D spec of the right "ingredients" panel
  (rows, portions stepper, hourglass) for building that one next.
- `references/stopwatch-2d.md` — the 2D spec of the stopwatch timer modal
  (blob, white ring, purple segments, time display).
- `assets/*.svg` — the organic blob silhouettes (card, strip, segments, right
  card, hourglass parts, stopwatch). Reuse these; don't redraw them.

## Workflow for a new panel

1. **Set `ASSET_DIR`** at the top of `build_panel.py` to this skill's `assets/`
   folder (absolute path), then load the script into Blender via
   `execute_blender_code` (exec the file contents, or paste the helpers).
2. **Pick the panel height** in px for the Y-flip: `283` for the left/title
   panel, `360` for the right panel. The scale is **1 web px = 0.01 Blender
   units**; map design coords with `D2B(wx, wy) = (wx*0.01, (H-wy)*0.01)`.
3. **Import + fit + clean each blob shape.** `import_svg_as_mesh()` then
   `fit_rect()` to its target rectangle (rotate the ones the 2D layout rotated
   90°), `solidify()` for thickness, then **always `clean_mesh()`** — the SVG
   residue (duplicate verts, T-junctions, overlapping collinear edges) is
   invisible while flat but shows as tangled edges once anything is raised.
4. **Build content on the flat top:** `make_text()` for title/meta, `build_glyph()`
   for the pixel-pot, segment tiles for the strip. Color with the house
   materials from `make_materials()`.
5. **Seat everything flush** with `seat_flush()` so each object's bottom rests
   on the panel top (small sink so there's no gap) — raised elements still rise
   from there.
6. **Round tile edges** with `bevel_all()` (angle-limited bevel modifier,
   width 0.006) — same treatment for the pixel cubes and the strip tiles.
7. **Light it** with `setup_metal_lighting()` and enable ray tracing, otherwise
   the aluminium reads as flat white.

## Non-negotiables (why they matter)

- **Clean every SVG-derived mesh.** Import→convert→solidify stacks duplicate and
  T-junction geometry. Skipping cleanup looks fine until you raise/bevel a tile,
  then you get crisscrossing edges. `clean_mesh()` does merge-by-distance +
  limited dissolve + T-junction dissolve.
- **Metal needs a contrasty environment.** A metallic surface mirrors its
  surroundings; on a uniformly bright world it looks like flat white plastic.
  Use a dark world + one bright softbox + `scene.eevee.use_raytracing = True`.
- **Text must be fully matte** (specular 0, roughness 1). Otherwise, viewed
  head-on, the specular highlight bounces the light straight back and the color
  washes out to near-white — fine from the side, wrong from above.
- **Respect existing transforms.** When editing a scene the user has arranged,
  never delete-and-rebuild an object to change it (that resets position) and
  never auto-recenter. Edit mesh data in place; change only what was asked.
- **Verify by rendering.** Render from a relevant angle and look. For metal,
  render with a dark backdrop; for color/edges, a brighter close-up.

See `references/design-tokens.md` for exact values and `build_panel.py` for the
implementation of each step above.
