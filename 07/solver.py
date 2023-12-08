import numpy as np
from pathlib import Path

ORDER = "AKQJT98765432J"
ORDER_JOKER = "AKQT98765432J"

SECOND_PART = False

POWER_TO_NAME = {
    10: "high card",
    20: "pair",
    30: "two pairs",
    40: "three of a kind",
    50: "full house",
    60: "four of a kind",
    70: "five of a kind",
}


class Hand:
    hand: str
    bid: int
    power: int

    def __init__(self, hand, bid, second_part: bool):
        self.hand = hand
        self.bid = bid
        if second_part:
            self.power = self._calculate_power_joker()
            self.order = ORDER_JOKER
        else:
            self.power = self._calculate_power()
            self.order = ORDER

    def _calculate_power_joker(self) -> int:
        non_joker = self.hand.replace("J", "")
        _, counts = np.unique(list(non_joker), return_counts=True)
        jokers = self.hand.count("J")

        if 5 - jokers in counts or jokers >= 4:
            return 70
        if 4 - jokers in counts or jokers >= 3:
            return 60

        assert jokers <= 2
        has_two_pairs = (counts == 2).sum() == 2
        if (
            (3 in counts and 2 in counts)
            or (3 in counts and jokers >= 1)
            or (has_two_pairs and jokers >= 1)
        ):
            return 50
        if 3 in counts or jokers >= 2 or (2 in counts and jokers >= 1):
            return 40
        if has_two_pairs or jokers >= 2:
            return 30
        if 2 in counts or jokers >= 1:
            return 20
        return 10

    def _calculate_power(self) -> int:
        _, counts = np.unique(list(self.hand), return_counts=True)
        if 5 in counts:
            return 70
        if 4 in counts:
            return 60
        if 3 in counts and 2 in counts:
            return 50
        if 3 in counts:
            return 40
        if (counts == 2).sum() == 2:
            return 30
        if 2 in counts:
            return 20
        return 10

    def __repr__(self):
        return f"Hand('{self.hand}', {self.bid})"

    def __lt__(self, other):
        if self.power < other.power:
            return True
        if self.power > other.power:
            return False
        for i in range(len(self.hand)):
            a = self.order.index(self.hand[i])
            b = self.order.index(other.hand[i])
            if a > b:
                return True
            if a < b:
                return False
        raise ValueError("Hands are equal")


def solve(file: Path, second_part: bool):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() for line in lines]

    hands = []
    for line in lines:
        hand, bid = line.split()
        hands.append(Hand(hand, int(bid), second_part))

    hands = sorted(hands)
    if file == "example.txt":
        print(hands)

    if file == "input.txt":
        import random

        for _ in range(10):
            l = random.choice(hands)
            r = random.choice(hands)
            print(
                f"{l} |",
                POWER_TO_NAME[l.power],
                f"| {r} |",
                POWER_TO_NAME[r.power],
                l > r,
            )

    total = 0
    for i, hand in enumerate(hands, 1):
        total += i * hand.bid

    if second_part:
        print("B:", total)
    else:
        print("A:", total)


if __name__ == "__main__":
    import fire

    def _input(file: Path):
        solve(file, False)
        solve(file, True)

    fire.Fire(_input)
