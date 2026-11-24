"""Module 1: the six algorithms, each one counting its own comparisons.

Every sort takes a list, works on a copy so the caller's list is never
changed, and returns (sorted_list, comparison_count). Linear search returns
(index_or_-1, comparison_count).

What counts as a comparison: any time two data values are compared with
<, <=, >, >= or ==. Index checks like "j >= 0" are not counted because they
compare positions, not data.
"""


def linear_search(data, target):
    """Scan left to right. One comparison for every element looked at."""
    comparisons = 0
    for i in range(len(data)):
        comparisons += 1
        if data[i] == target:
            return i, comparisons
    return -1, comparisons


def merge_sort(data):
    """Top-down merge sort. Comparisons are counted inside the merge step."""
    counter = [0]
    result = _merge_sort(list(data), counter)
    return result, counter[0]


def _merge_sort(items, counter):
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = _merge_sort(items[:mid], counter)
    right = _merge_sort(items[mid:], counter)
    return _merge(left, right, counter)


def _merge(left, right, counter):
    merged = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        counter[0] += 1
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    # one side ran out, the rest of the other side needs no comparisons
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def selection_sort(data):
    """Find the smallest remaining item each pass and swap it into place."""
    a = list(data)
    n = len(a)
    comparisons = 0
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[smallest]:
                smallest = j
        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]
    return a, comparisons


def insertion_sort(data):
    """Grow a sorted prefix by sliding each new key left into position."""
    a = list(data)
    comparisons = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comparisons


def bubble_sort(data):
    """Bubble sort with an early exit when a full pass makes no swaps."""
    a = list(data)
    n = len(a)
    comparisons = 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a, comparisons


def quick_sort(data):
    """Quick sort with the first element as the pivot.

    I use an explicit stack instead of recursion. With a first-element pivot
    a sorted list of 1,000 items would recurse about 1,000 levels deep and hit
    Python's default recursion limit. The comparison counts are the same.
    """
    a = list(data)
    comparisons = 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        pivot = a[lo]
        store = lo
        for j in range(lo + 1, hi + 1):
            comparisons += 1
            if a[j] < pivot:
                store += 1
                a[store], a[j] = a[j], a[store]
        a[lo], a[store] = a[store], a[lo]
        stack.append((lo, store - 1))
        stack.append((store + 1, hi))
    return a, comparisons


SORTS = {
    "Merge Sort": merge_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Bubble Sort": bubble_sort,
    "Quick Sort": quick_sort,
}
