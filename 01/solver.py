from pathlib import Path
from typing import Literal

replacements = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def solve(file: Path, task_part: Literal[1, 2]):
    with open(file) as fh:
        lines = fh.readlines()
    total = 0
    for line in lines:
        if task_part == 2:
            for source, target in replacements.items():
                # just replacing doesn't work since one letter can be used in multiple numbers
                # preppending and appending `source` keeps the letters available for later passes of the loop
                # and the `target` is included at the correct position
                # -> basically a "lazy" way to solve this
                line = line.replace(source, f"{source}{target}{source}")
        numbers = [c for c in line if c.isnumeric()]
        first, last = numbers[0], numbers[-1]
        total += int(first + last)

    print(total)


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
