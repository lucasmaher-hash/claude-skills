# Figma Workflow — Nothing-Design

How to actually build a design in Figma using this skill, end to end. The output target is **always Figma** via the figma MCP toolchain.

## Prerequisites — skills to chain

This skill *describes the aesthetic*. The Figma plugin toolchain *executes the writes*. You must load both:

| Use case | Load these skills in addition to nothing-design |
|---|---|
| Creating a brand new Figma file | `figma:figma-create-new-file`, then `figma:figma-use` |
| Building components / variables in an existing file | `figma:figma-use`, optionally `figma:figma-generate-library` |
| Building a full screen / page composition | `figma:figma-use`, `figma:figma-generate-design` |
| Building a FigJam diagram (rare for UI work) | `figma:figma-use-figjam` |

**Mandatory order**: load the prerequisite skill *before* the corresponding MCP tool call. Skipping `figma-use` before `use_figma` causes hard-to-debug failures.

## Build order — always this sequence

Do not skip steps and do not reorder. Each step depends on the prior one being in place.

### Step 1 — Confirm the target Figma file
- If user has an existing file: ask for the file URL or confirm the one currently open in the figma MCP.
- If not: run `figma-create-new-file` (load that skill first) with editorType=`design` and a sensible file name (e.g., `Nothing Design — {project}`).

### Step 2 — Set up local variables (design tokens)

Before any visual element exists, create the variables. Read `design-tokens.md` and create:

1. **Color variables** — one collection called `nothing/colors`, with all 9 tokens from the palette table.
2. **Number variables** — one collection called `nothing/spacing`, with the 9 spacing tokens (4–96). And one called `nothing/radius` with the 5 radius tokens.
3. **Text styles** — for each row in the type scale table (display/xl … body/sm), create a Figma text style with the specified font, size, weight, letter-spacing, and case.
4. **Effect styles** — create the 5 shadow recipes (raised, raised-sm, raised-lg, hover, pressed) as effect styles.

All subsequent layers must reference these variables/styles, never raw values. If you find yourself typing `#F0F0F3` into a fill picker, stop and bind the variable instead.

### Step 3 — Build the component library

Read `component-recipes.md`. Build these as Figma components on a dedicated page called `Library`, in this order:

1. Neumorphic Card (with all state variants)
2. Neumorphic Button + Pill Button
3. Black Pill + Outlined Pill
4. Toggle / Switch
5. Search Bar
6. Pixel Heading (just a text style + adjacent dot pattern, not a full component)
7. Dot-Matrix Block
8. Thin Divider
9. Orange Accent Dot
10. Section Header

Use Figma's variant feature for state matrices (default/hover/pressed). Set sensible defaults.

### Step 4 — Assemble screens

Now build the actual screens the user asked for, on a page called `Screens`. Compose using the components you just built. Follow the spacing scale rigorously.

For each screen:
1. Frame at standard device size (390×844 for mobile, 1440×900 for desktop, 1280×800 for laptop landing).
2. Fill: `bg/surface`.
3. Apply page outer padding per `design-tokens.md` spacing rules.
4. Drop in section-by-section: title block → content cards → CTA.
5. After each major section, take a screenshot via the Figma MCP to verify it matches the references.

### Step 5 — Verify against references

After the screen looks complete, do a side-by-side mental comparison with the most relevant reference image(s):
- Is the background `#F0F0F3`, not white?
- Do all containers have the dual neumorphic shadow?
- Is the display heading in OCR-A BT Regular (mixed case, -4% tracking)? Are small labels in VT323 (UPPERCASE)?
- Is there at most one orange accent?
- Is whitespace generous (not cramped)?
- Is there at least one dot-matrix element or thin-line divider as a Nothing signature?

If any answer is no, fix before declaring done.

## Common pitfalls

### Pitfall 1: hardcoded colors
You skipped Step 2 and went straight to placing rectangles. Every fix later requires hand-editing every layer. **Always set up variables first.**

### Pitfall 2: card on wrong background
You placed a neumorphic card on a white frame. The shadow appears wrong because neumorphism requires `container_fill == page_fill`. Both must be `#F0F0F3`.

### Pitfall 3: hover variant missing
You built a button with one variant. The hover-extrude behavior is the *defining feature* of this style — always add the hover variant with `shadow/hover`.

### Pitfall 4: too many orange accents
You added orange to a button, an icon, and a number on the same screen. Result: orange becomes wallpaper, no longer an accent. **Max one or two per screen.**

### Pitfall 5: wrong font slipped in
You used "Inter" or "Courier Prime" because the right font wasn't loaded. The three fonts are: `OCR-A BT Regular` (display — locally installed, NOT in Figma's built-in fonts, `listAvailableFontsAsync()` returns nothing for it), `VT323` and `Roboto` (bundled in `~/.claude/skills/nothing-design/fonts/`). Display headings = OCR-A BT Regular in **original/mixed case**, -4% tracking. Pixel labels and button text = VT323 in UPPERCASE. Body = Roboto. Nothing else. Plaster and Courier Prime are both deprecated — do not use even if you find them in the file. Because OCR-A BT is local-only, plugin `loadFontAsync` will fail — apply the font via Figma desktop app if needed.

### Pitfall 6: built without seeing the references
Specs don't capture the *feel*. Always Read at least 3 reference images at the start of the work so you have visual ground truth.

## Working incrementally

For any non-trivial screen, work in chunks. After each chunk:
- Save the file (Figma autosaves but be explicit).
- Take a screenshot.
- If it doesn't match the reference vibe, course-correct before adding more.

Better to ship one polished screen than three sloppy ones.
