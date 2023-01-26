from aratools.parcour import Etappe, CheckPoint
import drawSvg as draw
import abc

from typing import Literal, Sequence

align_mode = Literal["text-bottom", "middle", "text-top"]


def etappe_to_svg(etappe: Etappe) -> draw.Drawing:
    # a3 is 210 x 148 mm
    width = 210
    height = 148
    drawing = draw.Drawing(width=width, height=height)
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

    lower_prik_row = TextBoxRow(
        x=0,
        y=0,
        width=width,
        height=round(0.3 * combined_row_height),
        n=n_lower,
        align="text-top",
        texts=["prik hier"] * n_lower,
    )
    drawing.append(lower_prik_row)
    lower_cp_idx_row = TextBoxRow(
        x=0,
        y=lower_prik_row.height,
        width=width,
        height=round(0.1 * combined_row_height),
        n=n_lower,
        align="text-bottom",
        texts=[f"{etappe.idx}.{i}" for i in range(1, len(etappe) + 1)[-n_lower:]],
    )
    drawing.append(lower_cp_idx_row)
    lower_score_row = TextBoxRow(
        x=0,
        y=lower_prik_row.height + lower_cp_idx_row.height,
        width=width,
        height=round(0.1 * combined_row_height),
        n=n_lower,
        align="text-bottom",
        texts=[f"{cp.score} p" for cp in etappe[-n_lower:]],
    )
    drawing.append(lower_score_row)
    lower_hint_row = TextBoxRow(
        x=0,
        y=lower_prik_row.height + lower_cp_idx_row.height + lower_score_row.height,
        width=width,
        height=round(0.2 * combined_row_height),
        n=n_lower,
        align="text-bottom",
        texts=[f"{cp.hint}" for cp in etappe[-n_lower:]],
    )
    drawing.append(lower_hint_row)
    drawing.saveSvg("test.svg")


class Box(draw.Group):
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
        super().__init__(children=self._get_children())

    @abc.abstractmethod
    def _get_children(self) -> list[draw.DrawingBasicElement]:
        pass

    def to_drawing(self, width: int, height: int) -> draw.Drawing:
        assert width >= self.x + self.width
        assert height >= self.y + self.height
        canvas = draw.Drawing(width=width, height=width)
        canvas.append(self)
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
            self.x,
            self.y,
            self.width,
            self.height,
            fill="white",
            stroke="black",
            stroke_width=1,
        )
        match self.align:
            case "text-bottom":
                text_y = self.y + 1
            case "middle":
                text_y = self.y + round(self.height / 2)
            case "text-top":
                text_y = self.y + self.height - self.fontSize

        self.text = draw.Text(
            self.text,
            self.fontSize,
            x=self.x + self.width / 2,
            y=text_y,
            text_anchor="middle",
            dominant_baseline=self.align,
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
    CheckPoint(idx=1, score=1, hint="Onder de brug", coordinate=(23400, 23523)),
    CheckPoint(idx=2, score=2, hint="Paaltje", coordinate=(23444, 23523)),
    CheckPoint(idx=3, score=1, hint="Onder de brug", coordinate=(23400, 23523)),
    CheckPoint(idx=4, score=2, hint="Paaltje", coordinate=(23444, 23523)),
    CheckPoint(idx=5, score=1, hint="Onder de brug", coordinate=(23400, 23523)),
    CheckPoint(idx=6, score=2, hint="Paaltje", coordinate=(23444, 23523)),
    CheckPoint(idx=7, score=1, hint="Onder de brug", coordinate=(23400, 23523)),
    CheckPoint(idx=8, score=2, hint="Paaltje", coordinate=(23444, 23523)),
]
ref_etappe = Etappe(idx=idx, kind=kind, checkpoints=tuple(cps))

etappe_to_svg(etappe=ref_etappe)
