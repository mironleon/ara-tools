import re

import pyproj


class WKT_converter:
    _amersfoort_transformer = pyproj.Transformer.from_crs(
        pyproj.CRS.from_string("EPSG:4326"),
        pyproj.CRS.from_string("EPSG:28992"),
        always_xy=False,
    )

    _float_pattern = re.compile(r"\d*\.\d*")

    @classmethod
    def to_amersfoort(cls, wkt_str: str) -> tuple[int, int]:
        """
        Example input string from google mymaps exported CSV's:
        "# POINT (5.2652943 52.1516656)"

        Return tuple of rijksdriehoeks coordinaten, e.g.:
        (146657, 462617)
        """
        wkt_tuple = tuple(float(c) for c in cls._float_pattern.findall(wkt_str))
        assert len(wkt_tuple) == 2, f"Could not find two coordinates in {wkt_str}"
        # longitude extents of the netherlands
        assert (
            wkt_tuple[0] > 3.4 and wkt_tuple[0] < 7
        ), f"WGS84 longitude out of bounds {wkt_tuple[0]}"
        # latidude extents of the netherlands
        assert (
            wkt_tuple[1] > 50.5 and wkt_tuple[1] < 53.5
        ), f"WGS84 latitude out of bounds {wkt_tuple[1]}"
        # pyproj returns coordinate tuple in y, x order for some reason
        # the units are in meters, so for our purposes we can round to
        # the nearest meter
        x, y = (
            round(c)
            for c in cls._amersfoort_transformer.transform(wkt_tuple[1], wkt_tuple[0])
        )
        km = int(1e3)
        # wikipedia says the extents of the amersfoort system are x: [0, 280], y: [300, 625]
        assert x >= 0 and x <= 280 * km, f"X coordinate {x} out of bounds"
        assert y >= 300 * km and y <= 625 * km, f"Y coordinate {y} out of bounds"
        return x, y


print(WKT_converter.to_amersfoort("# POINT (5.2652943 52.1516656)"))
