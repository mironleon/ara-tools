# ara-tools

Tools for organising the Amsterdam Adventure Race. Generates printable landscape A3 ponskaart pdfs via [pylatex](https://github.com/JelteF/PyLaTeX)

See example [pdf](tests/example_data/pdfs/Etappe_1.pdf)

## Generating ponskaart PDFS

You will need to generate two kinds of csv files:
    - 1 csv file per etappe describing coordinates, hints, etc.
    - 1 csv file listing the team names

### Etappe file example

First line describes what 'kind' of etappe it is, all following lines describe a checkpoint. Each row consists of IDX, SCORE, HINT, SHOW_COORDINATE, COORDINATE.

For now the coordinate is already expected to be in [rijksdriehoekscoordinaten](https://nl.wikipedia.org/wiki/Rijksdriehoeksco%C3%B6rdinaten), a single space separated string `Longitude Latidude`

```csv
hardlopen
1,2,bankje,TRUE,51050 62500
2,10,brug,TRUE,50030 655056
3,1,boom,FALSE,50051 65503
4,5,zwemmen,TRUE,50250 65300
5,15,paaltje,TRUE,50050 65200
6,2,bankje om op te zitten,TRUE,51050 62500
7,10,brug,TRUE,50030 655056
8,1,boom,FALSE,50051 65503
9,5,zwemmen in de zee,TRUE,50250 65300
10,15,paaltje,TRUE,50050 65200
```

### Team names

On team name per row. While the code handles very long team names gracefully, it is recommended to limit the names to a sensible 50 characters or so

```csv
blabalteam
halloteam
team de gekke konijnen
adventure aces
```

## Installing and running locally

### Ubuntu

```bash
git clone git@github.com:mironleon/aratools.git
cd aratools
pip install .
sudo apt-get install texlive-pictures texlive-science texlive-latex-extra latexmk
```

In a python shell, notebook or file

```python
from aratools.parcour import Parcour
from pathlib import Path

INPUT_DATA = Path().home() / 'input_csvs'
parcour = Parcour(INPUT_DATA)
OUTPUT = Path().home() / 'output_pdfs'
OUTPUT.mkdir(exist_ok=True)
parcour.generate_ponskaart_pdfs(OUTPUT)
```

### Windows

No idea, probably WSL <https://ubuntu.com/wsl> (untested)

## Running on binder

The easiest way, start the notebook on binder, upload your csv files in the notebook environment and follow the instructions in the notebook.

Note that it may take several minutes for the notebook to start

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mironleon/aratools/main?urlpath=tree)

## Planned features

- Allow using [WGS84](https://wiki.gis.com/wiki/index.php/WGS84) coordinates (googles maps standard) and convert to rijksdriehoeks
- Provide sample google sheets template with data validation
- Provide guide for exporting csvs from google maps
