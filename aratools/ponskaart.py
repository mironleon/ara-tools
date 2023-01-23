import csv
from pathlib import Path
import re
from contextlib import contextmanager
from collections.abc import Iterator
from dataclasses import dataclass


@contextmanager
def csvreader(path: str | Path) -> Iterator[list[str]]:
    file_obj = open(Path(path), mode="r", newline="")
    reader = csv.reader(file_obj)
    try:
        yield reader  # type: ignore
    finally:
        file_obj.close()


class PonsKaart:
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
        assert len(self.team_names > 0)

    def _process_etappe_files(self):
        # etappe file should contain header with transport kind (kano, fiets, hardlopen)
        CP_FILE = re.compile(r"cp_etappe_\d*\.csv$", flag=re.IGNORECASE)
        paths = sorted(
            path for path in self.input_dir.iterdir() if CP_FILE.match(str(path))
        )
        _etappes = tuple(Etappe.from_csv(path) for path in paths)
        self.etappes = {et.idx: et for et in _etappes}


@dataclass(frozen=True)
class CheckPoint:
    idx: int
    score: int  # how many points scoring the cp is worth
    hint: str
    coordinate: tuple[
        int, int
    ]  # https://nl.wikipedia.org/wiki/Rijksdriehoeksco%C3%B6rdinaten

    def __lt__(self, other):
        return self.idx < other


@dataclass(frozen=True)
class Etappe:
    idx: int
    kind: str  # fietsen, kano, run-bike
    checkpoints: tuple[CheckPoint, ...]

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

    def __lt__(self, other):
        return self.idx < other
