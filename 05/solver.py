from pathlib import Path


def _solve(seeds: list[int], maps: dict):
    outputs = []
    for seed in seeds:
        source_name = "seed"
        source = seed
        while source_name in maps:
            for interval in maps[source_name]["intervals"]:
                destination_start, source_start, length = interval
                if source_start <= source < source_start + length:
                    source = destination_start + (source - source_start)
                    break
            source_name = maps[source_name]["target"]
        outputs.append(source)
    return outputs


def _solve_inverse(seeds_intervals: list[(int, int)], inverse_maps: dict):
    target_name = "location"
    mapped_endpoints = [0, 10**15]
    while target_name in inverse_maps:
        source_name = inverse_maps[target_name]["source"]
        intervals = inverse_maps[target_name]["intervals"]
        endpoints = mapped_endpoints
        for interval in intervals:
            destination_start, source_start, length = interval
            endpoints.append(destination_start)
            # TODO -1 I think?
            endpoints.append(destination_start + length - 1)
        mapped_endpoints = []
        for endpoint in endpoints:
            source = endpoint
            for interval in intervals:
                destination_start, source_start, length = interval
                if destination_start <= endpoint < destination_start + length:
                    source = source_start + (endpoint - destination_start)
                    break
            mapped_endpoints.append(source)
        target_name = source_name

    usable_endpoints = []
    for endpoint in mapped_endpoints:
        for interval in seeds_intervals:
            start, end = interval
            if start <= endpoint <= end:
                usable_endpoints.append(endpoint)

    return usable_endpoints


def solve(file: Path):
    with open(file) as fh:
        lines = fh.readlines()
    lines = [line.strip() for line in lines]

    seeds = []
    x = ""
    y = ""
    maps = {}
    inverse_maps = {}
    for line in lines:
        # empty line
        if len(line) == 0:
            continue
        # initial line
        if line.startswith("seeds"):
            seeds = [int(x) for x in line.split(":")[1].split(" ") if x]
            continue
        # X-to-Y map:
        if line[0].isalpha():
            x, _, y = line.split()[0].split("-")
            continue
        # data line
        assert line[0].isdigit(), line
        assert x and y, line
        destination_start, source_start, length = [int(x) for x in line.split()]
        if x not in maps:
            maps[x] = {}
            maps[x]["intervals"] = []
            maps[x]["target"] = y
        if y not in inverse_maps:
            inverse_maps[y] = {}
            inverse_maps[y]["source"] = x
            inverse_maps[y]["intervals"] = []
        maps[x]["intervals"].append((destination_start, source_start, length))
        inverse_maps[y]["intervals"].append((destination_start, source_start, length))

    outputs = _solve(seeds, maps)
    print("A:", min(outputs))

    seeds_intervals = []
    for i in range(0, len(seeds), 2):
        seeds_intervals.append((seeds[i], seeds[i] + seeds[i + 1] - 1))

    seeds = _solve_inverse(seeds_intervals, inverse_maps)
    outputs = _solve(seeds, maps)
    print("B:", min(outputs))


if __name__ == "__main__":
    import fire

    fire.Fire(solve)
