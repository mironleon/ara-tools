import shutil
import subprocess
from csv import writer
from pathlib import Path

from aratools.parcour import CheckPoint, Etappe, Parcour, fix_gmaps_csv

EXAMPLE_DIR = Path(__file__).absolute().parent / "example_data"
GMAP_DIR = Path(__file__).absolute().parent / "gmap_data"


def test_fix_gmap_csv():
    fixed_lines = fix_gmaps_csv(GMAP_DIR / "gmap_etappe.csv")
    assert fixed_lines == [
        "WKT,name,description,hidden\n",
        '"POINT (5.2652943 52.1516656)",Point 1,descritpion,1\n',
        '"POINT (5.3142177 52.1459776)",Point 2,description,0\n',
        '"POINT (5.2768814 52.1408683)",Point 3,mooi punt,0\n',
    ]


def test_parcour():
    parcour = Parcour(input_dir=EXAMPLE_DIR)
    assert len(parcour.etappes) == 2
    assert len(parcour.etappes[1]) == 10
    assert all(isinstance(cp, CheckPoint) for cp in parcour.etappes[1])
    assert parcour.etappes[1].kind == "hardlopen"
    assert parcour.etappes[2].kind == "fietsen"


def test_checkpoint_ordering():
    cp1 = CheckPoint(idx=1, score=1, hint="", show=True, coordinate=(0, 0))
    cp2 = CheckPoint(idx=2, score=1, hint="", show=False, coordinate=(0, 0))
    assert cp1 < cp2
    assert cp2 > cp1
    assert sorted([cp2, cp1]) == [cp1, cp2]


def test_etappe_from_csv(tmp_path):
    idx = 5
    kind = "Hardlopen"
    cp1 = CheckPoint(
        idx=1, score=1, hint="Onder de brug", show=True, coordinate=(23400, 23523)
    )
    cp2 = CheckPoint(
        idx=2, score=2, hint="Paaltje", show=False, coordinate=(23444, 23523)
    )
    etappe_fn = tmp_path / f"etappe_{idx}.csv"
    ref_etappe = Etappe(idx=idx, kind=kind, checkpoints=(cp1, cp2))
    with open(etappe_fn, "w") as f:
        csv_writer = writer(f)
        csv_writer.writerow([kind])
        csv_writer.writerow(
            [
                str(cp1.idx),
                str(cp1.score),
                str(cp1.hint),
                str(cp1.show).upper(),
                f"{cp1.coordinate[0]} {cp1.coordinate[1]}",
            ]
        )
        csv_writer.writerow(
            [
                str(cp2.idx),
                str(cp2.score),
                str(cp2.hint),
                str(cp2.show).upper(),
                f"{cp2.coordinate[0]} {cp2.coordinate[1]}",
            ]
        )
    etappe = Etappe.from_csv(etappe_fn)
    assert etappe == ref_etappe


def test_generate_pdfs():
    parcour = Parcour(input_dir=EXAMPLE_DIR)
    base_path = EXAMPLE_DIR / "pdfs"
    if base_path.exists():
        shutil.rmtree(base_path)
    base_path.mkdir()
    parcour.generate_ponskaart_pdfs(base_path)
    for idx in parcour.etappes:
        path = base_path / f"Etappe_{idx}.pdf"
        assert path.exists()
        subprocess.run(f"open {path}", shell=True, check=True)
