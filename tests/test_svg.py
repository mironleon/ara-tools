from aratools.svg import TextBox, TextBoxRow
import pytest
from pathlib import Path


REF_DIR = Path(__file__).absolute().parent / "svg_references"


@pytest.mark.parametrize("align", ["text-bottom", "middle", "text-top"])
def test_text_box(align):
    tbox = TextBox(x=10, y=10, width=100, height=100, text="Foo", align=align)
    with open(REF_DIR / f"test_{align}.svg", "r") as f:
        assert tbox.to_drawing(width=120, height=120).asSvg() == f.read()


def test_text_box_row():
    tbox_row = TextBoxRow(
        x=10,
        y=10,
        width=500,
        height=100,
        n=8,
        align="middle",
        texts=[f"foo_{i} \n foo" for i in range(8)],
    )
    with open(REF_DIR / "test_textboxrow.svg", "r") as f:
        assert tbox_row.to_drawing(width=520, height=520).asSvg() == f.read()
