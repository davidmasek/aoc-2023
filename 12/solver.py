from pathlib import Path


def count_possible(
    line: str,
    groups: list[int],
    line_index: int = 0,
    group_index: int = 0,
    group_count: int = 0,
) -> int:
    if line_index >= len(line):
        if group_index >= len(groups):
            return 1
        if group_index == len(groups) - 1 and group_count == groups[-1]:
            return 1
        return 0

    c = line[line_index]
    if c == "#":
        if group_index >= len(groups):
            return 0
        group_count += 1
        target_count = groups[group_index]
        if group_count > target_count:
            return 0

        return count_possible(
            line,
            groups,
            line_index + 1,
            group_index,
            group_count,
        )
    elif c == ".":
        if group_count > 0:
            target_count = groups[group_index]
            if group_count != target_count:
                return 0
            group_index += 1
            group_count = 0
        assert group_count == 0

        return count_possible(line, groups, line_index + 1, group_index, group_count)
    elif c == "?":
        line_a = line[:line_index] + "#" + line[line_index + 1 :]
        line_b = line[:line_index] + "." + line[line_index + 1 :]
        return count_possible(
            line_a,
            groups,
            line_index,
            group_index,
            group_count,
        ) + count_possible(
            line_b,
            groups,
            line_index,
            group_index,
            group_count,
        )
    else:
        raise ValueError(c)


def unfold(line, groups):
    line += "?"
    line = line * 5
    line = line[:-1]
    groups = groups * 5
    return line, groups


def solve(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    # skip empty lines, remove newlines
    lines = [line.strip() for line in lines if line]

    total = 0
    for line in lines:
        record, groups = line.split()
        groups = [int(g) for g in groups.split(",")]
        r = count_possible(record, groups)
        total += r

    print("A:", total)

    print("B: not implemented")
    return

    total = 0
    for line in lines:
        record, groups = line.split()
        groups = [int(g) for g in groups.split(",")]
        record, groups = unfold(record, groups)
        r = count_possible(record, groups)
        total += r

    print("B:", total)

    line, groups


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
