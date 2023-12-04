from pathlib import Path


def solve(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() for line in lines]

    common_counts = {}
    for line in lines:
        card_id = int(line.split(":")[0].split(" ")[-1])
        winning, owned = line.split(":")[1].split("|")
        winning = [int(x.strip()) for x in winning.split(" ") if x]
        owned = [int(x.strip()) for x in owned.split(" ") if x]
        common_count = len(set(winning) & set(owned))
        common_counts[card_id] = common_count

    total = 0
    for card_count in common_counts.values():
        if card_count == 0:
            value = 0
        else:
            value = 2 ** (card_count - 1)
        total += value
    print("A:", total)

    cards_owned = {}
    for card_i, card_count in common_counts.items():
        currently_owned = cards_owned.get(card_i, 1)
        cards_owned[card_i] = currently_owned
        for won_idx in range(card_i + 1, card_i + card_count + 1):
            # do not go past table
            if won_idx in common_counts:
                cards_owned[won_idx] = cards_owned.get(won_idx, 1) + currently_owned
    print("B:", sum(cards_owned.values()))


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
