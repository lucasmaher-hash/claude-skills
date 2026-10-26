---
name: tuning-controls
description: Build temporary visual adjustment panels for Lucas whenever he asks for Regler, sliders, a tuner, or controls to fine-tune sizes, spacing, colors, materials or animation values. Apply these defaults when creating or revising such tuning controls; ordinary end-user app sliders are outside this scope.
---

# Tuning controls

Use this skill whenever building or revising Lucas's temporary adjustment controls. Follow his explicit changes to these defaults. Do not add a panel just because a page could be tuned.

## Panel placement and movement

- Start **fixed at the bottom right** of the viewport, with a small gutter and device safe-area clearance. Keep it above the content it controls, while respecting existing menus and dialogs.
- The panel must be **freely draggable** to another position. Make the title bar and unused panel surface grabbable; show a grab/grabbing cursor. Do not start panel movement from sliders, number fields, color pickers or buttons.
- Use Pointer Events with pointer capture so mouse, pen and touch movement remain attached to the grab point. Preserve the initial pointer offset. Apply `touch-action: none` to the drag surface, not the entire page or the form controls.
- Keep the panel header reachable: constrain movement to viewport bounds and re-clamp after resizing or orientation changes. Size the panel to fit narrow screens and scroll its contents when needed.
- Persist its position within the current project's tuner state when practical. If there is no saved position, use bottom right. Do not permanently replace the default with an off-screen saved coordinate.

## Collapse is mandatory

- Provide a clearly labelled collapse/expand button in the header. Collapse hides the controls while keeping the draggable title bar and expand button visible.
- Keep the panel's position when collapsing or expanding. Respect viewport bounds when the expanded body needs more space.
- Use a real keyboard-operable button with `aria-expanded` and `aria-controls`. Give each field a visible label and retain native keyboard slider behavior.

## Generous ranges

Lucas explicitly wants a **wider range than the implementer initially thinks necessary**. Narrow ranges have repeatedly stopped him from reaching the desired look.

- Choose a normal starting value independently of the exploration bounds. Do not center a tiny range around the current setting.
- For multiplicative visual adjustments, consider roughly **0.25×–4× the current value** as a starting range, and widen further when the property permits. This is an example, not a cap. Darkness or effect intensity may need **0–400% or more**; genuine bounded quantities such as opacity still stay within their valid domain.
- Allow zero/off when meaningful and negative values when the property supports them, such as offsets, rotation or tracking. Do not allow invalid dimensions or other values the underlying feature cannot use.
- Pair sliders with an editable numeric value and visible unit so Lucas can enter a valid value beyond the initial slider bounds. Expand the slider bounds to include it rather than silently clamping it to the old range. Use sensible fine steps near the working values.
- Keep visually independent properties independent: changing paper tint should not change ink darkness; changing width should not secretly change an unrelated gap. Show any intentional coupling.

## Settings and handoff

- Apply changes live to the intended element. Keep originals intact; use reversible presentation settings for image/material tuning where possible.
- Save the values locally under a project/component-specific key, validate restored values, and provide Reset. Keep panel position/collapse state separate from the actual appearance settings.
- Display the current settings in a selectable/copyable structured block, including units and exact color values. This lets Lucas send the chosen values back without estimating slider positions.
- Treat these as temporary authoring controls. Make their availability explicit, such as localhost or a preview query parameter, unless Lucas asks for them on the normal public page. Do not make a public result depend on settings held only in one browser.
- When Lucas approves values and asks to remove the controls, save the exact settings as the page/component defaults. Preserve effective tint/color calculations. Remove the temporary panel, scripts, styles and unused translation keys, then verify the approved appearance still works without localStorage.

## Check before handing over

Verify the meaningful behaviors: default bottom-right position; dragging from the grab surface on desktop and touch; controls do not drag the panel; collapsed panel can be moved and reopened; resize/orientation does not strand it off screen; wide ranges and numeric input work; exported settings and Reset are accurate. Describe source-only checks honestly if a rendered interaction check is unavailable.
