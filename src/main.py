"""Modules 3 and 4: console menu and the comparison runner.

Run with:  python src/main.py
"""
import copy

from algorithms import (linear_search, merge_sort, selection_sort,
                        insertion_sort, bubble_sort, quick_sort)
from inputs import ask_for_list, ask_for_target
from display import show_list, show_single, show_all

MENU = """
==============================================
 Comparison Count Analysis of Search and Sorting
==============================================
 1. Linear Search
 2. Merge Sort
 3. Selection Sort
 4. Insertion Sort
 5. Bubble Sort
 6. Quick Sort
 7. All of the above
 8. Exit
----------------------------------------------"""

SORT_OPTIONS = {
    "2": ("Merge Sort", merge_sort),
    "3": ("Selection Sort", selection_sort),
    "4": ("Insertion Sort", insertion_sort),
    "5": ("Bubble Sort", bubble_sort),
    "6": ("Quick Sort", quick_sort),
}


def run_linear(data, target):
    index, count = linear_search(data, target)
    if index == -1:
        lines = ["Target " + str(target) + " was not found."]
    else:
        lines = ["Target " + str(target) + " found at index " + str(index) + "."]
    show_single("Linear Search", len(data), count, ["Input:  " + show_list(data)] + lines)


def run_sort(name, func, data):
    result, count = func(copy.copy(data))
    lines = ["Input:  " + show_list(data), "Sorted: " + show_list(result)]
    if result != sorted(data):
        lines.append("WARNING: result does not match Python's sorted().")
    show_single(name, len(data), count, lines)


def run_all(data, target):
    """Option 7. Every algorithm gets its own copy of the same list."""
    print("\nInput:  " + show_list(data))
    print("Target: " + str(target))
    results = []

    index, count = linear_search(copy.copy(data), target)
    note = "found at " + str(index) if index != -1 else "not found"
    results.append(("Linear Search", count, note))

    expected_sorted = sorted(data)
    for name, func in [("Merge Sort", merge_sort), ("Selection Sort", selection_sort),
                       ("Insertion Sort", insertion_sort), ("Bubble Sort", bubble_sort),
                       ("Quick Sort", quick_sort)]:
        out, count = func(copy.copy(data))
        results.append((name, count, "sorted OK" if out == expected_sorted else "WRONG"))
    show_all(len(data), results)


def get_choice():
    """Read a menu choice. Only 1 to 8 are accepted."""
    while True:
        choice = input("Choose an option (1-8): ").strip()
        if choice in {"1", "2", "3", "4", "5", "6", "7", "8"}:
            return choice
        print("  Invalid choice '" + choice + "'. Please type a number from 1 to 8.")


def main():
    while True:
        print(MENU)
        choice = get_choice()
        if choice == "8":
            print("Goodbye.")
            return
        data = ask_for_list()
        if choice == "1":
            run_linear(data, ask_for_target())
        elif choice == "7":
            run_all(data, ask_for_target())
        else:
            name, func = SORT_OPTIONS[choice]
            run_sort(name, func, data)
        input("\nPress Enter to return to the menu...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
