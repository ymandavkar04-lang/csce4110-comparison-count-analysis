"""Experiments: comparison counts for every algorithm, input type, and size.

Run with:  python src/experiments.py
Writes results/counts.csv and, if matplotlib is installed, a few charts.
Random-style inputs (random, nearly, duplicates) are averaged over TRIALS runs.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from algorithms import SORTS, linear_search
from generators import INPUT_TYPES, make_input
from theory import expected
from display import table, fmt

SIZES = [10, 100, 1000]
TRIALS = 20
RANDOMIZED = {"random", "nearly", "duplicates"}
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def average_count(func, kind, n):
    trials = TRIALS if kind in RANDOMIZED else 1
    total = 0
    for seed in range(trials):
        data = make_input(kind, n, seed=seed)
        result, count = func(data)
        assert result == sorted(data)
        total += count
    return total / trials


def run_all():
    rows = []
    for name, func in SORTS.items():
        for kind in INPUT_TYPES:
            for n in SIZES:
                best, avg, worst = expected(name, n)
                rows.append({"algorithm": name, "input_type": kind, "n": n,
                             "measured": round(average_count(func, kind, n), 1),
                             "best": round(best, 1), "average": round(avg, 1),
                             "worst": round(worst, 1)})
    return rows


def linear_rows():
    """Linear search: target at start, middle, end, missing, plus random average."""
    rows = []
    for n in SIZES:
        data = list(range(1, n + 1))
        cases = [("start", 1), ("middle", (n + 1) // 2), ("end", n), ("missing", 0)]
        for label, target in cases:
            rows.append({"n": n, "target": label, "measured": linear_search(data, target)[1]})
        # average over every possible present target
        total = sum(linear_search(data, t)[1] for t in data)
        rows.append({"n": n, "target": "average (all present)", "measured": total / n})
    return rows


def save_csv(rows, name):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def print_tables(rows):
    for n in SIZES:
        print("\nn = " + str(n) + "  (measured comparisons)")
        headers = ["Algorithm"] + INPUT_TYPES
        out = []
        for name in SORTS:
            line = [name]
            for kind in INPUT_TYPES:
                match = [r for r in rows if r["algorithm"] == name and r["input_type"] == kind and r["n"] == n][0]
                line.append(fmt(match["measured"]))
            out.append(line)
        print(table(headers, out))


def make_charts(rows):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed, skipping charts.")
        return
    colors = {"Merge Sort": "#1b6ca8", "Selection Sort": "#7a7a7a", "Insertion Sort": "#2e8b57",
              "Bubble Sort": "#d1862b", "Quick Sort": "#b03a48"}

    def get(name, kind, n):
        return [r for r in rows if r["algorithm"] == name and r["input_type"] == kind and r["n"] == n][0]["measured"]

    # Chart 1: n = 1000, grouped bars, log scale
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    width = 0.15
    for i, name in enumerate(SORTS):
        vals = [get(name, kind, 1000) for kind in INPUT_TYPES]
        xs = [j + (i - 2) * width for j in range(len(INPUT_TYPES))]
        ax.bar(xs, vals, width, label=name, color=colors[name])
    ax.set_xticks(range(len(INPUT_TYPES)))
    ax.set_xticklabels(INPUT_TYPES)
    ax.set_yscale("log")
    ax.set_ylabel("comparisons (log scale)")
    ax.set_xlabel("input type")
    ax.set_title("Comparisons by algorithm and input type, n = 1000")
    ax.set_ylim(100, 5_000_000)
    ax.legend(fontsize=8, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart_by_input_n1000.png"), dpi=200)
    plt.close(fig)

    # Chart 2: growth with n on random input, log-log, with n log n and n^2/4 guides
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    sizes = [10, 30, 100, 300, 1000, 3000]
    for name, func in SORTS.items():
        ys = [average_count(func, "random", n) for n in sizes]
        ax.plot(sizes, ys, marker="o", label=name, color=colors[name])
    import math
    ax.plot(sizes, [n * math.log2(n) for n in sizes], "k--", linewidth=1, label="n log2 n")
    ax.plot(sizes, [n * n / 4 for n in sizes], "k:", linewidth=1, label="n^2 / 4")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("input size n")
    ax.set_ylabel("comparisons")
    ax.set_title("Growth of comparison count on random input")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart_growth_random.png"), dpi=200)
    plt.close(fig)

    # Chart 3: insertion vs quick, n = 1000, linear scale, to show the input sensitivity
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8))
    for ax, name in zip(axes, ["Insertion Sort", "Quick Sort"]):
        vals = [get(name, kind, 1000) for kind in INPUT_TYPES]
        ax.bar(INPUT_TYPES, vals, color=colors[name])
        ax.set_title(name + ", n = 1000")
        ax.set_ylabel("comparisons")
        ax.tick_params(axis="x", labelrotation=30)
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart_input_sensitivity.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    data_rows = run_all()
    print("saved " + save_csv(data_rows, "counts.csv"))
    print("saved " + save_csv(linear_rows(), "linear_search.csv"))
    print_tables(data_rows)
    make_charts(data_rows)
