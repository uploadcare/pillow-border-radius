import os.path

from border_radius import border_radius_mask, Image

import pytest


@pytest.mark.parametrize("size, radius, vertical_radius", [
    ((60, 40), (10,), None),
    ((60, 40), (10, 12), None),
    ((60, 40), (10, 12, 14), None),
    ((60, 40), (10, 12, 14, 16), None),
])
def test_referential(size, radius, vertical_radius):
    def collect_args(radius):
        fn_args = []
        for arg in radius:
            fn_args.append(str(arg))
        return ",".join(fn_args)

    out_args = collect_args(radius)
    if vertical_radius is not None:
        out_args += "_" + collect_args(vertical_radius)

    out_file = f"./test_refs/mask_{size[0]}x{size[1]}_{out_args}.png"

    mask = border_radius_mask(size, radius, vertical_radius)

    if not os.path.exists(out_file):
        mask.save(out_file, optimize=True)
        raise AssertionError("reference is not found")

    ref = Image.open(out_file)
    if mask.tobytes() != ref.tobytes():
        os.rename(out_file, '{}.__fail__{}'.format(*os.path.splitext(out_file)))
        mask.save(out_file, optimize=True)
        raise AssertionError("processed doesn't match with reference")
