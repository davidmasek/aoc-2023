import numpy as np
from pathlib import Path
import itertools


def solve_first(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() for line in lines]

    total = 0
    for line in lines:
        numbers = [int(x) for x in line.split() if x]
        all_differences = [
            numbers,
        ]
        differences = [
            second - first for (first, second) in itertools.pairwise(numbers)
        ]
        while not all([d == 0 for d in differences]):
            all_differences.append(differences)
            differences = [
                second - first for (first, second) in itertools.pairwise(differences)
            ]

        for i in reversed(range(len(all_differences) - 1)):
            all_differences[i].append(
                all_differences[i][-1] + all_differences[i + 1][-1]
            )

        res = all_differences[0][-1]
        total += res

    print("A:", total)


def solve_second(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() for line in lines]

    total = 0
    for line in lines:
        numbers = [int(x) for x in line.split() if x]
        all_differences = [
            numbers,
        ]
        differences = [
            second - first for (first, second) in itertools.pairwise(numbers)
        ]
        while not all([d == 0 for d in differences]):
            all_differences.append(differences)
            differences = [
                second - first for (first, second) in itertools.pairwise(differences)
            ]

        for i in reversed(range(len(all_differences) - 1)):
            all_differences[i].insert(
                0,
                all_differences[i][0] - all_differences[i + 1][0],
            )

        res = all_differences[0][0]
        total += res

    print("B:", total)


def solve(file: Path):
    solve_first(file)
    solve_second(file)


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
