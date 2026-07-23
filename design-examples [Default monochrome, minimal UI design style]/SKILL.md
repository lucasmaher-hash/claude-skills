---
name: design-examples
description: Use this skill EVERY time the user asks to create, design, build, generate, mock up, or sketch any UI, interface, screen, layout, dashboard, app, mobile view, component, page, widget, or visual composition — in Figma, in code (HTML/CSS/React), or anywhere else. The skill contains reference screenshots showing the user's preferred visual style (monochrome, minimal, technical) so every design output matches that aesthetic. Trigger keywords include "design", "create a UI", "build a screen", "mock up", "Figma file", "page", "dashboard", "component", "layout", "interface".
---

# design-examples

Reference aesthetic for every design created for this user. **Look at the screenshots in `examples/` before producing any design output** — match their style.

## Workflow (mandatory)

1. **Before** writing any design code (Figma `use_figma`, HTML/CSS, React, SVG, etc.), read at least one example from `examples/` that matches the task type:
   - Mobile screen → `02-equaliser-mobile.webp`
   - Data dashboard / desktop layout → `03-setio-dashboard.webp`
   - Technical/data-visualization/HUD → `01-radar-hud.jpg`
   - Soft UI / widget / control panel → `04-neumorphic-player.webp`
2. If the task type is ambiguous, read **two** examples.
3. Apply the style principles below.
4. Briefly note in your response which example(s) you referenced.

The examples are in `examples/` inside this skill folder. Use the Read tool on each `.webp`/`.jpg` to view it — they render as images.

## Core style principles (shared across all examples)

- **Palette: monochrome only.** Off-white / light-gray backgrounds (`#EEEEEE`–`#F5F5F5`), near-black text, mid-gray accents. No saturated color. Pure black reserved for high-emphasis interactive elements (selected pills, primary CTAs).
- **Typography is the hero.** Oversized numerals or display text dominate the composition. Smaller supporting text uses monospace or condensed sans-serif. Letter spacing is generous on labels (UPPERCASE TRACKING).
- **Generous negative space.** Compositions breathe. Whitespace is structural, not filler.
- **Technical / industrial vocabulary.** Use labels like `STL`, `ALR`, `trk.01`, `pro_sec_04`, `CORE METRICS`, `RUN IN CONTROL`. Codenames, prefixes, abbreviations. Looks like instrumentation, not marketing.
- **Thin lines, precise geometry.** 1px strokes, dotted/dashed arcs, tick marks, crosshairs. Lines often communicate more than fills.
- **Numeric data is decorative.** Show stats, timecodes, coordinates, frequencies even when not functional — they reinforce the technical mood.
- **No drop shadows by default** — except in neumorphic contexts (soft UI), where shadows are dual (light top-left, dark bottom-right) and very subtle.
- **No gradients, no glassmorphism, no glow effects, no rounded image corners over ~16px** (except neumorphic widgets where rounded ≥24px is the whole point).

## Style modes (pick one per design)

### Mode A — Technical / HUD (see `01-radar-hud.jpg`)
- Light-gray background.
- Thin black lines forming arcs, crosshairs, tick scales.
- Small bracketed labels (`[ S ]`, `trk.03`, `F/A-18`) scattered as data points.
- Top-corner readouts: `LF 7.2 / STL 275 / 153° / 32`.
- Bottom-edge status text: `:: Target Range Clear ::`.
- Center: a single large number in a thin-stroked rectangle.

### Mode B — Display monospace mobile (see `02-equaliser-mobile.webp`)
- White / very-light-gray app background.
- Big uppercase pixel/LCD-style title (`EQUALISER`).
- Segmented control: one pill solid black with white text, the other outline-only.
- Center: a circular/dial control with soft neumorphic depth.
- Bottom: stacked pill buttons (light gray), one solid-black wide CTA at the very bottom (`CUSTOM`).

### Mode C — Editorial data dashboard (see `03-setio-dashboard.webp`)
- Cream/off-white background.
- Massive timecode or numeric headline at the top (`01:40:29`).
- Left rail: stacked brand variants (`Setio°PX3`, `Setio°C1 Basic`).
- Center: tiny logo lockup.
- Right: a single short slogan in caps (`RUN IN CONTROL.`).
- Lower half: tiny bar chart (sparkline) + thin horizontal data bars + a row of metric numbers with micro-labels.

### Mode D — Neumorphic soft UI (see `04-neumorphic-player.webp`)
- Light gray background (`~#E0E0E0`).
- Heavily rounded rectangles (28–40px radius).
- Dual soft shadows: highlight top-left, shadow bottom-right.
- Inset "carved-out" wells for displays; raised "extruded" surfaces for buttons.
- Minimal black ink for labels and icons only.
- Small chip/badge accents (e.g. `FAV` pill).

## Hard rules

- **No emoji in designs.**
- **No stock-photo gradients or AI-illustrated backgrounds.**
- **No Material Design / iOS default-blue accents.** If you find yourself reaching for `#007AFF` or `#6200EE`, stop.
- **Default font stack:** Inter (regular + medium weights) or a monospace (JetBrains Mono, IBM Plex Mono). For Figma, "Inter" is always safe. Avoid Roboto, SF Pro Display, Poppins.
- **Container backgrounds: `#F2F2F2` to `#FAFAFA`.** Never pure white unless the example shows it.
- **Text fill:** `#111111`–`#1A1A1A` for primary, `#9A9A9A`–`#B0B0B0` for secondary/tertiary.

## When to ask the user

If the task could fit multiple modes (e.g. "make me a music player" — Mode B or Mode D both work), ask which one fits, showing the example filenames as options.
