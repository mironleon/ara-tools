from aratools.svg import TextBox, TextBoxRow

from pathlib import Path

REF_DIR = Path(__file__).absolute().parent / "svg_references"

for align in ["bottom", "middle", "top"]:
    tbox = TextBox(x=10, y=10, width=100, height=100, text="Foo", align=align)
    tbox.to_drawing(width=120, height=120).saveSvg(REF_DIR / f"textbox_{align}.svg")

    tbox_row = TextBoxRow(
        x=10,
        y=10,
        width=500,
        height=100,
        n=8,
        align=align,
        texts=[f"foo_{i} \n foo" for i in range(8)],
    )

    tbox_row.to_drawing(width=520, height=520).saveSvg(
        REF_DIR / f"textboxrow_{align}.svg"
    )
