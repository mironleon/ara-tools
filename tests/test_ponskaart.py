from aratools.ponskaart import PonsKaart
from pathlib import Path


def test_ponskaart():
    PonsKaart(input_dir=Path(__file__).absolute().parent / "example_data")
