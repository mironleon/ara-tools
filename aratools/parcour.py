import csv
import re
from collections.abc import Collection, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path


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


@dataclass(frozen=True)
class CheckPoint:
    idx: int
    score: int  # how many points scoring the cp is worth
    hint: str
    # TODO some cp's should not show coordinate, add 'hidden' attribute?
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
        # etappe_4.csv should result in idx 4
        idx = int(path.stem.split("_")[-1])
        with csvreader(path) as reader:
            # header line should contain kind of etappe (fietsen, kano, run-bike)
            kind = next(reader)[0]
            cps = tuple(
                CheckPoint(
                    idx=int(row[0]),
                    score=int(row[1]),
                    hint=row[2],
                    coordinate=(int(row[3].split()[0]), int(row[3].split()[1])),
                )
                for row in reader
            )
        return cls(idx=idx, kind=kind, checkpoints=cps)

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
