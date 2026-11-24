"""Test input generators: the five input types from the proposal."""
import random

INPUT_TYPES = ["random", "sorted", "reverse", "nearly", "duplicates"]


def make_input(kind, n, seed=None):
    """Build a list of n integers of the requested kind.

    random      shuffled distinct values
    sorted      1..n in order
    reverse     n..1
    nearly      sorted, then about 5 percent of positions get swapped
    duplicates  values drawn from a tiny range so lots of repeats
    """
    rng = random.Random(seed)
    if kind == "random":
        items = list(range(1, n + 1))
        rng.shuffle(items)
        return items
    if kind == "sorted":
        return list(range(1, n + 1))
    if kind == "reverse":
        return list(range(n, 0, -1))
    if kind == "nearly":
        items = list(range(1, n + 1))
        swaps = max(1, n // 20) if n > 1 else 0
        for _ in range(swaps):
            i = rng.randrange(n)
            j = rng.randrange(n)
            items[i], items[j] = items[j], items[i]
        return items
    if kind == "duplicates":
        spread = max(2, n // 10)
        return [rng.randint(1, spread) for _ in range(n)]
    raise ValueError("unknown input type: " + kind)
