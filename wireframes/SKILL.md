---
name: wireframes
description: Create or revise wireframes and wireflows in Lucas's preferred white-and-gray style, with real content, accent-colored element-edge highlights and S-curve action-to-result connectors. Use whenever Lucas asks for wireframes, Wireframes, wireflows, or Drahtmodelle.
---

# Wireframes

Use this construction for Lucas's wireframe requests, unless his current brief explicitly changes it. The reference is a readable, middle-detail interface in white and gray with restrained accent annotations. For a workflow, connect actual controls to the resulting element on the next screen.

## Establish the flow

Read the current product implementation, supplied recording, or screen references before drawing. Identify each real action and the resulting state. Preserve the same example content across states so the reader can follow one task or object. Do not invent a historical design process, research finding, app capability, or benchmark.

Use concrete labels and realistic content instead of skeleton text bars. Match the product's hierarchy and navigation; omit decorative details that do not explain the action. Keep the phone proportions and chrome consistent across all steps.

## Visual construction

- White interface surfaces; pale gray groups, rows and navigation; dark gray text and simple dark phone outlines. No product-material effects, colored marketing backgrounds, or elaborate shadows inside these explanatory screens.
- Choose an accent from the product/page's content or existing palette. Adjust its shade if necessary to contrast with the gray/white surfaces (aim for at least 3:1 for meaningful boundaries). Blue-gray is the to.morrow example, not a universal color rule.
- Highlight only the controls currently clicked, dragged or otherwise operated. The accent stroke **replaces the element's actual outer border** and follows its existing shape and corner radius. Never draw a loose oval around a rectangular card. A circular completion control uses its own circular edge.
- Use the same stroke weight for active edges and connector shafts, approximately 130% of the prior annotation stroke; the to.morrow reference uses 1.95 CSS px from a 1.5 px baseline. Keep visible stroke weight consistent when SVGs scale, e.g. with `vector-effect="non-scaling-stroke"`.
- Remove the bottom swipe/home-indicator bar. Lower the app navigation slightly and extend its gray background to the bottom of the rounded screen. Clip that fill to the screen's rounded interior so it cannot cover the bezel.
- Remove extra utility controls that distract from the demonstrated flow, such as an unrelated Add task field.

## Action-to-result connectors

Connect the relevant element on one screen to the relevant element on the next, rather than placing a generic arrow in the gap between phones. Start and end at real element boundaries. Leave a small clearance for the arrowhead.

Use a smooth S-shaped cubic Bézier. The endpoint tangent should enter the destination cleanly, without crossing its label. Route around unrelated content, with enough horizontal space between phones. Do not force every screen to have an outlined result: highlight active controls; an intermediate passive display may remain gray.

A useful rightward connection is:

```text
M x1 y1 C (x1 + reach) y1, (x2 - reach) y2, x2 y2
```

Choose reach for the geometry; use waypoint curves when that simple shape would collide with content. Anchor endpoints to the actual SVG/DOM element boxes and recompute on layout/font/language changes. Keep connectors in the same horizontally scrolling coordinate space as the screens.

When the story is a drag between lists, let the dragged card visibly escape the source phone. Remove nested clipping on that card only, retain its whole accent border and label, and reserve room before the following screen. Do not add an extra detached gesture arrow underneath it. Connect that card directly to its destination. For Undo, connect the actual Undo control to the restored card.

## Responsive layout

On desktop, fit the whole sequence statically into the available content width. Use equal fluid columns and consistent proportional gaps; do not impose a phone/track minimum width that creates horizontal scrolling. Keep deliberate card overflow inside the gap to the next screen. Enable horizontal scrolling only at the mobile breakpoint.

### Mobile

Use a horizontally scrolling strip reaching the container's left and right edges; avoid stationary pale gutters that mask passing content. Preserve comfortable initial and final scroll padding. Allow keyboard access to the scroll region.

Put short step labels above the screens on mobile. Keep their height consistent so screen tops line up. Drop redundant introductory sentences and subordinate notes when the labels and graphics already explain the flow. Use compact phones that actually reduce the strip's layout height; reduce the rendered/grid dimensions rather than applying a transform that leaves the old whitespace. The to.morrow Live example reduces a 220 px phone to 176 px (20%). Adapt dimensions to the current brief instead of making every future phone the same size.

## Check before delivery

Inspect each screen and the complete connected flow. Confirm that labels agree with the pictured state, no arrow or dragged object is accidentally cropped, highlighted borders belong to the controls, and bottom navigation has no white gap. Check narrow and wide layouts, both ends of horizontal scroll, and any supported language changes. Distinguish an actual browser check from source-only or isolated SVG rendering.

For a recording-based task, use real frame timings and keep measured observations separate from values read from source code. Do not claim pixel identity unless a rendered comparison supports it.
