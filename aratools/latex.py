from aratools.parcour import Etappe, CheckPoint

from pylatex import Document, Tabularx, NoEscape, Tabular
from pylatex.utils import bold, italic
import subprocess


def etappe_to_pdf(etappe: Etappe, team_name: str):
    table_width = NoEscape("0.9 \paperwidth")
    row_height = "1.0"

    if len(etappe) % 2 == 0:
        n_upper = int(len(etappe) / 2)
        n_lower = n_upper
    else:
        n_upper = int(len(etappe) / 2) + 1
        n_lower = int(len(etappe) / 2)

    doc = Document(
        geometry_options={
            "margin": "0.5cm",
            "showframe": False,
            "paper": "a5paper",
            "landscape": True,
        },
    )
    doc.preamble.append(NoEscape(r"\usepackage{graphicx}"))

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
            [f"{etappe.idx}.{i}" for i in range(1, len(etappe) + 1)[:n_upper]]
        )
        table.add_hline()
        table.add_row([f"{cp.score} p" for cp in etappe[:n_upper]])
        table.add_hline()
        table.add_row([f"{cp.hint}" for cp in etappe[:n_upper]], mapper=italic)
        table.add_hline()
        table.add_row(
            ["\n".join(str(c) for c in cp.coordinate) for cp in etappe[:n_upper]],
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
            ["\n".join(str(c) for c in cp.coordinate) for cp in etappe[-n_lower:]],
            mapper=bold,
        )
        table.add_hline()
        table.add_row([f"{cp.hint}" for cp in etappe[-n_lower:]], mapper=italic)
        table.add_hline()
        table.add_row([f"{cp.score} p" for cp in etappe[-n_lower:]])
        table.add_hline()
        table.add_row(
            [f"{etappe.idx}.{i}" for i in range(1, len(etappe) + 1)[-n_lower:]]
        )
        table.add_hline()
        table.add_row(["prik hier" + 5 * "\n"] * n_lower)
        table.add_hline()
    doc.append(NoEscape("}"))

    doc.generate_pdf("test", clean_tex=False)


subprocess.run("rm test.pdf", shell=True)

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
    CheckPoint(idx=9, score=7, hint="Viaduct", coordinate=(23444, 23523)),
]
ref_etappe = Etappe(idx=idx, kind=kind, checkpoints=tuple(cps))

etappe_to_pdf(ref_etappe, team_name="1 - Het beste team van de hele wereld")

subprocess.run("open test.pdf", shell=True)
