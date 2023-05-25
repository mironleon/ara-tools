import csv
from collections.abc import Collection, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from fastkml import kml

from aratools.coordinate import WKT_converter
from aratools.latex import etappe_to_pdf


@contextmanager
def csvreader(path: str | Path) -> Iterator[list[str]]:
    file_obj = open(Path(path), mode="r", newline="")
    reader = csv.reader(file_obj)
    try:
        yield reader  # type: ignore
    finally:
        file_obj.close()


class Parcour:
    """
    Object representing adventure race parcour, built from a list of participating teams
    and a KML file representing etappes with checkpoints
    """

    def __init__(self, team_csv_path: str | Path, etappe_kml_path: str | Path):
        self._process_teams_file(team_csv_path)
        self._process_etappes_kml(etappe_kml_path)

    def _process_teams_file(self, path: str | Path):
        # team names, single csv file, names only
        path = Path(path).resolve()
        assert path.suffix == ".csv"
        with csvreader(path) as reader:
            self.team_names = tuple(row[0] for row in reader)
        assert len(self.team_names)

    def _process_etappes_kml(self, path: str | Path):
        path = Path(path).resolve()
        assert path.suffix == ".kml"
        with open(path, "rb") as f:
            kml_str = f.read()
        k = kml.KML()
        k.from_string(kml_str)
        doc = list(k.features())[0]
        folders = doc.features()
        _etappes = tuple(Etappe.from_kml_folder(f) for f in folders)
        self.etappes = {et.idx: et for et in _etappes}

    def generate_ponskaart_pdfs(self, path: str | Path):
        """
        Generate a 1 a3 landscape pdf file per etappe, containing
        ponskaarts for all the teams
        """
        path = Path(path)
        for idx, etappe in self.etappes.items():
            etappe_to_pdf(etappe, self.team_names, path / f"Etappe_{idx}")


@dataclass(frozen=True)
class CheckPoint:
    idx: int
    score: int  # how many points scoring the cp is worth
    hint: str
    hidden: bool
    coordinate: tuple[
        int, int
    ]  # https://nl.wikipedia.org/wiki/Rijksdriehoeksco%C3%B6rdinaten

    def __lt__(self, other):
        return self.idx < other

    def __gt__(self, other):
        return self.idx > other


@dataclass(frozen=True)
class Etappe(Collection[CheckPoint]):
    idx: int
    kind: str  # fietsen, kano, run-bike
    checkpoints: tuple[CheckPoint, ...]

    def __post_init__(self):
        assert tuple(sorted(self.checkpoints)) == self.checkpoints
        # need at least 1 cp on the upper row and 1 on the lower row
        assert len(self.checkpoints) > 1

    @classmethod
    def from_kml_folder(cls, folder: kml.Folder):
        name = folder.name
        # etappe_4_hardlopen should result in idx 4
        idx = int(name.split("_")[-2])
        # and kind 'hardlopen'
        kind = name.split("_")[-1]
        cps = []
        for i, placemark in enumerate(folder.features()):
            cp_data = {
                e.name.lower(): e.value for e in placemark.extended_data.elements
            }
            point = placemark.geometry
            cps.append(
                CheckPoint(
                    idx=i + 1,
                    score=int(float(cp_data["score"])),
                    hint=str(cp_data["hint"]),
                    hidden=bool(cp_data["hidden"]),
                    coordinate=WKT_converter.to_amersfoort(point.x, point.y),
                )
            )
        return cls(idx=idx, kind=kind, checkpoints=tuple(cps))

    def __lt__(self, other) -> bool:
        return bool(self.idx < other)

    def __gt__(self, other) -> bool:
        return bool(self.idx > other)

    def __len__(self) -> int:
        return len(self.checkpoints)

    def __iter__(self) -> Iterator[CheckPoint]:
        return iter(self.checkpoints)

    def __getitem__(self, key) -> CheckPoint:
        return self.checkpoints[key]

    def __contains__(self, __x: object) -> bool:
        return bool(__x in self.checkpoints)
