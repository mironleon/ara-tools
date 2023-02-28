from pathlib import Path

from aratools.csv import fix_gmaps_csv

GMAP_DIR = Path(__file__).absolute().parent / "gmap_data"


def test_fix_gmap_csv():
    fixed_lines = fix_gmaps_csv(GMAP_DIR / "gmap_etappe.csv")
    assert fixed_lines == [
        "WKT,name,description,hidden\n",
        '"POINT (5.2652943 52.1516656)",Point 1,descritpion,1\n',
        '"POINT (5.3142177 52.1459776)",Point 2,description,0\n',
        '"POINT (5.2768814 52.1408683)",Point 3,mooi punt,0\n',
    ]
