---
name: macos-app-icon
description: Turn any image (photo, logo, screenshot) into a correctly-shaped macOS app icon and .icns file. Use whenever the user asks to make an image into a Mac/macOS app icon, a Finder or Dock icon, an .icns, or to "round the corners like an app icon". Also handles the iOS variant on request.
---

# macOS app icon

Converts an arbitrary image into an icon that sits correctly next to system
icons in Finder and the Dock, plus a multi-resolution `.icns`.

## Run it

```bash
python3 "$HOME/.claude/skills/macos-app-icon [Turn any image into a macOS app icon + .icns]/scripts/make_icon.py" <image>
```

Writes `<name>-macos-1024.png` and `<name>.icns` next to the source. Flags:
`-o/--outdir`, `-n/--name`, `-p/--platform {macos,ios}`, `--no-recentre`.

Needs Pillow + numpy (present on this machine) and `iconutil` (ships with macOS).

Afterwards, show the result to the user — read the PNG back, or render it beside
a system icon (see Verify) — then send the files and give the install steps.

## The geometry, and why it matters

These numbers were measured, not guessed: the alpha channel of a real system
icon (`/System/Applications/Stickies.app/.../AppIcon.icns`) was extracted with
`iconutil -c iconset` and its corner profile least-squares fit.

| Property | macOS | iOS |
|---|---|---|
| Canvas | 1024 | 1024 |
| Tile | **824** centred, transparent margin | full-bleed 1024 |
| Corner curve | **circular (n = 2)** | superellipse n = 5 |
| Corner radius | **0.225 x tile** | — (full-tile squircle) |
| Shadow | soft, y+10, blur 18, black @ 35% | none |

### The edge rim light (on by default)

Native macOS icons carry a bright inner border, strongest at the **top-left and
bottom-right**. `rim_light()` reproduces it and runs by default; `--no-rim`
disables it. Measured off Podcasts.app and Freeform.app, as blend-alpha toward
white by outward normal angle (225deg = top-left corner):

| phi | 0 | 45 | 90 | 135 | 180 | 225 | 270 | 315 |
|---|---|---|---|---|---|---|---|---|
| Apple | 0.29 | 0.47 | 0.28 | 0.12 | 0.44 | **0.65** | 0.42 | 0.16 |
| ours | 0.25 | 0.48 | 0.25 | 0.19 | 0.39 | **0.70** | 0.39 | 0.19 |

Three things here are easy to get wrong:

- It is **two-lobed** along the TL-BR diagonal, plus a weaker single top-left
  bias. A one-directional highlight leaves bottom-right flat; a pure diagonal
  makes top and left too dim. Both terms are needed.
- It is a blend **toward white**, not a brightness lift — saturation falls at
  the rim (Podcasts TL: 0.59 fill -> 0.25 rim). This is why an already-white
  icon shows almost no rim, which the model reproduces for free.
- The three amplitudes were **solved numerically** against re-measured output,
  not taken from the raw fit; boundary sampling attenuates edges and corner arcs
  differently. Re-solve if you change `width` or `falloff`.

**macOS does not use the iOS squircle.** The fit came out n = 2.02, r/w = 0.220,
rmse 0.5px — a plain rounded rect. Applying an n=5 superellipse is the failure
mode to avoid: it reads visibly square next to system icons, and *raising the
radius does not fix it* because the squareness lives in the curve, not the size.

Second failure mode: full-bleed. macOS icons are inset to the 824 grid with a
transparent margin. A full-bleed 1024 square overflows its neighbours in Finder.

## Framing

The script finds the artwork by sampling the background from the border strips
and taking everything unlike it, so it works on light and dark sources alike,
then centres the square crop on it. `--no-recentre` gives a plain centre crop.

`-z/--zoom FRAC` crops in until the artwork fills FRAC of the tile (0.70 is a
good default). **Check whether the source has wide margins** — they stack on top
of the 824 inset and leave the subject tiny in the Dock. Always render the
comparison below and look before deciding; if the subject is visibly lighter
than the system icon's, rebuild with `-z 0.70`.

`--pixel` upscales with nearest-neighbour instead of Lanczos. Use it for any
pixel art — Lanczos smears the hard edges, which is the entire point of the
artwork. Check the source for this too; it is easy to miss on a small preview.

The script never scales the subject down on its own. If artwork crowds the
corners, offer to inset it rather than doing it unasked.

## Verify before delivering

Render the result beside a real system icon at the same size and look at it.
Do not trust the numbers alone:

```bash
python3 -c "
from PIL import Image
a=Image.open('OUT.png').resize((256,256),Image.LANCZOS)
b=Image.open('/System/Applications/Stickies.app/Contents/Resources/AppIcon.icns').convert('RGBA').resize((256,256),Image.LANCZOS)
c=Image.new('RGBA',(560,296),(245,245,247,255))
c.alpha_composite(a,(20,20)); c.alpha_composite(b,(296,20))
c.convert('RGB').save('cmp.png')"
```

Corner curvature and overall footprint should match.

## Folder icons

`scripts/make_folder_icon.py` builds folder icons in the user's established
style: **Apple's real folder shape recoloured near-black, with a glyph centred
on the front panel. No sheet, no extra layers — this is settled; see below.**

```bash
python3 ".../scripts/make_folder_icon.py" <glyph> -n <name> -o <outdir> --apply ~/path/to/folder
```

`<glyph>` is an .icns (artwork is lifted off its tile) or any image. Options:
`--base "#RRGGBB"` folder colour, `--area` glyph coverage (default 0.34),
`--with-sheet` adds a grey paper strip — **do not use it unprompted**: the user
iterated on the sheet three times and then rejected it outright ("Es klappt
einfach nicht"). The plain black folder + glyph is the canonical look.

What the script already handles (don't redo these by hand):
- Recolours by remapping luminance, not flat-filling, so the tab edge and
  panel shading survive.
- Lifting a glyph from an app tile insets past Apple's rim light (else it
  ghosts as a rounded rectangle) and keys with a ramp (else the edges alias).
- Glyphs are scaled by ink coverage, not longest edge, so a set of folders
  reads as siblings.
- Speck removal drops key artefacts under 2% of the largest blob.

Glyph preparation that stays outside the script:
- Line art meant to show on the black folder must be light — invert dark
  artwork (255 - RGB, keep alpha, AA survives).
- Lifting a logo off a flat background: flood the background colour from the
  border. A plain colour-distance key deletes interior details that match the
  background (a white letter on a red tile vanishes and the folder shows
  through). Enclosed regions must survive.

Folder icons are NOT in restore-icons.sh — folders don't get replaced by
updates. Library home: `resources/app-icons/folders/` (+ glyphs in `sources/`).

## Installing it

Select the PNG in Finder, Cmd-C, Get Info on the .app, click the small icon
top-left, Cmd-V. Tell the user an app auto-update will overwrite it.

Applying it directly, when the session has App Management permission:

```python
from AppKit import NSWorkspace, NSImage
img = NSImage.alloc().initWithContentsOfFile_(icns)
NSWorkspace.sharedWorkspace().setIcon_forFile_options_(img, app_path, 0)
```

Two distinct failure modes, worth telling apart before reporting:

- `Operation not permitted` -> macOS **App Management** (TCC). Since Sonoma,
  modifying another app's bundle needs that entitlement. The user grants it in
  System Settings > Privacy & Security > App Management for whichever app runs
  the session. Not something to work around.
- `Permission denied` -> plain Unix ownership; the bundle is `root:wheel`
  (Microsoft apps, installer-delivered apps). Needs an admin password, so hand
  it to the user via the Finder Get Info route, which prompts properly.

## Always refresh the Dock afterwards

**Do this without being asked** — the Dock keeps showing the old icon otherwise,
and the user should never have to drag the app out of the Dock and back in.

```bash
"$HOME/.claude/skills/macos-app-icon [Turn any image into a macOS app icon + .icns]/scripts/refresh_dock.sh" /Applications/Foo.app
```

`killall Dock` alone does not work. IconServices caches the *rendered* icon per
app, keyed off bundle mtime, and the Dock reads that cache — so the stale icon
survives a Dock restart. The script bumps the bundle's mtime, re-registers it
with `lsregister -f`, kills `iconservicesagent`/`iconservicesd`, deletes the
per-user `com.apple.iconservices*` caches, then restarts Dock and Finder. No
sudo required.

For an Xcode target use the `.icns`, or for iOS the `-ios-square-1024.png` —
`AppIcon` assets reject alpha, and iOS applies its own mask.
