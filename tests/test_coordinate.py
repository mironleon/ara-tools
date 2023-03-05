import pytest

from aratools.coordinate import WKT_converter


# taken from https://www.nsgi.nl/documents/1888506/3754578/20220111+Lijst+actuele+kernnetpunten+voor+RDinfo.ods/ae6fecb4-e145-8d93-8a91-fc578dd18d52?t=1641991881508
# and converted with https://epsg.io/transform#s_srs=28992&t_srs=4326&x=NaN&y=NaN
@pytest.mark.parametrize(
    "long, lat, expected",
    (
        # Steen R.D. Westerpad Ameland
        (5.7581475, 53.4575106, (179641, 607984)),
        # Viaduct Koningsweg Arnhem
        (5.930493, 52.0383178, (192277, 450138)),
    ),
)
def test_wkt_converter(long, lat, expected):
    assert WKT_converter.to_amersfoort(long, lat) == expected
