"""Expected comparison counts (best, average, worst) from the proposal table.

Everything here returns a number so it can be printed next to measured counts.
"""
import math


def _log2(n):
    return math.log2(n) if n > 1 else 0.0


def expected(name, n):
    """Return (best, average, worst) as floats for an input of size n."""
    if n < 2 and name != "Linear Search":
        return (0.0, 0.0, 0.0)
    pairs = n * (n - 1) / 2
    if name == "Linear Search":
        return (1.0, n / 2, float(n))
    if name == "Merge Sort":
        return ((n * _log2(n)) / 2, n * _log2(n), n * _log2(n) - n + 1)
    if name == "Selection Sort":
        return (pairs, pairs, pairs)
    if name == "Insertion Sort":
        return (float(n - 1), n * n / 4, pairs)
    if name == "Bubble Sort":
        return (float(n - 1), n * n / 2, pairs)
    if name == "Quick Sort":
        return (n * _log2(n), n * _log2(n), pairs)
    raise ValueError("unknown algorithm: " + name)


def formula_text(name):
    """Short text version of the three formulas for the report and the menu."""
    table = {
        "Linear Search": ("1", "n/2", "n"),
        "Merge Sort": ("(n log2 n)/2", "n log2 n", "n log2 n - n + 1"),
        "Selection Sort": ("n(n-1)/2", "n(n-1)/2", "n(n-1)/2"),
        "Insertion Sort": ("n-1", "n^2/4", "n(n-1)/2"),
        "Bubble Sort": ("n-1", "n^2/2", "n(n-1)/2"),
        "Quick Sort": ("n log2 n", "n log2 n", "n(n-1)/2"),
    }
    return table[name]
