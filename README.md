# Advent of Code

My solutions to [Advent of Code](https://adventofcode.com/) puzzles, written in Python.

## Repository layout

Solutions are organised by year and day:

```
<year>/<day>/
```

Two formats are used depending on the year:

- **Jupyter notebooks** (2021, 2023): each day has a `notebook.ipynb` with one cell per part,
  next to the puzzle input and the example input from the puzzle statement
  (`*_input.txt` / `*_input_test.txt`).
- **Standalone scripts** (2022): each day has a `script.py`, a `README.md` with the puzzle
  statement and the expected output, plus `simple_input.txt` (example) and
  `complex_input.txt` (real puzzle input).

## Progress

| Year | Days | Format |
|------|------|--------|
| [2021](2021) | [1](2021/01), [2](2021/02) | Notebooks |
| [2022](2022) | [13](2022/13), [14](2022/14), [15](2022/15) (day [12](2022/12) has the statement only) | Scripts |
| [2023](2023) | [1](2023/01) – [15](2023/15) | Notebooks |

## Requirements

- Python 3.10+ (some solutions use `itertools.pairwise`)
- Third-party packages used by some solutions: `numpy`, `pandas`, `regex`
- `jupyter` to run the notebooks

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy pandas regex jupyter
```

## Running the solutions

### Notebooks (2021, 2023)

Notebooks read their input with a relative path, so start Jupyter from the day's directory
(or open the notebook from there) and run all cells:

```bash
cd 2023/01
jupyter notebook notebook.ipynb
```

To run against the example input, change the file name in the `open(...)` call to the
`*_input_test.txt` file.

### Scripts (2022)

Scripts read from `input.txt` in the current directory. Copy the input you want to use,
then run the script:

```bash
cd 2022/13
cp complex_input.txt input.txt   # or simple_input.txt for the example
python3 script.py
```

Each day's `README.md` lists the expected output.

## Note on inputs

Puzzle inputs are committed next to each solution. Inputs are unique per account, so to solve
with your own, download it from the puzzle page and save it under the same file name.
