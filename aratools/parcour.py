import csv
import re
from collections.abc import Collection, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from aratools.latex import etappe_to_pdf
from aratools.coordinate import WKT_converter


def fix_gmaps_csv(fn: str | Path) -> list[str]:
    with open(fn) as f:
        lines = f.readlines()
    header = lines[0]
    assert header == "WKT,name,description,hidden\n"
    n_columns = 4
    new_lines = []
    new_l = ""
    while len(lines):
        line = lines.pop(0)
        new_l += line
        if new_l.count(",") == n_columns - 1:
            new_lines.append(new_l.strip().replace("\n", "") + "\n")
            new_l = ""
    return new_lines


@contextmanager
def csvreader(path: str | Path) -> Iterator[list[str]]:
    file_obj = open(Path(path), mode="r", newline="")
    reader = csv.reader(file_obj)
    try:
        yield reader  # type: ignore
    finally:
        file_obj.close()


class Parcour:
    def __init__(self, input_dir: str | Path):
        self.input_dir = Path(input_dir)
        assert self.input_dir.exists()
        self._process_teams_file()
        self._process_etappe_files()

    def _process_teams_file(self):
        # team names, single csv file, names only
        path = self.input_dir / "teams.csv"
        with csvreader(path) as reader:
            self.team_names = tuple(row[0] for row in reader)
        assert len(self.team_names)

    def _process_etappe_files(self):
        # etappe file should contain header with transport kind (kano, fiets, hardlopen)
        CP_FILE = re.compile(r"etappe_\d*\.csv$", re.IGNORECASE)
        paths = sorted(
            path for path in self.input_dir.iterdir() if CP_FILE.search(str(path))
        )
        assert len(paths)
        _etappes = tuple(sorted(Etappe.from_csv(path) for path in paths))
        self.etappes = {et.idx: et for et in _etappes}

    def generate_ponskaart_pdfs(self, path: str | Path):
        path = Path(path)
        for idx, etappe in self.etappes.items():
            etappe_to_pdf(etappe, self.team_names, path / f"Etappe_{idx}")


@dataclass(frozen=True)
class CheckPoint:
    idx: int
    score: int  # how many points scoring the cp is worth
    hint: str
    show: bool
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
        assert len(self.checkpoints)

    @classmethod
    def from_csv(cls, path: Path):
        reader = csv.DictReader(fix_gmaps_csv(path))
        return cls(
            # etappe_4_hardlopen.csv should result in idx 4
            idx=int(path.stem.split("_")[-2]),
            # and kind 'hardlopen'
            kind=path.stem.split("_")[-1],
            checkpoints=tuple(
                CheckPoint(
                    idx=i + 1,
                    score=int(line["score"]),
                    hint=str(line["hint"]),
                    show=bool(line["hidden"]),
                    coordinate=WKT_converter.to_amersfoort(line["WKT"]),
                )
                for i, line in enumerate(reader)
            ),
        )

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
