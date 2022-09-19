from PIL import Image


mask_refs_mitmaps = []


def _init_mitmaps():
    if mask_refs_mitmaps:
        return
    ref = Image.open('border_radius.2048.png')
    mask_refs_mitmaps.insert(0, ref)
    while ref.width >= 4:
        ref = ref.resize((ref.width // 2, ref.height // 2), Image.HAMMING)
        mask_refs_mitmaps.insert(0, ref)


def border_radius_args(size, radius, vertical_radius=None):
    if vertical_radius is None:
        vertical_radius = radius

    def inner(dim, radius):
        if not isinstance(radius, tuple):
            radius = (radius,)

        r_nw, r_ne, r_se, r_sw = list(radius) + [None] * (4 - len(radius))

        if r_ne is None:
            r_ne = r_nw
        if r_se is None:
            r_se = r_nw
        if r_sw is None:
            r_sw = r_ne
        return r_nw, r_ne, r_se, r_sw

    return list(zip(
        inner(size[0], radius),
        inner(size[1], vertical_radius)
    ))


def border_radius_mask(size, radius, vertical_radius=None):
    _init_mitmaps()

    r_nw, r_ne, r_se, r_sw = border_radius_args(size, radius, vertical_radius)

    im = Image.new('L', size, 255)

    corners_cache = {}

    for r, transpose, offset_x, offset_y in [
        (r_nw, None, 0, 0),
        (r_ne, Image.FLIP_LEFT_RIGHT, 1, 0),
        (r_sw, Image.FLIP_TOP_BOTTOM, 0, 1),
        (r_se, Image.ROTATE_180, 1, 1),
    ]:
        if min(*r) == 0:
            continue
        corner = corners_cache.get(r)
        if corner is None:
            mitmap_index = min(max(*r).bit_length(), len(mask_refs_mitmaps) - 1)
            mask_ref = mask_refs_mitmaps[mitmap_index]
            corner = mask_ref.resize(r, Image.HAMMING)
            corners_cache[r] = corner
        if transpose is not None:
            corner = corner.transpose(transpose)
        im.paste(corner, (
            (size[0] - r[0]) * offset_x,
            (size[1] - r[1]) * offset_y
        ))

    return im
