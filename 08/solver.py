import numpy as np
from pathlib import Path


def solve(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() for line in lines]
    # skip empty lines
    lines = [line for line in lines if line]

    moves_input = lines[0]
    graph_input = lines[1:]
    graph = {}
    for line in graph_input:
        src, left_right = line.split("=")
        src = src.strip()
        left, right = left_right.strip().strip("(").strip(")").split(",")
        left, right = left.strip(), right.strip()
        graph[src] = (left, right)

    moves = []
    for move in moves_input:
        assert move in "LR"
        if move == "L":
            moves.append(0)
        else:
            moves.append(1)

    nodes = [node for node in graph if node.endswith("A")]
    print("Solving for", len(nodes), "nodes")
    finds_z_in = []
    for node in nodes:
        i = 0
        total = 0
        while True:
            total += 1
            node = graph[node][moves[i]]
            i = (i + 1) % len(moves)
            if node.endswith("Z"):
                print("Found Z", total, "in steps")
                finds_z_in.append(total)
                break

    print("A:", finds_z_in[0])

    import math

    print("B:", math.lcm(*finds_z_in))


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
