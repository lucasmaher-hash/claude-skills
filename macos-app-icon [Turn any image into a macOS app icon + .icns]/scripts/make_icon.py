#!/usr/bin/env python3
"""Turn any image into a macOS (or iOS) app icon.

macOS geometry was derived by fitting the alpha channel of a real system icon
(Stickies.app): the corner is a CIRCULAR arc at r = 0.225 x tile width, not the
iOS squircle. Fit was n = 2.02, r/w = 0.220, rmse 0.5px. Using a superellipse
here is the classic mistake -- it reads visibly square next to system icons.

  macOS : 824x824 tile centred on a 1024 canvas, transparent margin, soft shadow
  iOS   : full-bleed 1024 square, superellipse n=5 corners, no shadow
"""
import argparse, os, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

CANVAS = 1024
MAC_TILE = 824          # Apple's macOS icon grid
MAC_RADIUS = 0.225      # circular corner, fraction of tile width
MAC_CORNER_N = 2.0      # 2.0 == circular. Do not raise this for macOS.
IOS_CORNER_N = 5.0      # iOS squircle
IOS_RADIUS = 0.50       # full superellipse spanning the tile
SS = 4                  # supersample factor for mask antialiasing

ICNS_SIZES = [(16, "16x16"), (32, "16x16@2x"), (32, "32x32"), (64, "32x32@2x"),
              (128, "128x128"), (256, "128x128@2x"), (256, "256x256"),
              (512, "256x256@2x"), (512, "512x512"), (1024, "512x512@2x")]


def corner_mask(size, rr, n, ss=SS):
    """Rounded rect with straight edges and superelliptical corners.

    rr is the corner radius as a fraction of the width; n=2 gives a circular
    corner, higher n squares it off. rr=0.5 with n=5 degenerates to the iOS
    full-tile squircle.
    """
    p = size * ss
    r = rr * p
    ax = np.arange(p) + 0.5
    d = np.maximum(np.maximum(r - ax, ax - (p - r)), 0)
    DX, DY = np.meshgrid(d, d)
    inside = (DX / r) ** n + (DY / r) ** n <= 1.0
    return Image.fromarray((inside * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)


def content_bbox(im):
    """Bounding box of the artwork, whatever the background.

    Background is sampled from the four border strips, then anything far enough
    from that colour counts as content. Do NOT key off brightness alone -- that
    finds the subject on a dark background but selects the whole canvas on a
    light one, which silently disables recentring and zooming.
    """
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    h, w = a.shape[:2]
    e = max(2, min(h, w) // 64)
    border = np.concatenate([a[:e].reshape(-1, 3), a[-e:].reshape(-1, 3),
                             a[:, :e].reshape(-1, 3), a[:, -e:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    dist = np.linalg.norm(a - bg, axis=2)
    ys, xs = np.where(dist > max(30.0, dist.max() * 0.15))
    if not len(xs):
        return 0, 0, w, h
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def square_crop(im, recentre=True, zoom=None):
    """Largest square containing the artwork, centred on it.

    zoom, if given, is the fraction of the square the artwork should fill --
    e.g. 0.72 crops in until the subject occupies 72% of the tile. Useful when
    the source has wide margins that would otherwise stack on top of the 824
    inset and leave the subject tiny in the Dock.
    """
    w, h = im.size
    cx, cy = w / 2, h / 2
    side = min(w, h)

    if recentre or zoom:
        x0, y0, x1, y1 = content_bbox(im)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if zoom:
            side = min(max(x1 - x0, y1 - y0) / zoom, min(w, h))

    half = side / 2
    cx = min(max(cx, half), w - half)
    cy = min(max(cy, half), h - half)
    x, y = round(cx - half), round(cy - half)
    return im.crop((x, y, x + round(side), y + round(side)))


def rim_light(tile, rr, mean=0.409, lobe2=0.209, lobe1=0.115,
              width=0.018, falloff=1.6):
    """Apple's edge rim: a bright inner border, strongest top-left and bottom-right.

    Measured off Podcasts.app and Freeform.app rather than guessed, then fit.
    Expressed as blend-alpha toward white, by outward normal angle phi
    (x right, y down, so 225deg is the top-left corner):

        phi    0     45    90    135   180   225   270   315
        Apple  0.29  0.47  0.28  0.12  0.44  0.65  0.42  0.16
        model  0.29  0.47  0.29  0.14  0.42  0.66  0.42  0.14

    A(phi) = mean + lobe2*cos(2*(phi - 45deg)) + lobe1*cos(phi - 225deg)
    least-squares fit, rmse 0.013 over all eight positions.

    TWO terms are needed and both matter. The lobe2 term is the TL/BR diagonal
    the eye actually notices. The lobe1 term is a weaker single top-left bias --
    without it, top and left come out too dim and bottom-right too hot, because
    a pure diagonal model is symmetric about the centre and Apple's is not.

    Saturation FALLS at the rim (Podcasts TL: 0.59 fill -> 0.25 rim), so this is
    an alpha blend toward white, not a brightness or value boost. That also
    explains why an already-white icon (Reminders) shows almost no rim: there is
    nothing left to lighten, and the model reproduces that for free.

    The inward profile decays to nothing by ~1.8% of the tile width
    (69/42/21/3 at tile 204), matching (1 - d/w)**1.6.

    The defaults are NOT the raw fit -- they were solved numerically so that
    re-measuring our own output with the same procedure reproduces Apple's
    numbers (rmse 0.044, worst position 0.07, inside the 0.16 spread between
    Apple's own icons). Sampling the boundary pixel lands slightly inside the
    edge and the attenuation differs between straight edges and corner arcs, so
    scaling the raw fit by one constant overshoots the corners. If you change
    width or falloff, re-solve rather than hand-adjusting these three.
    """
    W = tile.size[0]
    r = rr * W
    a = np.asarray(tile.convert("RGB")).astype(np.float32)

    ax = np.arange(W) + 0.5 - W / 2
    PX, PY = np.meshgrid(ax, ax)
    b = W / 2 - r
    qx, qy = np.abs(PX) - b, np.abs(PY) - b
    outside = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0))
    sdf = outside + np.minimum(np.maximum(qx, qy), 0) - r   # <0 inside

    depth = np.maximum(-sdf, 0)
    gy, gx = np.gradient(sdf)
    phi = np.arctan2(gy, gx)                                # outward normal, y down

    amp = (mean
           + lobe2 * np.cos(2 * (phi - np.pi / 4))
           + lobe1 * np.cos(phi - np.radians(225)))
    alpha = np.clip(1 - depth / (width * W), 0, 1) ** falloff * amp
    alpha = np.clip(alpha, 0, 1)[..., None]

    lit = a + alpha * (255.0 - a)
    out = Image.fromarray(np.clip(lit, 0, 255).astype(np.uint8)).convert("RGBA")
    out.putalpha(tile.getchannel("A") if tile.mode == "RGBA" else 255)
    return out


def background_colour(im):
    """Modal-ish background colour, sampled from the four border strips."""
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    h, w = a.shape[:2]
    e = max(2, min(h, w) // 64)
    border = np.concatenate([a[:e].reshape(-1, 3), a[-e:].reshape(-1, 3),
                             a[:, :e].reshape(-1, 3), a[:, -e:].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(border, axis=0))


def pad_square(im, fill=0.78):
    """Lift the artwork out and centre it on a fresh square of the background.

    Use when the source is off-centre and the surround should look even on every
    side -- cropping cannot fix that, it just moves the imbalance around. The new
    canvas is painted in the sampled background colour, so on a flat background
    there is no seam, and any rounded corners baked into a screenshot are
    discarded rather than fighting the corner mask.

    fill is the fraction of the square the artwork's longest edge occupies.
    Margins come out equal left/right and equal top/bottom; they differ between
    the two axes whenever the subject is not itself square, which is correct --
    equalising all four would mean distorting the artwork.
    """
    x0, y0, x1, y1 = content_bbox(im)
    art = im.crop((x0, y0, x1, y1))
    side = round(max(art.size) / fill)
    sq = Image.new("RGB", (side, side), background_colour(im))
    sq.paste(art, ((side - art.width) // 2, (side - art.height) // 2),
             art if art.mode == "RGBA" else None)
    return sq.convert("RGBA")


def build(src, platform="macos", recentre=True, pixel=False, zoom=None, pad=None, rim=True):
    # Pixel art must be upscaled with NEAREST -- Lanczos smears the hard edges
    # into mush, which is the whole point of the artwork.
    up = Image.NEAREST if pixel else Image.LANCZOS
    im = Image.open(src).convert("RGBA")
    if pad:
        im = pad_square(im, pad)
        recentre, zoom = False, None   # already centred and sized
    if platform == "ios":
        tile = square_crop(im, recentre, zoom).resize((CANVAS, CANVAS), up)
        m = corner_mask(CANVAS, IOS_RADIUS, IOS_CORNER_N)
        rounded = tile.copy()
        rounded.putalpha(m)
        return rounded, tile.convert("RGB")   # rounded + opaque square for Xcode

    tile = square_crop(im, recentre, zoom).resize((MAC_TILE, MAC_TILE), up)
    if rim:
        tile = rim_light(tile, MAC_RADIUS)
    m = corner_mask(MAC_TILE, MAC_RADIUS, MAC_CORNER_N)
    off = (CANVAS - MAC_TILE) // 2

    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    shadow = Image.new("L", (CANVAS, CANVAS), 0)
    shadow.paste(m, (off, off + 10))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.paste(Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 90)), (0, 0), shadow)

    tile.putalpha(m)
    canvas.alpha_composite(tile, (off, off))
    return canvas, None


def write_icns(canvas, out_icns):
    iconset = os.path.splitext(out_icns)[0] + ".iconset"
    os.makedirs(iconset, exist_ok=True)
    for px, name in ICNS_SIZES:
        canvas.resize((px, px), Image.LANCZOS).save(f"{iconset}/icon_{name}.png")
    subprocess.run(["iconutil", "-c", "icns", iconset, "-o", out_icns], check=True)
    return iconset


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("-o", "--outdir", default=None,
                    help="output directory (default: alongside the source)")
    ap.add_argument("-n", "--name", default=None,
                    help="output basename (default: from the source filename)")
    ap.add_argument("-p", "--platform", choices=["macos", "ios"], default="macos")
    ap.add_argument("--no-recentre", action="store_true",
                    help="plain centre crop instead of recentring on the artwork")
    ap.add_argument("--pixel", action="store_true",
                    help="pixel art: upscale with nearest-neighbour so edges stay hard")
    ap.add_argument("-z", "--zoom", type=float, default=None, metavar="FRAC",
                    help="crop in until the artwork fills FRAC of the tile, e.g. 0.72. "
                         "Use when the source has wide margins.")
    ap.add_argument("--no-rim", action="store_true",
                    help="skip the Apple edge rim light (on by default for macOS)")
    ap.add_argument("--pad", type=float, default=None, metavar="FRAC",
                    help="re-centre the artwork on a fresh square of the background "
                         "colour, filling FRAC of it (0.78 is a good default). Use when "
                         "the source is off-centre and the surround must look even.")
    a = ap.parse_args()

    outdir = a.outdir or os.path.dirname(os.path.abspath(a.src))
    base = a.name or os.path.splitext(os.path.basename(a.src))[0].strip() or "icon"
    os.makedirs(outdir, exist_ok=True)

    canvas, square = build(a.src, a.platform, not a.no_recentre, a.pixel, a.zoom, a.pad,
                           not a.no_rim)
    written = []

    if a.platform == "macos":
        png = os.path.join(outdir, f"{base}-macos-1024.png")
        canvas.save(png); written.append(png)
        icns = os.path.join(outdir, f"{base}.icns")
        write_icns(canvas, icns); written.append(icns)
    else:
        png = os.path.join(outdir, f"{base}-ios-1024.png")
        canvas.save(png); written.append(png)
        p512 = os.path.join(outdir, f"{base}-ios-512.png")
        canvas.resize((512, 512), Image.LANCZOS).save(p512); written.append(p512)
        sq = os.path.join(outdir, f"{base}-ios-square-1024.png")
        square.save(sq); written.append(sq)   # Xcode AppIcon rejects alpha

    for p in written:
        print(p)


if __name__ == "__main__":
    sys.exit(main())
