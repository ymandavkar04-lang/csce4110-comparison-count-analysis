"""Module 2: input handling.

Turns what the user types into a list of numbers and rejects anything bad.
Two ways to enter data:
  1. a typed or pasted list such as  5, 3, 9, 1
  2. a generator shortcut such as    gen random 100   (kinds: see generators.py)
"""
from generators import INPUT_TYPES, make_input

MAX_SIZE = 5000  # the slow sorts do about n^2/2 steps, so keep it reasonable


class InputError(Exception):
    """Raised with a message that is safe to show to the user."""


def parse_number(text):
    """Convert one piece of text to an int, or a float if it has a decimal."""
    text = text.strip()
    try:
        return int(text)
    except ValueError:
        pass
    try:
        value = float(text)
    except ValueError:
        raise InputError("'" + text + "' is not a number.")
    if value != value or value in (float("inf"), float("-inf")):
        raise InputError("'" + text + "' is not a usable number.")
    return value


def parse_list(line):
    """Parse a line of comma-separated numbers (spaces around commas are fine)."""
    line = line.strip()
    if line == "":
        raise InputError("The list is empty. Enter at least one number.")
    pieces = line.split(",")
    values = []
    for piece in pieces:
        if piece.strip() == "":
            raise InputError("Found an empty spot between commas. Check for a stray comma.")
        values.append(parse_number(piece))
    if len(values) > MAX_SIZE:
        raise InputError("That list has " + str(len(values)) + " numbers. The limit is "
                         + str(MAX_SIZE) + ".")
    return values


def parse_generator(line):
    """Parse 'gen <kind> <size>' and return the generated list."""
    parts = line.split()
    if len(parts) != 3:
        raise InputError("Use the form: gen <kind> <size>   for example: gen random 100")
    kind = parts[1].lower()
    if kind not in INPUT_TYPES:
        raise InputError("Unknown kind '" + parts[1] + "'. Choose from: " + ", ".join(INPUT_TYPES) + ".")
    try:
        size = int(parts[2])
    except ValueError:
        raise InputError("Size must be a whole number, got '" + parts[2] + "'.")
    if size < 1:
        raise InputError("Size must be at least 1.")
    if size > MAX_SIZE:
        raise InputError("Size " + str(size) + " is too big. The limit is " + str(MAX_SIZE) + ".")
    return make_input(kind, size, seed=size)


def parse_entry(line):
    """Dispatch: generator shortcut or a plain list."""
    if line.strip().lower().startswith("gen"):
        return parse_generator(line)
    return parse_list(line)


def ask_for_list(prompt_fn=input):
    """Keep asking until the user gives a valid list."""
    while True:
        line = prompt_fn("Enter numbers separated by commas (or 'gen random 100'): ")
        try:
            return parse_entry(line)
        except InputError as err:
            print("  Invalid input: " + str(err))


def ask_for_target(prompt_fn=input):
    """Keep asking until the user gives a valid search target."""
    while True:
        line = prompt_fn("Enter the number to search for: ")
        try:
            return parse_number(line)
        except InputError as err:
            print("  Invalid input: " + str(err))
