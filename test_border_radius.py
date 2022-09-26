import os.path

import pytest

from border_radius import Image, border_radius_args, border_radius_mask


@pytest.mark.parametrize("size, radius, vert_radius", [
    ((60, 40), (10, 12, 14, 16), None),
    ((60, 40), (10, 12, 14, 16), (20,)),
    ((60, 60), (0, 90), None),
    ((60, 60), (95, 5), None),
])
def test_referential(size, radius, vert_radius):
    def collect_args(radius):
        fn_args = []
        for arg in radius:
            if not isinstance(arg, int):
                arg = round(arg * 100) + 'p'
            fn_args.append(str(arg))
        return ",".join(fn_args)

    out_args = collect_args(radius)
    if vert_radius is not None:
        out_args += "_" + collect_args(vert_radius)

    out_file = f"./test_refs/mask_{size[0]}x{size[1]}_{out_args}.png"

    mask = border_radius_mask(size, radius, vert_radius)

    if not os.path.exists(out_file):
        mask.save(out_file, optimize=True)
        raise AssertionError("reference is not found")

    ref = Image.open(out_file)
    if mask.tobytes() != ref.tobytes():
        os.rename(out_file, '{}.__fail__{}'.format(*os.path.splitext(out_file)))
        mask.save(out_file, optimize=True)
        raise AssertionError("processed doesn't match with reference")


@pytest.mark.parametrize("expected, size, radius, vert_radius", [
    # arguments order and inheritance
    ([(10, 10), (10, 10), (10, 10), (10, 10)], (60, 40), 10, None),
    ([(10, 10), (10, 10), (10, 10), (10, 10)], (60, 40), (10,), None),
    ([(10, 10), (12, 12), (10, 10), (12, 12)], (60, 40), (10, 12), None),
    ([(10, 10), (12, 12), (14, 14), (12, 12)], (60, 40), (10, 12, 14), None),
    ([(10, 10), (12, 12), (14, 14), (16, 16)], (60, 40), (10, 12, 14, 16), None),
    ([(10, 20), (10, 18), (10, 16), (10, 14)], (60, 40), (10,), (20, 18, 16, 14)),
    ([(10, 20), (12, 18), (10, 16), (12, 18)], (60, 40), (10, 12), (20, 18, 16)),
    ([(10, 20), (12, 18), (14, 20), (12, 18)], (60, 40), (10, 12, 14), (20, 18)),
    ([(10, 20), (12, 20), (14, 20), (16, 20)], (60, 40), (10, 12, 14, 16), (20,)),
    ([(10, 20), (12, 20), (14, 20), (16, 20)], (60, 40), (10, 12, 14, 16), 20),
    # list arguments
    ([(10, 12), (12, 14), (14, 12), (16, 14)], (60, 40), [10, 12, 14, 16], [12, 14]),
    # limit overlapped corners
    ([(20, 20), (20, 20), (20, 20), (20, 20)], (60, 40), 50, None),
    ([(20, 20), (20, 20), (20, 20), (20, 20)], (60, 41), 50, None),
    ([(21, 21), (21, 21), (21, 21), (21, 21)], (60, 42), 50, None),
    ([(21, 21), (21, 21), (21, 21), (21, 21)], (60, 43), 50, None),
    ([(33, 33), (7, 7), (33, 33), (7, 7)], (60, 40), (50, 10), None),
    ([(34, 34), (7, 7), (34, 34), (7, 7)], (60, 41), (50, 10), None),
    ([(50, 34), (10, 7), (50, 34), (10, 7)], (60, 41), (5.0, 1.0), None),
])
def test_args(expected, size, radius, vert_radius):
    args = border_radius_args(size, radius, vert_radius)
    assert expected == args
