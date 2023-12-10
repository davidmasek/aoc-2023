from pathlib import Path


def get_neighbors(y, x, lines):
    nbs = []
    north = y - 1
    south = y + 1
    west = x - 1
    east = x + 1

    if lines[north][x] == "|":
        nbs.append((north, x))
    elif lines[north][x] == "7":
        nbs.append((north, x))
    elif lines[north][x] == "F":
        nbs.append((north, x))
    if lines[south][x] == "|":
        nbs.append((south, x))
    elif lines[south][x] == "L":
        nbs.append((south, x))
    elif lines[south][x] == "J":
        nbs.append((south, x))
    if lines[y][east] == "-":
        nbs.append((y, east))
    elif lines[y][east] == "J":
        nbs.append((y, east))
    elif lines[y][east] == "7":
        nbs.append((y, east))
    if lines[y][west] == "-":
        nbs.append((y, west))
    elif lines[y][west] == "F":
        nbs.append((y, west))
    elif lines[y][west] == "L":
        nbs.append((y, west))

    # filter out-of-bounds
    nbs = [
        nb
        for nb in nbs
        if (nb[0] >= 0 and nb[1] >= 0 and nb[0] < len(lines) and nb[1] < len(lines[0]))
    ]

    can_visit = []
    current = lines[y][x]
    if current == "-":
        can_visit.append((y, east))
        can_visit.append((y, west))
    elif current == "|":
        can_visit.append((north, x))
        can_visit.append((south, x))
    elif current == "L":
        can_visit.append((north, x))
        can_visit.append((y, east))
    elif current == "J":
        can_visit.append((north, x))
        can_visit.append((y, west))
    elif current == "7":
        can_visit.append((south, x))
        can_visit.append((y, west))
    elif current == "F":
        can_visit.append((south, x))
        can_visit.append((y, east))
    elif current == "S":
        can_visit.append((north, x))
        can_visit.append((south, x))
        can_visit.append((y, east))
        can_visit.append((y, west))

    nbs = set(can_visit).intersection(set(nbs))

    return list(nbs)


def solve_first(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() for line in lines]

    lines.insert(0, "." * len(lines[0]))
    lines.append("." * len(lines[0]))
    _lines = []
    for line in lines:
        line = "." + line + "."
        _lines.append(line)
    lines = _lines

    s_y, s_x = None, None
    for y, line in enumerate(lines):
        x = line.find("S")
        if x >= 0:
            s_y = y
            s_x = x
            break

    assert s_x is not None and s_y is not None, "start not found"

    q = [(s_y, s_x)]
    seen = {}
    seen[(s_y, s_x)] = True
    path = []

    while len(q) > 0:
        node = q.pop()
        path.append(node)
        nbs = get_neighbors(node[0], node[1], lines)
        for nb in nbs:
            if nb not in seen:
                seen[(nb[0], nb[1])] = True
                q.append(nb)

    print("A:", len(path) // 2)
    return lines, path


def is_inside(y: int, x: int, lines: list[str], path: dict) -> bool:
    crosses = 0
    # going horizontally bypasses the "squeezing" option
    while y < len(lines) and x < len(lines[0]):
        is_cross = ((y, x) in path) and (lines[y][x] not in "L7")
        if is_cross:
            crosses += 1
        y += 1
        x += 1
    return crosses % 2 == 1


def solve_second(file: Path):
    lines, path = solve_first(file)
    path = {k: True for k in path}
    total = 0
    map_ = []
    for y in range(len(lines)):
        map_line = []
        for x in range(len(lines[0])):
            if (y, x) in path:
                map_line.append(lines[y][x])
            elif is_inside(y, x, lines, path):
                total += 1
                map_line.append("I")
            else:
                map_line.append(".")
        map_.append("".join(map_line))
    # print("\n".join(map_))
    print("B:", total)


def solve(file: Path):
    solve_first(file)
    solve_second(file)


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
