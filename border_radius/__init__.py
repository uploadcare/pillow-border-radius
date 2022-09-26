from os.path import abspath, dirname, join

from PIL import Image, ImageOps


mask_refs_mipmaps = []


def resource(*x):
    return abspath(join(abspath(dirname(__file__)), 'resources', *x))


def _init_mipmaps():
    if mask_refs_mipmaps:
        return
    ref = Image.open(resource('border_radius.2048.png'))
    mask_refs_mipmaps.insert(0, ref)
    while ref.width >= 4:
        ref = ref.resize((ref.width // 2, ref.height // 2), Image.HAMMING)
        mask_refs_mipmaps.insert(0, ref)


def border_radius_args(size, radius, vert_radius=None):
    if vert_radius is None:
        vert_radius = radius

    def rel_size(dim, radius):
        if not isinstance(radius, (list, tuple)):
            radius = (radius,)

        radius = list(radius) + [None] * 3

        if radius[1] is None:
            radius[1] = radius[0]
        if radius[2] is None:
            radius[2] = radius[0]
        if radius[3] is None:
            radius[3] = radius[1]

        return [
            r / dim if isinstance(r, int) else r
            for r in radius[:4]
        ]

    radius = rel_size(size[0], radius)
    vert_radius = rel_size(size[1], vert_radius)
    scale = 1.001 * max(
        radius[0] + radius[1], radius[2] + radius[3],
        vert_radius[0] + vert_radius[3], vert_radius[1] + vert_radius[2]
    )
    if scale > 1.0:
        radius = [r / scale for r in radius]
        vert_radius = [r / scale for r in vert_radius]
    return list(zip(
        (round(r * size[0]) for r in radius),
        (round(r * size[1]) for r in vert_radius),
    ))


def border_radius_mask(size, radius, vert_radius=None):
    _init_mipmaps()

    r_nw, r_ne, r_se, r_sw = border_radius_args(size, radius, vert_radius)

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
            mipmap_index = min(max(*r).bit_length(), len(mask_refs_mipmaps) - 1)
            mask_ref = mask_refs_mipmaps[mipmap_index]
            corner = mask_ref.resize(r, Image.HAMMING)
            corners_cache[r] = corner
        if transpose is not None:
            corner = corner.transpose(transpose)
        if transpose is None or (size[0] >= r[0] * 2 and size[1] >= r[1] * 2):
            im.paste(corner, (
                (size[0] - r[0]) * offset_x,
                (size[1] - r[1]) * offset_y
            ))
        else:
            bg = Image.new('L', r, 0)
            im.paste(bg, (
                (size[0] - r[0]) * offset_x,
                (size[1] - r[1]) * offset_y
            ), ImageOps.invert(corner))

    return im
