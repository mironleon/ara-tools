from csv import writer
from pathlib import Path

from aratools.parcour import CheckPoint, Etappe, Parcour


def test_parcour():
    pons = Parcour(input_dir=Path(__file__).absolute().parent / "example_data")
    assert len(pons.etappes) == 2
    assert len(pons.etappes[1]) == 5
    assert all(isinstance(cp, CheckPoint) for cp in pons.etappes[1])
    assert pons.etappes[1].kind == "hardlopen"
    assert pons.etappes[2].kind == "fietsen"


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
