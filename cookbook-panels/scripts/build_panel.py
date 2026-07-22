"""
Cookbook Panels — Blender builder + utilities.

Run inside Blender (paste/exec via the Blender MCP `execute_blender_code`, or
`exec(open(path).read())`). Call the helpers; don't re-derive them. See
../references/design-tokens.md for the values and the "why".

IMPORTANT: set ASSET_DIR to this skill's assets/ folder (absolute path) before
importing any SVG.
"""
import bpy, bmesh, math
from mathutils import Vector, kdtree

# ---------------------------------------------------------------- config
ASSET_DIR = "/Users/lucasmaher/.claude/skills/cookbook-panels/assets"
S = 0.01  # 1 web px = 0.01 Blender units

def D2B(wx, wy, H):
    """Design px -> Blender (XY), flipping Y. H = panel height in px (283 / 360)."""
    return (wx * S, (H - wy) * S)

# ---------------------------------------------------------------- color
def _s2l(x):
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4

def hexcol(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return (_s2l(r), _s2l(g), _s2l(b), 1.0)

def _set(bsdf, key, val):
    if key in bsdf.inputs:
        bsdf.inputs[key].default_value = val

# ---------------------------------------------------------------- materials
def make_materials():
    """Create (or update) the house materials. Returns a name->material dict."""
    def mat(name, base, metallic=0.0, rough=0.5, spec=0.5, emit=None, emit_str=0.0, aniso=0.0):
        m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = hexcol(base)
        b.inputs["Metallic"].default_value = metallic
        b.inputs["Roughness"].default_value = rough
        _set(b, "Specular IOR Level", spec); _set(b, "Specular", spec)
        _set(b, "Anisotropic", aniso)
        if emit is not None:
            _set(b, "Emission Color", hexcol(emit)); _set(b, "Emission Strength", emit_str)
        return m
    return {
        "M_Satin":  mat("M_Satin",  "#CCCFD4", metallic=1.0, rough=0.30, aniso=0.4),
        "M_Purple": mat("M_Purple", "#5A36A8", rough=0.38, emit="#5A36A8", emit_str=0.18),
        "M_Title":  mat("M_Title",  "#5A36A8", rough=1.0, spec=0.0),   # fully matte
        "M_Meta":   mat("M_Meta",   "#0D0D0D", rough=1.0, spec=0.0),   # fully matte
        "M_Seg":    mat("M_Seg",    "#E7ECED", rough=0.5),
        "M_Floor":  mat("M_Floor",  "#29292B", rough=0.6),
        "M_Softbox": mat("M_Softbox", "#E7E7E7", emit="#FFFFFF", emit_str=6.0),
    }

def assign(obj, material):
    obj.data.materials.clear(); obj.data.materials.append(material)

# ---------------------------------------------------------------- geometry helpers
def world_bbox(o):
    bpy.context.view_layer.update()
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs = [v.x for v in cs]; ys = [v.y for v in cs]; zs = [v.z for v in cs]
    return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)

def world_top(o):    return world_bbox(o)[5]
def world_bottom(o): return world_bbox(o)[4]

def _activate(o):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = o; o.select_set(True)

def import_svg_as_mesh(filename, name):
    """Import an SVG (filled curve) and convert to a flat mesh in the XY plane."""
    import os
    before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=os.path.join(ASSET_DIR, filename))
    new = [o for o in bpy.data.objects if o not in before]
    curves = [o for o in new if o.type == 'CURVE']
    for c in curves:
        c.data.dimensions = '2D'; c.data.fill_mode = 'BOTH'
    bpy.ops.object.select_all(action='DESELECT')
    for c in curves: c.select_set(True)
    bpy.context.view_layer.objects.active = curves[0]
    if len(curves) > 1: bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active
    bpy.ops.object.convert(target='MESH'); o = bpy.context.view_layer.objects.active
    o.name = name
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    return o

def fit_rect(o, bxmin, bxmax, bymin, bymax, rotate90=False):
    """Scale+move o so its XY bbox fills the target Blender rect."""
    if rotate90:
        o.rotation_euler[2] = math.radians(90)
        _activate(o); bpy.ops.object.transform_apply(rotation=True)
    a = world_bbox(o); cw = a[1] - a[0]; ch = a[3] - a[2]
    o.scale = ((bxmax - bxmin) / cw, (bymax - bymin) / ch, 1.0)
    _activate(o); bpy.ops.object.transform_apply(scale=True)
    a = world_bbox(o); o.location.x += (bxmin - a[0]); o.location.y += (bymin - a[2])
    bpy.context.view_layer.update()

def solidify(o, thickness=0.08, top_at_zero=True):
    """Give a flat mesh thickness. top_at_zero -> grows downward, top stays at z=0."""
    _activate(o)
    m = o.modifiers.new("sol", "SOLIDIFY"); m.thickness = thickness
    m.offset = -1 if top_at_zero else 1
    bpy.ops.object.convert(target='MESH')

# ---------------------------------------------------------------- mesh cleanup
def clean_mesh(o, dissolve_deg=4.0):
    """Remove SVG-import residue: dup verts, T-junctions, overlapping collinear
    edges, slivers, holes. Run on EVERY SVG-derived mesh before raising/beveling.
    """
    _activate(o)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.0018)
    bpy.ops.mesh.dissolve_limited(angle_limit=math.radians(dissolve_deg))
    bpy.ops.mesh.dissolve_degenerate(threshold=0.0006)
    bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False)
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.fill_holes(sides=0)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    # T-junction pass (a vert sitting mid-edge) — repeat until clean
    for _ in range(3):
        bad = _t_junction_verts(o)
        if not bad:
            break
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(o.data); bm.verts.ensure_lookup_table()
        for i in bad:
            bm.verts[i].select = True
        bmesh.update_edit_mesh(o.data)
        bpy.ops.mesh.dissolve_verts()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0018)
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT')

def _t_junction_verts(o, tol=0.0015):
    bm = bmesh.new(); bm.from_mesh(o.data); bm.verts.ensure_lookup_table()
    bad = set()
    for e in bm.edges:
        a = e.verts[0].co; b = e.verts[1].co; ab = b - a; L = ab.length
        if L < 1e-6:
            continue
        for v in bm.verts:
            if v in e.verts:
                continue
            t = (v.co - a).dot(ab) / (L * L)
            if 0.02 < t < 0.98 and (v.co - (a + ab * t)).length < tol:
                bad.add(v.index)
    bm.free()
    return bad

# ---------------------------------------------------------------- raised content
def bevel_all(o, width=0.006, segments=2, angle=30.0):
    """Round all sharp edges a bit (same treatment for pixel cubes and tiles).
    Use the angle-limited Bevel MODIFIER — an edit-mode bevel clamps short edges
    to nothing."""
    for m in list(o.modifiers):
        if m.type == 'BEVEL':
            o.modifiers.remove(m)
    b = o.modifiers.new("bev", "BEVEL")
    b.width = width; b.segments = segments
    b.limit_method = 'ANGLE'; b.angle_limit = math.radians(angle)
    b.use_clamp_overlap = True
    _activate(o)
    try: bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    except Exception: bpy.ops.object.shade_smooth()

def build_glyph(name, grid, gx0, gx1, gy0, gy1, H, base_z, height, gap_px=1.6, cols=16):
    """Pixel-art glyph as one mesh of small boxes. `grid` = list of (row, c1, c2)
    spans (1-indexed). Sits with bottoms at base_z, rising `height`."""
    pitchx = (gx1 - gx0) / cols
    rows = max(r for r, _, _ in grid)
    pitchy = (gy1 - gy0) / rows
    tw = (pitchx - gap_px) * S; th = (pitchy - gap_px) * S
    hz = height / 2.0; zc = base_z + hz
    bm = bmesh.new()
    def box(cx, cy, cz, hx, hy, hz):
        vs = [bm.verts.new((cx + sx * hx, cy + sy * hy, cz + sz * hz))
              for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
        for f in [(0,1,3,2),(4,6,7,5),(0,2,6,4),(1,5,7,3),(0,4,5,1),(2,3,7,6)]:
            bm.faces.new([vs[i] for i in f])
    for (r, c1, c2) in grid:
        for c in range(c1, c2 + 1):
            X, Yb = D2B(gx0 + (c - 0.5) * pitchx, gy0 + (r - 0.5) * pitchy, H)
            box(X, Yb, zc, tw / 2, th / 2, hz)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    bevel_all(o)
    return o

def make_text(name, body, size, x_d, baseline_d, H, extrude=0.018, offset=0.0,
              base_z=0.0):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = body
    cu.size = size; cu.extrude = extrude; cu.offset = offset
    cu.align_x = 'LEFT'; cu.align_y = 'BOTTOM_BASELINE'
    o = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(o)
    X, Yb = D2B(x_d, baseline_d, H); o.location = (X, Yb, base_z)
    return o

def seat_flush(o, top_z, sink=0.002):
    """Drop o so its bottom rests on a surface at top_z (with a tiny sink).
    Raised elements still rise from there. XY untouched."""
    bpy.context.view_layer.update()
    o.location.z += (top_z - sink) - world_bottom(o)
    bpy.context.view_layer.update()

# ---------------------------------------------------------------- lighting
def setup_metal_lighting():
    """Dark, contrasty studio so the satin metal reads (not flat white)."""
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE'
    if hasattr(sc.eevee, "use_raytracing"):
        sc.eevee.use_raytracing = True
    w = sc.world; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = hexcol("#0E0E12")
    bg.inputs["Strength"].default_value = 1.0
    # key area light
    if "Light" not in bpy.data.objects:
        ld = bpy.data.lights.new("Light", 'AREA'); lo = bpy.data.objects.new("Light", ld)
        bpy.context.collection.objects.link(lo)
    key = bpy.data.objects["Light"]; key.data.type = 'AREA'
    key.data.size = 5; key.data.energy = 600; key.location = (1.4, -0.6, 4.5)
    # emissive softbox overhead (reflection sweep)
    if "Softbox" not in bpy.data.objects:
        bpy.ops.mesh.primitive_plane_add(size=7, location=(1.4, 0.6, 5.5))
        sb = bpy.context.active_object; sb.name = "Softbox"
        sb.rotation_euler = (math.radians(25), 0, 0)
        assign(sb, make_materials()["M_Softbox"])
        if hasattr(sb, "visible_camera"):
            sb.visible_camera = False
    # dark floor
    if "Floor" not in bpy.data.objects:
        bpy.ops.mesh.primitive_plane_add(size=40, location=(1.4, 1.3, 0))
        fl = bpy.context.active_object; fl.name = "Floor"
        assign(fl, make_materials()["M_Floor"])

# ---------------------------------------------------------------- the pot glyph
# 16-col x 13-row pixel pot with two steam dots. (row, colStart, colEnd), 1-indexed.
POT_GLYPH = [
    (1,6,6),(1,11,11),(2,5,5),(2,10,10),(3,6,6),(3,11,11),(4,5,5),(4,10,10),
    (5,8,9),(6,4,13),(7,3,14),(8,3,14),(9,1,16),(10,3,14),(11,3,14),(12,3,14),(13,4,13),
]

# ---------------------------------------------------------------- left panel build
def build_left_panel(title="ONE POT PASTA", meta="5 portions · ~25 min",
                     n_segments=7, highlight_segment=0, raised_segments=True):
    """Assemble the left/title panel. Returns dict of created objects.
    highlight_segment: 1-based index of a strip tile to color purple (0 = none,
    counting from the bottom). Tweak text/positions to taste afterwards."""
    H = 283.0
    M = make_materials()

    # card + strip blobs (both rotated 90deg in 2D) — target rects in Blender units
    main = import_svg_as_mesh("left_blob.svg", "Panel_Main")
    fit_rect(main, 0.987, 2.801, 0.03, 2.783, rotate90=True)
    solidify(main, 0.08); clean_mesh(main); assign(main, M["M_Satin"])

    strip = import_svg_as_mesh("strip_outer.svg", "Panel_Strip")
    fit_rect(strip, 0.187, 0.906, 0.026, 2.785, rotate90=True)
    solidify(strip, 0.08); clean_mesh(strip); assign(strip, M["M_Satin"])

    top = world_top(main)  # flat top surface (z)

    # title + meta text (house sizes), matte, seated flush
    t = make_text("Txt_Title", title, 0.1786, 116, 54, H, extrude=0.018, offset=0.0058)
    assign_text(t, M["M_Title"]); seat_flush(t, top)
    mtxt = make_text("Txt_Meta", meta, 0.0893, 116, 70, H, extrude=0.0012, offset=0.0032)
    assign_text(mtxt, M["M_Meta"]); seat_flush(mtxt, top)

    # raised pixel-pot glyph
    g = build_glyph("Glyph", POT_GLYPH, 116, 232, 103, 197, H, base_z=top, height=0.042)
    assign(g, M["M_Purple"]); seat_flush(g, top)

    # strip segments
    segs = import_svg_as_mesh("strip_full.svg", "Strip_Segments")
    fit_rect(segs, 0.14, 0.96, 0.03, 2.73, rotate90=False)
    solidify(segs, 0.024); clean_mesh(segs); assign(segs, M["M_Seg"])
    seat_flush(segs, top)
    if raised_segments:
        _raise_segments_to(segs, world_top(g))   # match glyph height
    bevel_all(segs)
    if highlight_segment:
        _color_segment(segs, highlight_segment, M["M_Purple"])

    setup_metal_lighting()
    return {"main": main, "strip": strip, "title": t, "meta": mtxt,
            "glyph": g, "segments": segs}

def assign_text(o, material):
    o.data.materials.clear(); o.data.materials.append(material)

def _raise_segments_to(o, target_top, sink=0.001):
    """Scale segments in Z so their tops reach target_top, keep bottom seated."""
    _activate(o)
    bpy.ops.object.transform_apply(scale=True)   # bake scale for even result
    b, t = world_bottom(o), world_top(o)
    target_bottom = world_bottom(o)  # keep current bottom
    k = (target_top - target_bottom) / (t - b)
    o.scale.z *= k; bpy.context.view_layer.update()
    o.location.z += target_bottom - world_bottom(o)
    bpy.context.view_layer.update()

def _color_segment(o, index_from_bottom, material):
    """Assign `material` to the Nth tile counting from the lowest world Y."""
    if material.name not in [m.name for m in o.data.materials if m]:
        o.data.materials.append(material)
    pidx = [i for i, m in enumerate(o.data.materials) if m and m.name == material.name][0]
    mw = o.matrix_world
    bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
    seen = set(); islands = []
    for f in bm.faces:
        if f.index in seen:
            continue
        stack = [f]; comp = []
        while stack:
            c = stack.pop()
            if c.index in seen:
                continue
            seen.add(c.index); comp.append(c.index)
            for e in c.edges:
                for nf in e.link_faces:
                    if nf.index not in seen:
                        stack.append(nf)
        vs = {v for fi in comp for v in bm.faces[fi].verts}
        cy = sum((mw @ v.co).y for v in vs) / len(vs)
        islands.append((cy, comp))
    bm.free()
    islands.sort(key=lambda t: t[0])
    target = set(islands[index_from_bottom - 1][1])
    _activate(o); bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    bpy.ops.mesh.select_all(action='DESELECT')
    bm2 = bmesh.from_edit_mesh(o.data); bm2.faces.ensure_lookup_table()
    for fi in target:
        bm2.faces[fi].select = True
    bmesh.update_edit_mesh(o.data)
    o.active_material_index = pidx
    bpy.ops.object.material_slot_assign()
    bpy.ops.object.mode_set(mode='OBJECT')

# Stopwatch button glyphs (pixel patterns)
CLOSE_X = [(0,2,2),(1,2,2),(2,0,4),(3,2,2),(4,2,2)]  # + pattern, will be rotated -44.38deg in web
PLAY_TRI = [(0,4,4),(1,3,4),(2,2,4),(3,3,4),(4,4,4)]  # triangle, 5 wide
STOP_SQ = [(1,1,3),(2,1,3),(3,1,3)]  # square, 3 wide

# ---------------------------------------------------------------- stopwatch timer build
def build_stopwatch(n_segments=20, highlight_from_bottom=0):
    """Assemble the stopwatch timer modal. Returns dict of created objects.
    n_segments: number of purple ring segments (default 20).
    highlight_from_bottom: 0-based index of a segment to color purple (0 = none)."""
    H = 388.334
    M = make_materials()

    # blob background
    blob = import_svg_as_mesh("stopwatch_blob.svg", "Stopwatch_Blob")
    fit_rect(blob, 0, 4.19621, 0, 3.88334)
    solidify(blob, 0.08); clean_mesh(blob); assign(blob, M["M_Satin"])

    top = world_top(blob)
    center_x, center_y = D2B(209.7, 193.9, H)
    ring_z = top + 0.001

    # white center ring
    bpy.ops.mesh.primitive_cylinder_add(radius=1.3838, depth=0.01, vertices=64)
    ring = bpy.context.active_object
    ring.name = "Ring_White"
    ring.location = (center_x, center_y, ring_z)
    mat_white = bpy.data.materials.new("M_White_Ring")
    mat_white.use_nodes = True
    b = mat_white.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexcol("#f4f6f6")
    b.inputs["Metallic"].default_value = 0.0
    b.inputs["Roughness"].default_value = 0.5
    ring.data.materials.append(mat_white)

    # inner gray center circle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.9738, depth=0.01, vertices=64)
    inner = bpy.context.active_object
    inner.name = "Inner_Center"
    inner.location = (center_x, center_y, ring_z + 0.002)
    assign(inner, M["M_Satin"])

    # time display text, matte, centered in inner circle
    time_txt = make_text("Txt_Time", "10:00", 0.41964, 209.7, 193.9, H,
                         extrude=0.008, offset=0.003)
    assign_text(time_txt, M["M_Title"])
    time_txt.location = (center_x, center_y, ring_z + 0.008)
    bpy.context.view_layer.update()

    # purple segmented ring (20 discrete raised tiles)
    seg_radius = 1.6730  # outer radius of ring segments
    seg_height = 0.042   # same height as pixel glyphs
    seg_width = 0.08     # radial width of each segment
    seg_angle = 360.0 / n_segments

    segments = []
    for i in range(n_segments):
        angle = i * seg_angle
        # position each segment at the ring radius
        rad = math.radians(angle + 90)
        seg_x = center_x + seg_radius * math.cos(rad) * 0.5
        seg_y = center_y + seg_radius * math.sin(rad) * 0.5

        # create small raised tile
        bpy.ops.mesh.primitive_cube_add(size=0.15)
        seg = bpy.context.active_object
        seg.name = f"Seg_{i}"
        seg.location = (seg_x, seg_y, ring_z + seg_height * 0.5)
        seg.scale = (0.08, 0.15, 0.04)
        assign(seg, M["M_Purple"])
        segments.append(seg)

    # close button (X) - bottom-left ear
    close_pos = D2B(7.74 + 32.659, 307.93 + 32.659, H)
    close_glyph = build_glyph("Btn_Close", CLOSE_X, close_pos[0]*100, close_pos[0]*100 + 50,
                              close_pos[1]*100, close_pos[1]*100 + 50, H, base_z=ring_z, height=0.04)
    assign(close_glyph, M["M_Purple"])
    close_glyph.rotation_euler[2] = math.radians(-44.38)
    _activate(close_glyph); bpy.ops.object.transform_apply(rotation=True)

    # play button (triangle) - top-right ear
    play_pos = D2B(348.0, 96.49 + 32.659, H)
    play_glyph = build_glyph("Btn_Play", PLAY_TRI, play_pos[0]*100, play_pos[0]*100 + 50,
                             play_pos[1]*100, play_pos[1]*100 + 50, H, base_z=ring_z, height=0.04)
    assign(play_glyph, M["M_Purple"])

    setup_metal_lighting()
    return {"blob": blob, "ring_white": ring, "inner_center": inner, "time_text": time_txt,
            "segments": segments, "btn_close": close_glyph, "btn_play": play_glyph}

# Quick start, e.g.:
#   exec(open(".../scripts/build_panel.py").read())
#   build_left_panel(highlight_segment=1)   # purple bottom tile
#   build_stopwatch()   # standard stopwatch timer
