from PIL import Image


def border_radius_mask(size, r_all, r_ne_sw=None, r_se=None, r_sw=None):
    if r_ne_sw is None:
        r_ne_sw = r_all
    if r_se is None:
        r_se = r_all
    if r_sw is None:
        r_sw = r_ne_sw

    im = Image.new('L', size, 255)
    ref = Image.open('border_radius.2048.png')

    for r, transpose, offset_x, offset_y in [
        (r_all, None, 0, 0),
        (r_ne_sw, Image.FLIP_LEFT_RIGHT, 1, 0),
        (r_sw, Image.FLIP_TOP_BOTTOM, 0, 1),
        (r_se, Image.ROTATE_180, 1, 1),
    ]:
        if r == 0:
            continue
        corner = ref.resize((r, r), Image.HAMMING)
        if transpose is not None:
            corner = corner.transpose(transpose)
        im.paste(corner, ((size[0] - r) * offset_x, (size[1] - r) * offset_y))

    return im
