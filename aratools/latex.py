from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pylatex import Document, NewPage, NoEscape, Tabular, Tabularx, VerticalSpace
from pylatex.utils import bold, italic

if TYPE_CHECKING:
    from aratools.parcour import Etappe


def etappe_to_pdf(etappe: Etappe, team_names: tuple[str, ...], path: Path):
    """
    Create a PDF with a ponskaart for every team for 1 etappe
    """
    doc = Document(
        geometry_options={
            "margin": "0.2cm",
            "showframe": False,
            "paper": "a4paper",
            "landscape": False,
        },
    )
    doc.preamble.append(NoEscape(r"\usepackage{graphicx}"))
    doc.preamble.append(NoEscape(r"\renewcommand{\familydefault}{\sfdefault}"))
    n_teams = len(team_names)
    # even
    if n_teams % 2 == 0:
        team_names_tuples = [
            (team_names[i], team_names[i + 1]) for i in range(0, len(team_names), 2)
        ]
        last_team_name = None
    else:
        team_names_tuples = [
            (team_names[i], team_names[i + 1]) for i in range(0, len(team_names) - 1, 2)
        ]
        last_team_name = team_names[-1]
    # print(team_names_tuples)
    for team_name_pair in team_names_tuples:
        team_1, team_2 = team_name_pair
        add_table_page(etappe=etappe, team_name=team_1, doc=doc, add_new_page=False)
        add_table_page(etappe=etappe, team_name=team_2, doc=doc, add_new_page=True)
    if last_team_name:
        add_table_page(
            etappe=etappe, team_name=last_team_name, doc=doc, add_new_page=True
        )
    doc.generate_pdf(str(path), clean_tex=False)


def add_table_page(
    etappe: Etappe, team_name: str, doc: Document, add_new_page: bool = True
):
    """
    Add a table page representing a ponskaart to a document
    """
    table_width = NoEscape(r"0.9 \paperwidth")
    row_height = "1.0"

    if len(etappe) % 2 == 0:
        n_upper = int(len(etappe) / 2)
        n_lower = n_upper
    else:
        n_upper = int(len(etappe) / 2) + 1
        n_lower = int(len(etappe) / 2)
    doc.append(NoEscape("\n"))
    doc.append(VerticalSpace("0.5em"))
    doc.append(NoEscape(r"\resizebox{0.9 \paperwidth}{3 cm}{"))
    with doc.create(
        Tabularx(
            "|X" * n_upper + "|",
            width_argument=table_width,
            row_height=row_height,
        )
    ) as table:
        table.add_hline()
        table.add_row(["prik hier" + 5 * "\n"] * n_upper)
        table.add_hline()
        table.add_row(
            [f"{etappe.idx}.{i}" for i in range(1, len(etappe) + 1)[:n_upper]],
            mapper=bold,
        )
        table.add_hline()
        table.add_row([f"{cp.score} p" for cp in etappe[:n_upper]])
        table.add_hline()
        table.add_row([f"{cp.hint}" for cp in etappe[:n_upper]], mapper=italic)
        table.add_hline()
        table.add_row(
            [
                "\n".join(str(c) for c in cp.coordinate) if cp.hidden else "Zie kaart"
                for cp in etappe[:n_upper]
            ],
            mapper=bold,
        )
        table.add_hline()
    doc.append(NoEscape("}"))

    doc.append(NoEscape("\n"))

    doc.append(NoEscape(r"\Large"))

    doc.append(NoEscape(r"\resizebox{0.9 \paperwidth}{1 cm}{"))
    with doc.create(
        Tabular(
            "|c" * 3 + "|",
        )
    ) as table:
        table.add_hline()
        table.add_row([f"Etappe {etappe.idx}", etappe.kind, team_name], mapper=bold)
        table.add_hline()
    doc.append(NoEscape("}"))

    doc.append(NoEscape(r"\normalsize"))

    doc.append(NoEscape("\n"))

    doc.append(NoEscape(r"\resizebox{0.9 \paperwidth}{3 cm}{"))
    with doc.create(
        Tabularx(
            "|X" * n_lower + "|",
            width_argument=table_width,
            row_height=row_height,
        )
    ) as table:
        table.add_hline()
        table.add_row(
            [
                "\n".join(str(c) for c in cp.coordinate) if cp.hidden else "Zie kaart"
                for cp in etappe[-n_lower:]
            ],
            mapper=bold,
        )
        table.add_hline()
        table.add_row([f"{cp.hint}" for cp in etappe[-n_lower:]], mapper=italic)
        table.add_hline()
        table.add_row([f"{cp.score} p" for cp in etappe[-n_lower:]])
        table.add_hline()
        table.add_row(
            [f"{etappe.idx}.{i}" for i in range(1, len(etappe) + 1)[-n_lower:]],
            mapper=bold,
        )
        table.add_hline()
        table.add_row(["prik hier" + 5 * "\n"] * n_lower)
        table.add_hline()
    doc.append(NoEscape("}"))
    doc.append(NoEscape("\n"))
    doc.append(VerticalSpace("2.5em"))

    if add_new_page:
        doc.append(NewPage())
