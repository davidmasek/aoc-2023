from pathlib import Path


def transpose(stuff: list[str]):
    outstuff = [["" for _ in range(len(stuff))] for _ in range(len(stuff[0]))]
    for i in range(len(stuff)):
        for j in range(len(stuff[i])):
            outstuff[j][i] = stuff[i][j]
    return ["".join(x) for x in outstuff]


def _solve(pattern):
    print("--------------")
    print(pattern)

    for r in range(1, len(pattern)):
        # print("checking", r)
        pattern_a = pattern[:r]
        pattern_b = pattern[r:]
        n_must_match = min(len(pattern_a), len(pattern_b))
        pattern_a = pattern_a[-n_must_match:]
        pattern_b = pattern_b[:n_must_match][::-1]
        # print(pattern_a, pattern_b)
        if pattern_a == pattern_b:
            print("matched after row", r)
            return r * 100

    pattern = transpose(pattern)
    for r in range(1, len(pattern)):
        # print("checking", r)
        pattern_a = pattern[:r]
        pattern_b = pattern[r:]
        n_must_match = min(len(pattern_a), len(pattern_b))
        pattern_a = pattern_a[-n_must_match:]
        pattern_b = pattern_b[:n_must_match][::-1]
        # print(pattern_a, pattern_b)
        if pattern_a == pattern_b:
            print("matched after col", r)
            return r


def solve(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() for line in lines]

    pattern = []
    total = 0
    for line in lines:
        if line:
            pattern.append(line)
        else:
            total += _solve(pattern)
            pattern = []
    if len(pattern) > 0:
        total += _solve(pattern)
    print("A:", total)

    # TODO B: instead of ==, we need to count number of "errors"
    # (you can break on errors > 1)
    # and find row/col with errors == 1


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
