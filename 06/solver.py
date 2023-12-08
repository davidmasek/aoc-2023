import numpy as np
from pathlib import Path


def solve_race(race_time, race_record):
    race_total = 0
    for speed in range(1, race_time):
        remaining_time = race_time - speed
        traveled = speed * remaining_time
        if traveled > race_record:
            race_total += 1
    return race_total


def solve(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() for line in lines]

    time = [int(x) for x in lines[0].split(":")[1].split(" ") if x]
    distance = [int(x) for x in lines[1].split(":")[1].split(" ") if x]
    if file == "example.txt":
        assert time == [7, 15, 30]
        assert distance == [9, 40, 200]
        print("input checked")

    races = []
    for r in range(len(time)):
        races.append(solve_race(time[r], distance[r]))

    print("A:", np.prod(races))
    print("B (hardcoded input):", solve_race(40829166, 277133813491063))


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
