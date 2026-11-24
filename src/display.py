"""Module 5: results display. Plain text tables, no outside libraries."""
from theory import expected, formula_text


def fmt(x):
    """Format a number: whole numbers with commas, others with one decimal."""
    if abs(x - round(x)) < 1e-9:
        return format(int(round(x)), ",")
    return format(x, ",.1f")


def table(headers, rows):
    """Return a string with a simple aligned table."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    out = [line]
    out.append("| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |")
    out.append(line)
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            text = str(cell)
            cells.append(text.rjust(widths[i]) if i > 0 else text.ljust(widths[i]))
        out.append("| " + " | ".join(cells) + " |")
    out.append(line)
    return "\n".join(out)


def show_list(items, limit=20):
    """Show a list in full when it is small, otherwise just the ends."""
    if len(items) <= limit:
        return str(items)
    return str(items[:5])[:-1] + ", ... " + str(items[-5:])[1:] + "  (" + str(len(items)) + " items)"


def show_single(name, n, measured, extra_lines):
    """Print one algorithm's result with its expected counts underneath."""
    best, avg, worst = expected(name, n)
    f_best, f_avg, f_worst = formula_text(name)
    print()
    for line in extra_lines:
        print(line)
    print("Comparisons made: " + fmt(measured))
    print("Expected for n = " + str(n) + ":")
    print("  best    " + f_best.ljust(18) + "= " + fmt(best))
    print("  average " + f_avg.ljust(18) + "= " + fmt(avg))
    print("  worst   " + f_worst.ljust(18) + "= " + fmt(worst))


def show_all(n, results):
    """Print the option 7 table. results is a list of (name, measured, ok_text)."""
    rows = []
    for name, measured, note in results:
        best, avg, worst = expected(name, n)
        rows.append([name, fmt(measured), fmt(best), fmt(avg), fmt(worst), note])
    print()
    print(table(["Algorithm", "Measured", "Best", "Average", "Worst", "Result"], rows))
