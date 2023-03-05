import pyproj


class WKT_converter:
    _amersfoort_transformer = pyproj.Transformer.from_crs(
        pyproj.CRS.from_string("EPSG:4326"),
        pyproj.CRS.from_string("EPSG:28992"),
        always_xy=False,
    )

    @classmethod
    def to_amersfoort(cls, longitude: float, latidude: float) -> tuple[int, int]:
        """
        Example input tuple from google mymaps exported kml:
        "(5.2652943 52.1516656)"

        Return tuple of rijksdriehoeks coordinaten, e.g.:
        (146657, 462617)
        """
        # longitude extents of the netherlands
        assert (
            longitude > 3.4 and longitude < 7
        ), f"WGS84 longitude out of bounds {longitude}"
        # latidude extents of the netherlands
        assert (
            latidude > 50.5 and latidude < 53.5
        ), f"WGS84 latitude out of bounds {latidude}"
        # pyproj returns coordinate tuple in y, x order for some reason
        # the units are in meters, so for our purposes we can round to
        # the nearest meter
        x, y = (
            round(c) for c in cls._amersfoort_transformer.transform(latidude, longitude)
        )
        km = int(1e3)
        # wikipedia says the extents of the amersfoort system are
        # x: [0, 280], y: [300, 625]
        assert x >= 0 and x <= 280 * km, f"X coordinate {x} out of bounds"
        assert y >= 300 * km and y <= 625 * km, f"Y coordinate {y} out of bounds"
        return x, y
