from pathlib import Path
from typing import Literal

limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_game(line: str) -> tuple:
    i = line.find(":")
    left, right = line[:i], line[i + 1 :]
    game_id = int(left.split()[-1])
    games_raw = right.split(";")
    games = []
    for game_raw in games_raw:
        game = {}
        for part in game_raw.split(","):
            value, color = part.strip().split(" ")
            game[color.strip()] = int(value.strip())
        games.append(game)
    return game_id, games


def validate_game(game: dict, limits: dict) -> bool:
    for color, value in game.items():
        if value > limits[color]:
            return False
    return True


def solve(file: Path, task_part: Literal[1, 2]):
    with open(file) as fh:
        lines = fh.readlines()
    total = 0
    for line in lines:
        game_id, games = parse_game(line)
        is_valid = True
        for game in games:
            is_valid = is_valid and validate_game(game, limits)
            if not is_valid:
                print(f"Game {game_id} is NOT valid")
                break
        if is_valid:
            print(f"Game {game_id} is valid")
            total += game_id

    print(total)


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
