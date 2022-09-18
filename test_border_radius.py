import os.path

from border_radius import border_radius_mask, Image

import pytest


@pytest.mark.parametrize("size,r_args,r_kwargs", [
    ((60, 40), (10,), {}),
    ((60, 40), (10, 12), {}),
    ((60, 40), (10, 12, 14), {}),
    ((60, 40), (10, 12, 14, 16), {}),
])
def test_referential(size, r_args, r_kwargs):
    fn_args = []
    for arg in r_args:
        fn_args.append(str(arg))
    for name, arg in r_kwargs.items():
        fn_args.append(f"{name}={arg}")
    out_args = ",".join(fn_args)
    out_file = f"./test_refs/mask_{size[0]}x{size[1]}_{out_args}.png"

    mask = border_radius_mask(size, *r_args, **r_kwargs)

    if not os.path.exists(out_file):
        mask.save(out_file, optimize=True)
        raise AssertionError("reference is not found")

    ref = Image.open(out_file)
    if mask.tobytes() != ref.tobytes():
        os.rename(out_file, '{}.__fail__{}'.format(*os.path.splitext(out_file)))
        mask.save(out_file, optimize=True)
        raise AssertionError("processed doesn't match with reference")
