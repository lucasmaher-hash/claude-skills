#!/usr/bin/env python3
"""Build a macOS folder icon: real folder shape, recoloured, with a glyph on it.

Starts from Apple's own GenericFolderIcon.icns rather than redrawing a folder,
so the silhouette, tab and edge shading are exactly right at every size.

  make_folder_icon.py <glyph> -n blender [--base "#0E0E0E"] [--apply ~/path/dir]

<glyph> is either an .icns (the artwork is lifted off its tile) or any image.
"""
import argparse, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_icon import write_icns

CANVAS = 1024
GENERIC = ("/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/"
           "GenericFolderIcon.icns")


def apple_folder(size=CANVAS):
    """Apple's stock folder at 1024, as RGBA."""
    d = "/tmp/_folder_icon.iconset"
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(["iconutil", "-c", "iconset", GENERIC, "-o", d],
                   capture_output=True, check=True)
    for cand in ("icon_512x512@2x.png", "icon_256x256@2x.png"):
        p = os.path.join(d, cand)
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            return im if im.size[0] == size else im.resize((size, size), Image.LANCZOS)
    raise SystemExit("no usable rep in GenericFolderIcon.icns")


def recolour(im, base=(14, 14, 14), spread=46):
    """Recolour the folder by REMAPPING LUMINANCE, not flat-filling.

    Flat-filling destroys the tab edge, the front-panel gradient and the rim
    light, and the result stops reading as a folder. Remapping keeps all of that
    intact: `base` is the darkest point, `spread` how much lighter the brightest
    part gets. Tinting works too -- pass a coloured base.
    """
    a = np.asarray(im).astype(np.float32)
    al = a[..., 3]
    lum = (a[..., :3] * np.array([0.2126, 0.7152, 0.0722])).sum(2)
    m = al > 200
    lo, hi = np.percentile(lum[m], 3), np.percentile(lum[m], 97)
    t = np.clip((lum - lo) / max(hi - lo, 1e-6), 0, 1)[..., None]
    rgb = np.array(base, dtype=np.float32) + t * spread
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), al]).astype(np.uint8))


def front_panel_top(im):
    """Row where the folder's front panel starts (first near-full-width row)."""
    al = np.asarray(im)[..., 3] > 200
    wid = al.sum(1)
    return int(np.where(wid >= 0.97 * wid.max())[0].min())


def add_sheet(folder, gap=20, inset=0.045, radius=14,
              colour=(180, 180, 188), bevel=46):
    """The paper sheet between the folder's back and front panels.

    GEOMETRY STAYS STOCK. Earlier attempts shifted the back panel up and the
    front panel down to open a gap -- that reads as a third panel bolted on,
    and the user rejected it twice. The correct construction: leave every
    folder pixel where it is, and let the sheet peek out in the band ABOVE the
    front panel's top edge, docked so its bottom edge lands exactly on it.

    Stacking: folder -> sheet (band yf-gap..yf+slack) -> front panel re-composited
    on top, which hides the slack and clips the sheet to a crisp dock line at yf.

    The front panel's own top bevel (a light band, ~46px in the stock art) is
    flattened to the body colour first: recolouring to near-black exaggerates it
    and it reads as a gap between sheet and panel even when they touch.

    The sheet is NOT in GenericFolderIcon.icns and not in the NSWorkspace icon
    either (verified: empty, full and arbitrary folders return byte-identical
    sheetless icons). Finder draws it from an asset the icon APIs do not
    expose, so it is reconstructed here. Do not hunt for it in stock assets.
    """
    al = np.asarray(folder)[..., 3] > 200
    ys, xs = np.where(al)
    x0, x1 = int(xs.min()), int(xs.max())
    yf = front_panel_top(folder)

    a = np.asarray(folder).copy()
    a[:yf, :, 3] = 0                                  # front panel, in place
    band = int(bevel)
    if band:
        sel = a[yf + band + 10: yf + band + 40, :, :3][
              a[yf + band + 10: yf + band + 40, :, 3] > 200]
        body = np.median(sel, axis=0)
        for i in range(band):
            w = min(1.0, (band - i) / band * 1.6)
            row = a[yf + i, :, :3].astype(np.float32)
            a[yf + i, :, :3] = (row * (1 - w) + body * w).astype(np.uint8)
    front = Image.fromarray(a)

    out = folder.copy()
    pad = int((x1 - x0) * inset)
    sheet = Image.new("RGBA", folder.size, (0, 0, 0, 0))
    ImageDraw.Draw(sheet).rounded_rectangle(
        [x0 + pad, yf - gap, x1 - pad, yf + 60], radius=radius,
        fill=tuple(colour) + (255,))
    out.alpha_composite(sheet)
    out.alpha_composite(front)                        # clips the sheet at yf
    return out


def _despeck(g, keep=0.02):
    """Drop key artefacts: blobs smaller than `keep` of the largest one."""
    al = np.asarray(g)[..., 3] > 10
    comps, rem = [], al.copy()
    while rem.any():
        ys, xs = np.where(rem)
        r = np.zeros_like(al); r[ys[0], xs[0]] = True
        while True:
            n = r.copy()
            n[1:, :] |= r[:-1, :]; n[:-1, :] |= r[1:, :]
            n[:, 1:] |= r[:, :-1]; n[:, :-1] |= r[:, 1:]
            n &= al
            if n.sum() == r.sum():
                break
            r = n
        comps.append(r); rem &= ~r
    big = max(c.sum() for c in comps)
    keepm = np.zeros_like(al)
    for c in comps:
        if c.sum() >= keep * big:
            keepm |= c
    a = np.asarray(g).copy()
    a[..., 3] = np.where(keepm, a[..., 3], 0)
    ys, xs = np.where(keepm)
    return Image.fromarray(a).crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def load_glyph(path, inset=0.06):
    """Lift artwork off a dark tile, or take an image's own alpha.

    Two traps when the source is an app icon: the tile carries Apple's rim
    light, which survives a black key and reappears as a ghostly rounded
    rectangle behind the glyph -- so inset past it first. And the key must ramp,
    not threshold, or the glyph loses its antialiasing.
    """
    if path.endswith(".icns"):
        d = "/tmp/_glyph.iconset"
        shutil.rmtree(d, ignore_errors=True)
        subprocess.run(["iconutil", "-c", "iconset", path, "-o", d],
                       capture_output=True, check=True)
        src = Image.open(os.path.join(d, "icon_512x512@2x.png")).convert("RGBA")
        a = np.asarray(src).astype(np.float32)
        ys, xs = np.where(a[..., 3] > 250)
        a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    else:
        src = Image.open(path).convert("RGBA")
        a = np.asarray(src).astype(np.float32)
        if a[..., 3].min() < 250:                      # already has alpha
            return _despeck(Image.fromarray(a.astype(np.uint8)))
    k = int(min(a.shape[:2]) * inset)
    if k:
        a = a[k:-k, k:-k]
    rgb = a[..., :3]
    alpha = np.clip((rgb.max(2) - 28.0) / 70.0, 0, 1) * 255
    return _despeck(Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8)))


def compose(folder, glyph, area=0.34, cy=590, cap=470):
    """Place the glyph, scaled by COVERAGE rather than longest edge.

    Longest-edge scaling makes a tall narrow mark read much smaller than a wide
    one at the same nominal size, because the eye judges ink area. Matching
    alpha coverage keeps a set of folders looking like siblings.
    """
    f = folder.copy()
    ink = (np.asarray(glyph)[..., 3] > 10).sum()
    s = min(np.sqrt((area * CANVAS) ** 2 / max(ink, 1)), cap / max(glyph.size))
    g = glyph.resize((max(1, round(glyph.width * s)),
                      max(1, round(glyph.height * s))), Image.LANCZOS)
    f.alpha_composite(g, ((CANVAS - g.width) // 2, int(cy - g.height / 2)))
    return f


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("glyph", help=".icns or image to place on the folder")
    ap.add_argument("-o", "--outdir", default=".")
    ap.add_argument("-n", "--name", required=True)
    ap.add_argument("--base", default="#0E0E0E", help="darkest folder colour (default near-black)")
    ap.add_argument("--spread", type=float, default=46, help="internal contrast (default 46)")
    # Sheet is OFF by default: the user iterated on it three times and then
    # rejected it outright ("Es klappt einfach nicht") -- the plain black
    # folder + glyph is the canonical style. Keep the code, don't default to it.
    ap.add_argument("--with-sheet", action="store_true", help="add the grey paper sheet (off by default)")
    ap.add_argument("--gap", type=int, default=20, help="how far the sheet shows between the panels (default 46)")
    ap.add_argument("--area", type=float, default=0.34, help="glyph ink coverage (default 0.34)")
    ap.add_argument("--sheet", default="#B4B4BC", help="sheet colour (default grey)")
    ap.add_argument("--apply", default=None, help="also set this folder's icon")
    a = ap.parse_args()

    base = tuple(int(a.base.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    f = recolour(apple_folder(), base, a.spread)
    if a.with_sheet:
        f = add_sheet(f, gap=a.gap, colour=tuple(int(a.sheet.lstrip("#")[i:i+2],16) for i in (0,2,4)))
    icon = compose(f, load_glyph(a.glyph), area=a.area)

    os.makedirs(a.outdir, exist_ok=True)
    png = os.path.join(a.outdir, f"{a.name}-folder-1024.png")
    icns = os.path.join(a.outdir, f"{a.name}-folder.icns")
    icon.save(png)
    write_icns(icon, icns)
    print(png); print(icns)

    if a.apply:
        from AppKit import NSWorkspace, NSImage
        p = os.path.expanduser(a.apply)
        img = NSImage.alloc().initWithContentsOfFile_(icns)
        ok = img and NSWorkspace.sharedWorkspace().setIcon_forFile_options_(img, p, 0)
        print(("applied to " if ok else "FAILED to apply to ") + p)


if __name__ == "__main__":
    sys.exit(main())
