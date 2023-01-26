from aratools.parcour import Etappe
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

    # squares for marking with prikker
    square_width_upper = round(width / n_upper)
    square_width_lower = round(width / n_lower)

    # middle line contains etappe number, etappe kind and team name
    middle_line_height = round(height / 15)

    # total height for upper and lower rows
    combined_row_height = round((height - middle_line_height) / 2)

    # TODO generate 'create row of text boxes'
    # lower rows
    low_row_background = draw.Rectangle(0, 0, width, combined_row_height, fill="red")
    # squares to prik with the prikker
    prik_squares = [
        draw.Rectangle(
            x=round(i * square_width_lower),
            y=0,
            width=square_width_lower,
            height=round(combined_row_height / 3),
            fill="white",
            stroke_width=1,
            stroke="black",
        )
        for i in range(n_lower)
    ]
    prik_text = [
        draw.Text(
            x=round((i + 0.3) * square_width_lower),
            y=0.8 * round(combined_row_height / 3),
            text="Prik Hier",
            fontSize=6,
        )
        for i in range(n_lower)
    ]
    #
    drawing.extend((low_row_background, *prik_squares, *prik_text))
    # middle row
    drawing.append(
        draw.Rectangle(0, combined_row_height, width, middle_line_height, fill="yellow")
    )
    etappe_name = draw.Text(
        text=f"Etappe {etappe.idx}", fontSize=8, x=0, y=round(height / 2)
    )
    etappe_kind = draw.Text(text=etappe.kind, fontSize=8, x="30%", y=round(height / 2))
    team_name = draw.Text(
        text="1 - Team BlaBla", fontSize=8, x="60%", y=round(height / 2)
    )
    drawing.extend((etappe_name, etappe_kind, team_name))
    # upper rows
    drawing.append(
        draw.Rectangle(
            0, height - combined_row_height, width, combined_row_height, fill="blue"
        )
    )
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


# idx = 5
# kind = "Hardlopen"
# cps = [
#     CheckPoint(idx=1, score=1, hint="Onder de brug", coordinate=(23400, 23523)),
#     CheckPoint(idx=2, score=2, hint="Paaltje", coordinate=(23444, 23523)),
#     CheckPoint(idx=3, score=1, hint="Onder de brug", coordinate=(23400, 23523)),
#     CheckPoint(idx=4, score=2, hint="Paaltje", coordinate=(23444, 23523)),
#     CheckPoint(idx=5, score=1, hint="Onder de brug", coordinate=(23400, 23523)),
#     CheckPoint(idx=6, score=2, hint="Paaltje", coordinate=(23444, 23523)),
#     CheckPoint(idx=7, score=1, hint="Onder de brug", coordinate=(23400, 23523)),
#     CheckPoint(idx=8, score=2, hint="Paaltje", coordinate=(23444, 23523)),
# ]
# ref_etappe = Etappe(idx=idx, kind=kind, checkpoints=tuple(cps))

# etappe_to_svg(etappe=ref_etappe)
