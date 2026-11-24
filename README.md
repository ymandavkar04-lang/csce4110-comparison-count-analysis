# Comparison Count Analysis of Search and Sorting Algorithms

CSCE 4110 Algorithms, Final Project (Fall 2026)

**Author:** Yash Mandavkar (individual project)

## What this project does

Big-O tells you how an algorithm grows, but not what the actual count looks
like on a given input. This program counts the comparisons that Linear Search,
Merge Sort, Selection Sort, Insertion Sort, Bubble Sort, and Quick Sort really
make, and puts the measured number next to the expected best, average, and
worst case for that input size.

It answers two questions:

1. Same algorithm, different input: how does the count change for random,
   sorted, reverse sorted, nearly sorted, and duplicate-heavy lists?
2. Same input, different algorithm: how do the six algorithms compare on one list?

Details that matter for the counts:

* Bubble Sort stops early when a pass makes no swaps.
* Quick Sort uses the first element as the pivot (so sorted input is its worst case).
* Only comparisons between data values are counted, not index checks.

## Dependencies

* Python 3.8 or newer
* The menu program and the tests use only the standard library.
* `matplotlib` is only needed for the charts made by `experiments.py`.

## Setup

```
git clone <this repository's URL>
cd <repository folder>
pip install -r requirements.txt     # only needed for the charts
```

## How to run

Menu program:

```
python src/main.py
```

Tests (32 tests):

```
python -m unittest discover -s tests -v
```

Experiments (writes CSV files and charts into `results/`):

```
python src/experiments.py
```

## Using the menu

```
 1. Linear Search     5. Bubble Sort
 2. Merge Sort        6. Quick Sort
 3. Selection Sort    7. All of the above
 4. Insertion Sort    8. Exit
```

After you pick 1 to 7 the program asks for a list. You can type or paste
numbers separated by commas, or use a generator shortcut:

```
gen <kind> <size>      kinds: random, sorted, reverse, nearly, duplicates
```

Options 1 and 7 also ask for a number to search for. Bad input (letters, empty
entries, a menu choice outside 1 to 8, sizes above 5000) is rejected and you
are asked again.

### Example session

```
Choose an option (1-8): 7
Enter numbers separated by commas (or 'gen random 100'): 5, 3, 9, 1, 7, 2
Enter the number to search for: 7

Input:  [5, 3, 9, 1, 7, 2]
Target: 7

+----------------+----------+------+---------+-------+------------+
| Algorithm      | Measured | Best | Average | Worst | Result     |
+----------------+----------+------+---------+-------+------------+
| Linear Search  |        5 |    1 |       3 |     6 | found at 4 |
| Merge Sort     |       10 |  7.8 |    15.5 |  10.5 |  sorted OK |
| Selection Sort |       15 |   15 |      15 |    15 |  sorted OK |
| Insertion Sort |       12 |    5 |       9 |    15 |  sorted OK |
| Bubble Sort    |       15 |    5 |      18 |    15 |  sorted OK |
| Quick Sort     |        8 | 15.5 |    15.5 |    15 |  sorted OK |
+----------------+----------+------+---------+-------+------------+
```

The "Best / Average / Worst" columns come straight from the proposal formulas
(`src/theory.py`). They are leading-term estimates, so for tiny lists like this
one they can look odd (for example the Merge Sort average is bigger than its
worst case). They line up much better as n grows, which is what the experiments
show.

## Project layout

```
src/
  algorithms.py    the six algorithms, each returning its comparison count
  theory.py        expected best / average / worst formulas
  generators.py    the five input types (random, sorted, reverse, nearly, duplicates)
  inputs.py        parsing and validation of what the user types
  display.py       text tables
  main.py          console menu and the option 7 runner
  experiments.py   runs every algorithm on every input type at n = 10, 100, 1000
tests/
  test_algorithms.py   correctness, edge cases, hand-traced and formula checks
results/
  counts.csv, linear_search.csv, and three charts (PNG)
```

## Sample data

No outside datasets are used. All inputs are typed in or made by the
generators in `src/generators.py`, which use fixed seeds so results can be
repeated.
