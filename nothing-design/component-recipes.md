# Component Recipes — Nothing-Design

Each recipe describes the structure, layers, and tokens for a component. Build these as Figma components with proper variant sets so you can reuse them across screens.

---

## 1. Neumorphic Card (default container)

The bread-and-butter shell that holds content.

```
Frame "Card"
├── Fill: bg/surface (#F0F0F3)
├── Corner radius: radius/lg (24px)
├── Effect: shadow/raised
├── Auto-layout: vertical, padding space/5 (24px), gap space/4 (16px)
└── [content children]
```

### Variants
- **State**: `default` (shadow/raised) | `hover` (shadow/hover) | `pressed` (shadow/pressed)
- **Size**: `sm` (radius/md, padding space/4) | `md` (default) | `lg` (radius/xl, padding space/6)

---

## 2. Neumorphic Button (rectangular)

```
Frame "Button"
├── Fill: bg/surface (#F0F0F3)
├── Corner radius: radius/md (16px)
├── Effect: shadow/raised-sm
├── Auto-layout: horizontal, padding space/3 vertical / space/5 horizontal, gap space/2
├── Text "Label" — label/lg, UPPERCASE, color text/primary
└── [optional icon, left or right]
```

### Variants
- **State**: `default` | `hover` (shadow/hover) | `pressed` (shadow/pressed, text shifts down 1px)
- **Icon**: `none` | `left` | `right` | `only`

---

## 3. Neumorphic Pill Button (fully rounded)

The Nothing-style soft pill used for navigation tabs and secondary actions.

```
Frame "Pill"
├── Fill: bg/surface
├── Corner radius: radius/pill (9999)
├── Effect: shadow/raised-sm
├── Auto-layout: horizontal, padding space/3 vertical / space/5 horizontal
└── Text "Label" — label/lg, UPPERCASE
```

Variants: same state matrix as Button. Add an `active` variant where shadow becomes `shadow/pressed` (inset, signals selected).

---

## 4. Black Pill Button (primary CTA alternative)

The contrasting button used for primary actions (see "CUSTOM" in the Equaliser reference, IMG_3636).

```
Frame "BlackPill"
├── Fill: bg/black (#1A1A1A)
├── Corner radius: radius/pill
├── Auto-layout: horizontal, padding space/3 vertical / space/6 horizontal
└── Text — label/lg, UPPERCASE, color #FFFFFF
```

No shadow on this one — it lives flat, by design. The contrast is what makes it pop.

---

## 5. Outlined Pill Button

Secondary to the black pill (the "ADVANCED" tab in the Equaliser reference).

```
Frame "OutlinedPill"
├── Fill: none (transparent — sits on bg/surface)
├── Stroke: 1px, #1A1A1A
├── Corner radius: radius/pill
├── Auto-layout: same as BlackPill
└── Text — label/lg, UPPERCASE, color text/primary
```

---

## 6. Toggle / Switch

Reference: Nothing OS Dual Connection screen (IMG_3633.JPG).

```
Frame "Toggle" (60×32)
├── Fill: bg/black (when on) | bg/surface (when off)
├── Corner radius: radius/pill
├── Effect (off state only): shadow/pressed (inset)
└── Knob: Circle 24×24
    ├── Fill: bg/white (when on) | bg/surface (when off)
    ├── Position: right (when on) | left (when off)
    └── Effect: shadow/raised-sm
```

Variants: `on` | `off` × `default` | `hover`.

---

## 7. Segmented Toggle (two-option control)

The selector used for mutually exclusive modes (e.g. 2D / 3D). Outer pill raised, active segment inset — the selected option sinks INTO the surface.

```
Frame "SegmentedToggle" (outer pill)
├── Fill: bg/surface
├── Corner radius: radius/pill (9999)
├── Effect: shadow/raised-sm   ← outer pill is RAISED
├── Auto-layout: horizontal, padding 5px all sides, gap 4px
│
├── Frame "Segment-active" (selected option)
│   ├── Fill: bg/surface
│   ├── Corner radius: ~18px (slightly less than pill so it nests visually)
│   ├── Effect: shadow/pressed  ← active segment is INSET (sinks in)
│   ├── layoutGrow: 1 / layoutSizingVertical: FILL
│   └── Text — label/lg, UPPERCASE, color text/primary
│
└── Frame "Segment" (inactive option)
    ├── Fill: none (transparent)
    ├── No effect
    ├── layoutGrow: 1 / layoutSizingVertical: FILL
    └── Text — label/lg, UPPERCASE, color text/secondary
```

**Critical rule:** The active segment uses `shadow/pressed` (inset), NOT `shadow/raised`. A raised active segment looks wrong — it should feel pressed down, not popped up. The outer container carries the raised shadow; the inner active segment carries the pressed/sunken shadow.

Build as a component set with variants for each state (e.g. `state=2d` | `state=3d`).

---

## 8. Search Bar (Neumorphic)

Reference: IMG_3645.JPG.

```
Frame "SearchBar"
├── Fill: bg/surface
├── Corner radius: radius/pill (or radius/md for rectangular variant)
├── Effect: shadow/pressed (inset — communicates "input field")
├── Auto-layout: horizontal, padding space/3 / space/5, gap space/3
├── Text "Search..." — body/md, color text/secondary
└── Icon: search, 20px, color text/secondary (right-aligned)
```

---

## 8. Display Heading

The signature page-title element. Editorial typewriter-serif, mixed case.

```
Text "Tuesday"  (mixed case preferred; UPPERCASE only for short single-word display titles)
├── Font: Courier Prime Bold, display/lg (44px)
├── Letter-spacing: -2%
├── Line-height: 105%
├── Color: text/primary (#1A1A1A)
└── (Optional) Adjacent: small orange dot, 6×6, #FF5C00, top-right baseline-aligned
```

Use for: page titles, hero text, section headings. For pixel-style smaller display callouts (card headings, status readouts), use `display/sm` which falls back to VT323.

---

## 9. Dot Divider (heading separator)

A 1px rule with two small dots on the left and one on the right — a typographic accent placed directly below display headings.

```
Frame "DotDivider" — auto-layout VERTICAL, gap 6px, fills none, FILL width
├── Rectangle "Rule" — 1px height, FILL width, fill text/primary (#1A1A1A)
└── Frame "Dots" — auto-layout HORIZONTAL, SPACE_BETWEEN, FILL width, fills none
    ├── Frame "DotsLeft" — auto-layout HORIZONTAL, gap 5px, fills none
    │   ├── Ellipse "Dot" — 4×4, fill text/primary
    │   └── Ellipse "Dot" — 4×4, fill text/primary
    └── Ellipse "Dot" — 4×4, fill text/primary
```

Use immediately after the display heading on any screen that has a hero title. Do not repeat it elsewhere on the same screen.

---

## 10. Dot-Matrix Block (data viz)

Reference: IMG_3621.jpg (audio visualizer), IMG_3643.JPG (line chart variant).

```
Frame "DotMatrix" (e.g., 320×120)
├── Auto-layout: grid, 32 cols × 12 rows, gap 4px each direction
└── For each cell:
    └── Circle 4×4
        ├── Fill: bg/black (#1A1A1A) when "active"
        ├── Fill: text/tertiary (#C7C7CC) when "inactive"
        └── (For ambient pattern variant: all inactive, opacity reduced)
```

Build as a component with a property to swap cell states programmatically when used. For one-off charts, just place individually.

---

## 10. Thin Divider

```
Line "Divider"
├── Stroke: 1px
├── Color: text/primary (#1A1A1A) for hard dividers
├── Color: text/secondary (#8E8E93) for softer dividers
└── Width: 100% of parent
```

No 2px, no 4px, no dashed. One pixel, solid.

---

## 11. Orange Accent Dot

The hero element. Use once per screen.

```
Circle "AccentDot" (6×6 or 8×8)
├── Fill: accent/orange (#FF5C00)
└── Position: adjacent to the single most important element on the screen
```

Variants by size: `xs` (4px), `sm` (6px), `md` (8px), `lg` (12px).

---

## 12. Section Header (label + divider)

```
Frame "SectionHeader"
├── Auto-layout: vertical, gap space/2
├── Text "MY DEVICES" — label/md, UPPERCASE, color text/secondary
└── Divider (thin, optional)
```

---

## Common compositions

### Stat card (number + label)
```
Card (size: md)
├── Text "REVENUE" — label/md, color text/secondary
├── Text "+326%" — display/xl, color text/primary
│   └── (optional) AccentDot adjacent to the number
└── DotMatrix (sparkline showing the trend)
```

### Settings row
```
Frame "Row" — horizontal auto-layout, space-between, padding space/3
├── Text "IN-EAR DETECTION" — label/lg
└── Toggle (variant: on)
```

### Page scaffold (mobile)
```
Frame "Screen" (390×844)
├── clipsContent: FALSE  ← page frame
├── Fill: bg/surface
├── Padding: space/7 (48px) horizontal, space/7 top, space/6 bottom  (see shadow safe-area rule in design-tokens.md)
├── Auto-layout: vertical, gap space/6
├── Header: SectionHeader or display heading
├── ButtonsGroup (auto-layout VERTICAL, transparent fill)
│   ├── clipsContent: FALSE  ← intermediate group frame, must also be false
│   ├── PillButton instance
│   ├── PillButton instance
│   └── SegmentedToggle instance
└── (Optional) Bottom-anchored: BlackPill primary CTA
```

**Critical:** every container frame in the chain holding neumorphic elements needs `clipsContent: false` — not just the page frame. See the shadow safe-area rule in `design-tokens.md`. A single clipping ancestor anywhere in the hierarchy cuts the shadow.

For desktop, use `space/8` (64px) horizontal padding or larger. Never use `space/5` (24px) — neumorphic shadows will clip.

---

## Anti-patterns — never do these

- Drop shadow on a card with a *different* background color than the page. Neumorphism only works when card fill == page fill.
- Two different orange elements on one screen.
- Sans-serif fonts in any context.
- A button with both a neumorphic shadow AND a stroke. Pick one chrome system per element.
- Cramped padding (anything less than 16px inside a container).
- Multiple competing dot-matrix blocks on the same screen — pick one as the visual anchor.
