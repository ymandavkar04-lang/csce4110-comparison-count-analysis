"""Module 6: tests. Run with:  python -m unittest discover -s tests -v

Covers correctness, edge cases, hand-traced counts, and the count claims
from the proposal (selection constant, insertion and bubble best/worst,
merge sort bounds, quick sort best/worst with a first-element pivot).
"""
import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from algorithms import (linear_search, merge_sort, selection_sort,
                        insertion_sort, bubble_sort, quick_sort, SORTS)
from generators import make_input, INPUT_TYPES
from inputs import parse_list, parse_generator, parse_number, InputError, MAX_SIZE
from theory import expected


def pairs(n):
    return n * (n - 1) // 2


class TestSortCorrectness(unittest.TestCase):
    EDGE_CASES = [
        [],
        [7],
        [2, 1],
        [1, 2],
        [3, 3, 3, 3],
        [5, 1, 5, 1, 5],
        [-3, 0, 2, -8, 7],
        [1.5, 0.5, 2.25, -1.0],
    ]

    def test_edge_cases(self):
        for name, func in SORTS.items():
            for case in self.EDGE_CASES:
                with self.subTest(algorithm=name, case=case):
                    original = list(case)
                    result, _ = func(case)
                    self.assertEqual(result, sorted(case))
                    self.assertEqual(case, original, "input list was modified")

    def test_all_input_types_and_sizes(self):
        for name, func in SORTS.items():
            for kind in INPUT_TYPES:
                for n in (10, 100, 1000):
                    with self.subTest(algorithm=name, kind=kind, n=n):
                        data = make_input(kind, n, seed=n)
                        result, _ = func(data)
                        self.assertEqual(result, sorted(data))

    def test_many_random_lists(self):
        rng = random.Random(4110)
        for _ in range(200):
            n = rng.randint(0, 60)
            data = [rng.randint(-20, 20) for _ in range(n)]
            for name, func in SORTS.items():
                result, _ = func(data)
                self.assertEqual(result, sorted(data), name)


class TestLinearSearch(unittest.TestCase):
    DATA = [10, 20, 30, 40, 50]

    def test_target_at_start(self):
        self.assertEqual(linear_search(self.DATA, 10), (0, 1))

    def test_target_in_middle(self):
        self.assertEqual(linear_search(self.DATA, 30), (2, 3))

    def test_target_at_end(self):
        self.assertEqual(linear_search(self.DATA, 50), (4, 5))

    def test_target_missing(self):
        self.assertEqual(linear_search(self.DATA, 99), (-1, 5))

    def test_empty_list(self):
        self.assertEqual(linear_search([], 1), (-1, 0))

    def test_duplicates_returns_first(self):
        self.assertEqual(linear_search([4, 9, 9, 9], 9), (1, 2))


class TestHandTracedCounts(unittest.TestCase):
    """Small examples I worked out on paper first."""

    def test_selection_sort_example(self):
        # n = 4 always 6 comparisons
        self.assertEqual(selection_sort([4, 3, 2, 1])[1], 6)
        self.assertEqual(selection_sort([1, 2, 3, 4])[1], 6)

    def test_insertion_sort_example(self):
        # [3,1,2]: key 1 compares with 3 (1 compare, shifts, j hits -1).
        #          key 2 compares with 3 (shift) then with 1 (stop) = 2 compares.
        self.assertEqual(insertion_sort([3, 1, 2])[1], 3)

    def test_bubble_sort_example(self):
        # [2,1,3]: pass 1 has 2 compares (swap once), pass 2 has 1 compare, no swap, stop.
        self.assertEqual(bubble_sort([2, 1, 3])[1], 3)

    def test_merge_sort_example(self):
        # [2,1,4,3]: merge [2],[1] = 1, merge [4],[3] = 1, merge [1,2],[3,4] = 2
        self.assertEqual(merge_sort([2, 1, 4, 3])[1], 4)
        # sorted [1,2,3,4]: 1 + 1 + 2 = 4 ; reverse [4,3,2,1]: 1 + 1 + 2 = 4
        # [1,3,2,4] merge [1],[3]=1, [2],[4]=1, [1,3],[2,4]: 1<=2, 3>2, 3<=4 then right left over = 3
        self.assertEqual(merge_sort([1, 3, 2, 4])[1], 5)

    def test_quick_sort_example(self):
        # [3,1,2]: pivot 3, 2 compares -> [2,1] then [3]; pivot 2 on [2,1], 1 compare. Total 3.
        self.assertEqual(quick_sort([3, 1, 2])[1], 3)
        # [2,1,3]: pivot 2, 2 compares, pieces [1] and [3] need none. Total 2.
        self.assertEqual(quick_sort([2, 1, 3])[1], 2)


class TestSixItemExample(unittest.TestCase):
    """The list [5, 3, 9, 1, 7, 2] traced by hand (used in the report too)."""
    DATA = [5, 3, 9, 1, 7, 2]

    def test_counts(self):
        self.assertEqual(linear_search(self.DATA, 7), (4, 5))
        self.assertEqual(merge_sort(self.DATA)[1], 10)
        self.assertEqual(selection_sort(self.DATA)[1], 15)
        self.assertEqual(insertion_sort(self.DATA)[1], 12)
        self.assertEqual(bubble_sort(self.DATA)[1], 15)
        self.assertEqual(quick_sort(self.DATA)[1], 8)


class TestComparisonClaims(unittest.TestCase):
    SIZES = (10, 100, 1000)

    def test_selection_same_on_every_input(self):
        for n in self.SIZES:
            for kind in INPUT_TYPES:
                with self.subTest(n=n, kind=kind):
                    self.assertEqual(selection_sort(make_input(kind, n, seed=1))[1], pairs(n))

    def test_insertion_sorted_and_reverse(self):
        for n in self.SIZES:
            self.assertEqual(insertion_sort(make_input("sorted", n))[1], n - 1)
            self.assertEqual(insertion_sort(make_input("reverse", n))[1], pairs(n))

    def test_bubble_sorted_and_reverse(self):
        for n in self.SIZES:
            self.assertEqual(bubble_sort(make_input("sorted", n))[1], n - 1)
            self.assertEqual(bubble_sort(make_input("reverse", n))[1], pairs(n))

    def test_merge_sort_within_n_log_n_bounds(self):
        for n in self.SIZES:
            lower = n * math.log2(n) / 2
            # exact worst case is n*ceil(log2 n) - 2^ceil(log2 n) + 1
            k = math.ceil(math.log2(n))
            upper = n * k - 2 ** k + 1
            for kind in INPUT_TYPES:
                with self.subTest(n=n, kind=kind):
                    count = merge_sort(make_input(kind, n, seed=2))[1]
                    # best case is only 'about' (n log2 n)/2, off by a few percent when n is not a power of 2
                    self.assertGreaterEqual(count, 0.9 * lower)
                    self.assertLessEqual(count, upper)

    def test_merge_sort_power_of_two_best_formula(self):
        for k in range(1, 11):
            n = 2 ** k
            self.assertEqual(merge_sort(list(range(n)))[1], (n * k) // 2)

    def test_merge_sort_power_of_two_worst_formula(self):
        # worst case for n = 2^k is exactly n log2 n - n + 1. Build it with the
        # interleaving trick: run merge sort backwards to find a worst input.
        for k in range(1, 9):
            n = 2 ** k
            worst = _merge_sort_worst_input(list(range(n)))
            count = merge_sort(worst)[1]
            self.assertEqual(count, n * k - n + 1)

    def test_quick_sort_random_near_n_log_n(self):
        for n in (100, 1000):
            counts = [quick_sort(make_input("random", n, seed=s))[1] for s in range(30)]
            mean = sum(counts) / len(counts)
            self.assertLess(mean, 2.0 * n * math.log2(n))
            self.assertGreater(mean, 0.8 * n * math.log2(n) * 0.5)

    def test_quick_sort_sorted_is_worst_case(self):
        for n in self.SIZES:
            self.assertEqual(quick_sort(make_input("sorted", n))[1], pairs(n))

    def test_linear_search_bounds(self):
        data = list(range(1, 101))
        self.assertEqual(linear_search(data, 1)[1], 1)
        self.assertEqual(linear_search(data, 100)[1], 100)
        self.assertEqual(linear_search(data, 0)[1], 100)

    def test_counts_never_exceed_n_choose_2_for_quadratic_sorts(self):
        for n in self.SIZES:
            for kind in INPUT_TYPES:
                data = make_input(kind, n, seed=3)
                for func in (selection_sort, insertion_sort, bubble_sort, quick_sort):
                    self.assertLessEqual(func(data)[1], pairs(n))

    def test_theory_table_matches_formulas(self):
        best, avg, worst = expected("Insertion Sort", 100)
        self.assertEqual((best, avg, worst), (99.0, 2500.0, 4950.0))
        best, avg, worst = expected("Selection Sort", 10)
        self.assertEqual((best, avg, worst), (45.0, 45.0, 45.0))


def _merge_sort_worst_input(items):
    """Return an arrangement of items that forces the most merge comparisons.

    Standard trick: split the sorted list into alternating elements, recurse on
    each half, then join them so every merge ends up interleaving fully.
    """
    if len(items) <= 1:
        return items
    left = _merge_sort_worst_input(items[0::2])
    right = _merge_sort_worst_input(items[1::2])
    return left + right


class TestInputHandling(unittest.TestCase):
    def test_valid_lists(self):
        self.assertEqual(parse_list("5, 3,9 , 1"), [5, 3, 9, 1])
        self.assertEqual(parse_list("-2, 4.5, 0"), [-2, 4.5, 0])
        self.assertEqual(parse_list("7"), [7])

    def test_bad_lists(self):
        for bad in ["", "   ", "1,,2", "1,2,", ",1", "a,b", "1, two, 3", "nan", "inf", "1;2"]:
            with self.subTest(bad=bad):
                with self.assertRaises(InputError):
                    parse_list(bad)

    def test_too_many_numbers(self):
        with self.assertRaises(InputError):
            parse_list(",".join(["1"] * (MAX_SIZE + 1)))

    def test_generator_shortcut(self):
        self.assertEqual(parse_generator("gen sorted 5"), [1, 2, 3, 4, 5])
        self.assertEqual(parse_generator("gen reverse 4"), [4, 3, 2, 1])
        self.assertEqual(len(parse_generator("gen random 50")), 50)

    def test_bad_generator(self):
        for bad in ["gen", "gen sorted", "gen weird 10", "gen sorted ten", "gen sorted 0",
                    "gen sorted -5", "gen sorted " + str(MAX_SIZE + 1)]:
            with self.subTest(bad=bad):
                with self.assertRaises(InputError):
                    parse_generator(bad)

    def test_parse_number(self):
        self.assertEqual(parse_number(" 12 "), 12)
        self.assertEqual(parse_number("3.5"), 3.5)
        with self.assertRaises(InputError):
            parse_number("abc")


if __name__ == "__main__":
    unittest.main()
