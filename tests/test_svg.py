from aratools.svg import get_text_box
import pytest
from pathlib import Path

import drawSvg as draw

REF_DIR = Path(__file__).absolute().parent / "svg_references"


@pytest.mark.parametrize("align", ["text-bottom", "middle", "text-top"])
def test_get_text_box(align):
    tbox = get_text_box(x=10, y=10, width=100, height=100, text="Foo", align=align)
    canvas = draw.Drawing(width=120, height=120)
    canvas.append(tbox)
    with open(REF_DIR / f"test_{align}.svg", "r") as f:
        assert canvas.asSvg() == f.read()
