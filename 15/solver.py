from pathlib import Path
from dataclasses import dataclass


@dataclass
class Lens:
    label: str
    focal: int


def hash(exp: str) -> int:
    total = 0
    exp = [ord(e) for e in exp]
    for e in exp:
        total = ((total + e) * 17) % 256
    return total


def solve(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    # skip empty
    lines = [line.strip() for line in lines if line]
    assert len(lines) == 1, "expecting only one line"
    line = lines[0]

    hashes = [hash(exp) for exp in line.split(",")]
    print(hashes)
    print("A:", sum(hashes))

    boxes = [[] for _ in range(256)]
    steps = [exp for exp in line.split(",")]
    for step in steps:
        if step.endswith("-"):
            label = step[:-1]
            target = hash(label)
            for i in range(len(boxes[target])):
                if boxes[target][i].label == label:
                    boxes[target].pop(i)
                    break
        elif step[-2] == "=":
            label = step[:-2]
            target = hash(label)
            focal = int(step[-1])
            found = False
            for i in range(len(boxes[target])):
                if boxes[target][i].label == label:
                    boxes[target][i].focal = focal
                    found = True
                    break
            if not found:
                boxes[target].append(Lens(label, focal))
        else:
            raise ValueError("invalid step", step)

    total = 0
    for box in range(len(boxes)):
        for slot in range(len(boxes[box])):
            total += (1 + box) * (1 + slot) * boxes[box][slot].focal
    print("B:", total)


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
