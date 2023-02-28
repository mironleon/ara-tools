from pathlib import Path


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
