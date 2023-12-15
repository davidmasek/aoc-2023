from pathlib import Path
import itertools
import math
from dataclasses import dataclass

import numpy as np


@dataclass
class Point:
    y: int
    x: int


@dataclass
class Distance:
    a: Point
    b: Point
    non_empty: int
    empty: int


def _solve(lines: list[str]) -> list[Distance]:
    rows = [[1 if c == "#" else 0 for c in r] for r in lines]
    galaxy = np.array(rows)
    print("shape", galaxy.shape)
    r = galaxy.sum(axis=1)
    empty_rows = np.nonzero(r == 0)[0]
    c = galaxy.sum(axis=0)
    empty_cols = np.nonzero(c == 0)[0]

    galaxies_coordinates = np.nonzero(galaxy == 1)

    print("found", len(galaxies_coordinates[0]), "galaxies")
    print("   ->", math.comb(len(galaxies_coordinates[0]), 2), "pairs")

    distances = []
    for i, j in itertools.combinations(range(len(galaxies_coordinates[0])), 2):
        yi, xi = galaxies_coordinates[0][i], galaxies_coordinates[1][i]
        yj, xj = galaxies_coordinates[0][j], galaxies_coordinates[1][j]
        distance = abs(yi - yj) + abs(xi - xj)

        empty_count = 0
        for empty_row in empty_rows:
            if yi < empty_row < yj or yj < empty_row < yi:
                empty_count += 1

        for empty_col in empty_cols:
            if xi < empty_col < xj or xj < empty_col < xi:
                empty_count += 1

        distances.append(Distance(Point(yi, xi), Point(yj, xj), distance, empty_count))

    return distances


def solve(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() for line in lines]

    distances = _solve(lines)

    dist_A = [d.non_empty + d.empty for d in distances]
    print("A:", sum(dist_A))

    multiplier = 1000000 - 1
    dist_B = [d.non_empty + multiplier * d.empty for d in distances]
    print("B:", sum(dist_B))


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
