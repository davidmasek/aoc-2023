from pathlib import Path
from dataclasses import dataclass
import numpy as np


@dataclass
class NumberSegment:
    x_start: int
    y_start: int
    x_span: int
    value: int


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

    counts = np.zeros([len(lines) + 2, len(lines[0]) + 2], dtype=np.int32)
    for segment in numbers:
        counts[
            max(0, segment.y_start - 1) : segment.y_start + 2,
            max(0, segment.x_start - 1) : segment.x_start + segment.x_span + 1,
        ] += 1
    total = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "*" and counts[y, x] == 2:
                print(f"Gear at {x=}, {y=}")
                values = []
                for segment in numbers:
                    if (
                        segment.y_start - 1 <= y <= segment.y_start + 1
                        and segment.x_start - 1 <= x <= segment.x_start + segment.x_span
                    ):
                        values.append(segment.value)
                        print(f"  {segment.value=}")
                assert len(values) == 2
                total += np.prod(values)
    print(total)


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
