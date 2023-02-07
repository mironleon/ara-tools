from pathlib import Path

import pytest

from aratools.svg import TextBox, TextBoxRow

REF_DIR = Path(__file__).absolute().parent / "svg_references"


@pytest.mark.parametrize("align", ["bottom", "middle", "top"])
def test_text_box(align):
    tbox = TextBox(x=10, y=10, width=100, height=100, text="Foo", align=align)
    with open(REF_DIR / f"textbox_{align}.svg", "r") as f:
        assert tbox.to_drawing(width=120, height=120).asSvg() == f.read()


@pytest.mark.parametrize("align", ["bottom", "middle", "top"])
def test_text_box_row(align):
    tbox_row = TextBoxRow(
        x=10,
        y=10,
        width=500,
        height=100,
        n=8,
        align=align,
        texts=[f"foo_{i} \n foo" for i in range(8)],
    )
    with open(REF_DIR / f"textboxrow_{align}.svg", "r") as f:
        assert tbox_row.to_drawing(width=520, height=520).asSvg() == f.read()
