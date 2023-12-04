from pathlib import Path


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


def calculate_limits(game: dict, limits: dict) -> dict:
    for color, value in game.items():
        limits[color] = max(limits.get(color, 0), value)
    return limits


def solve(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    total = 0
    for line in lines:
        game_id, games = parse_game(line)
        limits = {}
        for game in games:
            limits = calculate_limits(game, limits)

        game_power = limits["red"] * limits["green"] * limits["blue"]
        total += game_power

    print(total)


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
