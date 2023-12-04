from pathlib import Path
from dataclasses import dataclass


@dataclass
class NumberSegment:
    x_start: int
    y_start: int
    x_span: int
    value: int


def is_symbol(x, y, lines):
    if x < 0 or y < 0 or y >= len(lines) or x >= len(lines[y]):
        return False
    return lines[y][x] != "." and not lines[y][x].isnumeric()


def is_valid(segment, lines):
    for y in range(segment.y_start - 1, segment.y_start + 2):
        for x in range(segment.x_start - 1, segment.x_start + segment.x_span + 1):
            if is_symbol(x, y, lines):
                return True
    return False


def solve(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() + "." for line in lines]

    numbers = []
    for y in range(len(lines)):
        n_start = -1
        n_end = -1
        for x in range(len(lines[y])):
            # first part
            if lines[y][x].isnumeric() and n_start == -1:
                n_start = x
            # first non-part
            # (note that extra "." is added, so single digit at end of line is fine)
            if (
                not lines[y][x].isnumeric() or ((x + 1) >= len(lines[y]))
            ) and n_start != -1:
                n_end = x
                numbers.append(
                    NumberSegment(
                        n_start, y, n_end - n_start, int(lines[y][n_start:n_end])
                    )
                )
                n_start = -1
                n_end = -1
    numbers = [n for n in numbers if is_valid(n, lines)]
    print(sum([n.value for n in numbers]))


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
