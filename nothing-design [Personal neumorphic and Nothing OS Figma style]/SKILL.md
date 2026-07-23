---
name: nothing-design
description: Build UI/website designs in Figma using Lucas's personal style — light cream neumorphic chrome (F0F0F3 background, soft dual-shadow rounded containers, hover extrudes deeper) combined with Nothing OS-style content inside (NDot/Silkscreen pixel display fonts, monochrome with sparing #FF5C00 orange accents, dot-matrix patterns, thin 1px lines, generous whitespace). TRIGGER ONLY when the user types the slash command /nothing-design OR includes one of these phrases in a UI/website/screen/component design request: "in my style", "my style", "nothing style", "use my design style", "my design system", "lucas style". Do NOT auto-trigger for generic UI requests without one of those phrases. When triggered, this skill replaces any other design defaults (including the design-examples skill).
---

# Nothing-Design Skill

You build designs in **Figma** using a hybrid aesthetic that combines two influences:

1. **Neumorphic chrome** — the containers, buttons, and surfaces. Soft cream background, dual-shadow extruded elements with rounded corners. Hover deepens the shadow so the element appears to lift further off the surface.
2. **Nothing OS-style content** — the typography, icons, and decorative elements *inside* those containers. Pixel display fonts, monochrome palette, vivid orange accents used sparingly, dot-matrix patterns, thin lines, generous whitespace.

Always combine the two: neumorphic shells holding Nothing-style content.

## Mandatory first steps when this skill triggers

1. **Look at the reference images first.** Read `references/INDEX.md` to see what each image shows, then `Read` 3–5 images covering: at least one chrome spec (IMG_3647 or IMG_3644), at least one pure Nothing content screen (IMG_3621 or IMG_3636), at least one hybrid composition (IMG_3642 or IMG_3646), and the GIFs if hover/press behavior matters. References are ground truth — written specs cannot fully replace seeing them.

2. **Load the design tokens** by reading `design-tokens.md` — exact hex values, shadow recipes, font stack, spacing scale.

3. **Load the workflow guide** by reading `figma-workflow.md` — how to chain with the `figma-use` and `figma-generate-design` skills, what variables to set up first, in what order to build.

4. **Load component recipes** by reading `component-recipes.md` — copy-pasteable Figma recipes for buttons, cards, toggles, dot-matrix blocks, headings, pill buttons.

## Hard rules — do not violate

- **Background is always `#F0F0F3`** (cream / very-light-cool-gray). Never pure white #FFFFFF as the page background.
- **Every interactive container gets the dual shadow** (one light from top-left, one dark from bottom-right). Flat rectangles are forbidden for buttons/cards.
- **Hover state = deeper shadow + slight lift**, never a color change or border. Build hover as a separate variant in Figma component sets.
- **Three fonts only**: `OCR-A BT Regular` (display — monospaced OCR typeface for page titles and hero headings, **original/mixed case**, locally installed — not in Figma's built-in fonts), `VT323` (pixel/terminal — UPPERCASE small labels, metadata, button text), `Roboto` (body — paragraphs, default UI text). `VT323` and `Roboto` are bundled in `fonts/`. **Never** use Plaster (deprecated), Courier Prime (deprecated), Inter, Helvetica, SF Pro, or any other typeface.
- **Orange `#FF5C00` is an accent only** — use for at most 1–2 elements per screen (a single dot, a single underline, a single key number). Never as a button fill, never as a large block of color.
- **Monochrome otherwise** — blacks, whites, grays, the cream background. No other colors.
- **All caps + tight tracking** for short labels and headings; sentence case OK for longer body copy.
- **Generous whitespace** — minimum 24px padding inside containers, 32–48px between sections. Never cramped.
- **Dot-matrix decoration** — use for data viz, dividers, status indicators, and as ambient pattern fill. It's a signature Nothing element.
- **Thin 1px lines** as dividers, never thicker. Color: `#1A1A1A` at 100% or `#8E8E93`.

## Output

All designs go into **Figma** via the `figma-use` toolchain. Never produce HTML, React, or static images unless the user explicitly overrides.

Before writing any Figma code:
- Invoke the `figma-use` skill (mandatory prerequisite for `use_figma` calls).
- If creating a new file, invoke `figma-create-new-file` first.
- Read `figma-workflow.md` in this skill for the build order specific to this aesthetic.

Build incrementally section-by-section, set up local variables for all design tokens before placing any visual elements, and verify after each major section by taking a screenshot via the figma MCP.

## What this skill replaces

When this skill is triggered, it overrides the generic `design-examples` skill. Use these tokens, these components, this aesthetic — not the generic monochrome-minimal style.
