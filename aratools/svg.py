import abc
import subprocess
from collections.abc import Sequence
from typing import Literal

import drawSvg as draw

from aratools.formatting import format_text
from aratools.parcour import CheckPoint, Etappe

align_mode = Literal["bottom", "middle", "top"]

# TODO: thinner lines, support for 'hidden' cps (do not show coordinate), bold styling


# svg tag for grouping elements in and inheriting width and height attributes from
class SVG(draw.DrawingParentElement):
    TAG_NAME = "svg"


class DRAWING(draw.Drawing):
    def __init__(
        self,
        width,
        height,
        origin=(0, 0),
        idPrefix="d",
        displayInline=True,
        **svgArgs,
    ):
        super().__init__(width, height, origin, idPrefix, displayInline, **svgArgs)
        if origin == "center":
            self.viewBox = (-width / 2, -height / 2, width, height)
        else:
            origin = tuple(origin)
            assert len(origin) == 2
            self.viewBox = origin + (width, height)


def etappe_to_svg(etappe: Etappe, team_name: str = "foofooteam") -> draw.Drawing:
    # a3 is 210 x 148 mm
    width = 210
    height = 148
    drawing = DRAWING(width=width, height=height)
    if len(etappe) % 2 == 0:
        n_upper = int(len(etappe) / 2)
        n_lower = n_upper
    else:
        n_upper = int(len(etappe) / 2) + 1
        n_lower = int(len(etappe) / 2)

    # middle line contains etappe number, etappe kind and team name
    middle_line_height = round(height / 15)

    # total height for upper and lower rows
    combined_row_height = round((height - middle_line_height) / 2)
    h_factors = [0.3, 0.1, 0.1, 0.2, 0.3]
    heights = (
        [round(factor * combined_row_height) for factor in h_factors]
        + [middle_line_height]
        + [round(factor * combined_row_height) for factor in reversed(h_factors)]
    )
    n_boxes = [n_lower] * 5 + [3] + [n_upper] * 5
    alignments: list[align_mode] = [
        "top",
        "bottom",
        "bottom",
        "bottom",
        "top",
        "top",
        "top",
        "bottom",
        "bottom",
        "bottom",
        "top",
    ]
    text_lists = [
        ["prik hier1"] * n_lower,
        [f"{etappe.idx}.{i}" for i in range(1, len(etappe) + 1)[-n_lower:]],
        [f"{cp.score} p" for cp in etappe[-n_lower:]],
        [f"{cp.hint}" for cp in etappe[-n_lower:]],
        ["\n".join(str(c) for c in cp.coordinate) for cp in etappe[-n_lower:]],
        [f"Etappe {etappe.idx}", etappe.kind, team_name],
        ["\n".join(str(c) for c in cp.coordinate) for cp in etappe[:n_upper]],
        [f"{cp.hint}" for cp in etappe[:n_upper]],
        [f"{cp.score} p" for cp in etappe[:n_upper]],
        [f"{etappe.idx}.{i}" for i in range(1, len(etappe) + 1)[:n_upper]],
        ["prik hier"] * n_upper,
    ]
    for i, (row_height, n, align, texts) in enumerate(
        zip(heights, n_boxes, alignments, text_lists, strict=True)
    ):
        y = int(sum(heights[:i]))
        drawing.append(
            TextBoxRow(
                x=0,
                y=y,
                width=width,
                height=row_height,
                n=n,
                align=align,
                texts=texts,
            )
        )

    drawing.saveSvg("test.svg")


class Box(SVG):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        super().__init__(
            x=x, y=y, width=width, height=height, children=self._get_children()
        )

    @abc.abstractmethod
    def _get_children(self) -> list[draw.DrawingBasicElement]:
        pass

    def to_drawing(self, width: int, height: int) -> draw.Drawing:
        assert width >= self.x + self.width
        assert height >= self.y + self.height
        canvas = DRAWING(width=width, height=width)
        canvas.append(self)
        print(canvas.viewBox)
        return canvas


class TextBox(Box):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        fontSize: int = 8,
        align: align_mode = "middle",
    ):
        self.text = text
        self.fontSize = fontSize
        self.align = align
        super().__init__(x=x, y=y, width=width, height=height)

    def _get_children(self) -> list[draw.DrawingBasicElement]:
        self.rect = draw.Rectangle(
            x=0,
            y=0,
            width="100%",
            height="100%",
            fill="white",
            stroke="black",
            stroke_width=1,
        )
        match self.align:
            case "bottom":
                y = "95%"
                baseline = "auto"
            case "middle":
                y = "50%"
                baseline = "middle"
            case "top":
                y = "10"
                baseline = "hanging"
            case _:
                raise Exception(f"Unknown align mode: {self.align}")
        self.text = draw.Text(
            text=format_text(self.width, self.text, self.fontSize),
            fontSize=self.fontSize,
            x="50%",
            y=y,
            text_anchor="middle",
            dominant_baseline=baseline,
            font_family="monospace",
        )
        return [self.rect, self.text]


class TextBoxRow(Box):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        n: int,
        align: align_mode,
        texts: Sequence[str],
    ):
        self.n = n
        self.align = align
        self.texts = texts
        super().__init__(x=x, y=y, width=width, height=height)

    def _get_children(self) -> list[draw.DrawingBasicElement]:
        return [
            TextBox(
                x=self.x + round(i / self.n * self.width),
                y=self.y,
                width=round(self.width / self.n),
                height=self.height,
                text=self.texts[i],
                align=self.align,
            )
            for i in range(self.n)
        ]


idx = 5
kind = "Hardlopen"
cps = [
    CheckPoint(idx=1, score=1, hint="hANS de brug", coordinate=(23400, 23523)),
    CheckPoint(idx=2, score=2, hint="Paaltje", coordinate=(23444, 23523)),
    CheckPoint(idx=3, score=1, hint="Onder de brug", coordinate=(23406, 23523)),
    CheckPoint(idx=4, score=2, hint="Paaltje", coordinate=(23444, 23523)),
    CheckPoint(idx=5, score=1, hint="Onder de brug", coordinate=(27400, 23523)),
    CheckPoint(idx=6, score=2, hint="Paaltje", coordinate=(23444, 23523)),
    CheckPoint(idx=7, score=1, hint="Onder de brug", coordinate=(23400, 23723)),
    CheckPoint(idx=8, score=2, hint="Paaltje", coordinate=(23444, 23523)),
]
ref_etappe = Etappe(idx=idx, kind=kind, checkpoints=tuple(cps))

etappe_to_svg(etappe=ref_etappe)

subprocess.run("open test.svg", shell=True)
