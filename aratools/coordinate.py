import pyproj

crs_amersfoort = pyproj.CRS.from_string("EPSG:28992")
crs_google = pyproj.CRS.from_string("EPSG:4326")

transformer_amersfoort_google = pyproj.Transformer.from_crs(
    crs_amersfoort, crs_google, always_xy=False
)
transformer_google_amersfoort = pyproj.Transformer.from_crs(
    crs_google, crs_amersfoort, always_xy=False
)

print(transformer_google_amersfoort.transform(52.1516656, 5.2652943))


def WKT_to_amersfoort(wkt_str: str) -> tuple[int, int]:
    # POINT (5.2652943 52.1516656)
    wkt_str = wkt_str[wkt_str.index("(") :]
    wkt_tuple = eval(wkt_str.replace(" ", ","))
    assert (
        isinstance(wkt_tuple, tuple)
        and len(wkt_tuple) == 2
        and all(isinstance(d, float) for d in wkt_tuple)
    )
    return transformer_google_amersfoort.transform(wkt_tuple[1], wkt_tuple[0])


print(WKT_to_amersfoort("# POINT (5.2652943 52.1516656)"))
