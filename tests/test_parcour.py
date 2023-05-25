import shutil
import subprocess
from pathlib import Path

from aratools.parcour import CheckPoint, Parcour

EXAMPLE_DIR = Path(__file__).absolute().parent / "example_data"


def test_parcour():
    parcour = Parcour(
        team_csv_path=EXAMPLE_DIR / "teams.csv",
        etappe_kml_path=EXAMPLE_DIR / "test_map.kml",
    )
    assert len(parcour.etappes) == 7
    assert len(parcour.etappes[1]) == 3
    assert all(isinstance(cp, CheckPoint) for cp in parcour.etappes[1])
    assert parcour.etappes[1].kind == "fietsen"
    assert parcour.etappes[2].kind == "hardlopen"


def test_checkpoint_ordering():
    cp1 = CheckPoint(idx=1, score=1, hint="", hidden=True, coordinate=(0, 0))
    cp2 = CheckPoint(idx=2, score=1, hint="", hidden=False, coordinate=(0, 0))
    assert cp1 < cp2
    assert cp2 > cp1
    assert sorted([cp2, cp1]) == [cp1, cp2]


def test_generate_pdfs():
    parcour = Parcour(
        team_csv_path=EXAMPLE_DIR / "teams.csv",
        etappe_kml_path=EXAMPLE_DIR / "test_map.kml",
    )
    base_path = EXAMPLE_DIR / "pdfs"
    if base_path.exists():
        shutil.rmtree(base_path)
    base_path.mkdir()
    parcour.generate_ponskaart_pdfs(base_path)
    for idx in parcour.etappes:
        path = base_path / f"Etappe_{idx}.pdf"
        assert path.exists()
        subprocess.run(f"open {path}", shell=True, check=True)
