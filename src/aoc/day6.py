import math
from functools import reduce


def calc_distance(total_time: int, hold_time: int) -> int:
    if 0 <= hold_time <= total_time:
        return total_time * hold_time - hold_time**2
    else:
        return 0


def calc_solution_range(total_time: int, min_dist: int) -> (int, int):
    min_hold = math.ceil(0.5 * (total_time - math.sqrt(total_time**2 - 4 * min_dist)))
    max_hold = math.floor(
        0.5 * (math.sqrt(total_time**2 - 4 * min_dist) + total_time)
    )
    # can't hold longer than the race
    max_hold = min(total_time, max_hold)
    # need to atleast beat the record
    if calc_distance(total_time, min_hold) == min_dist:
        min_hold += 1
    if calc_distance(total_time, max_hold) == min_dist:
        max_hold -= 1
    return min_hold, max_hold


class BoatRacer:
    def __init__(self, file_path: str):
        with open(file_path, "r") as file:
            raw_input = file.read()
        time, distance = raw_input.split("\n")
        time = [int(t) for t in time.split(" ") if t not in ["", "Time:", "Distance:"]]
        distance = [
            int(t) for t in distance.split(" ") if t not in ["", "Time:", "Distance:"]
        ]
        self.race = list(zip(time, distance))

    def get_race_times(self):
        result = 1
        for r in self.race:
            print(f"starting race: {r}")
            min_hold, max_hold = calc_solution_range(r[0], r[1])
            print(
                f"Winning hold time: [{min_hold}, {max_hold}], that's {(max_hold-min_hold+1)} solutions"
            )
            result *= max_hold - min_hold + 1
        return result


class BoatRacerTwo:
    def __init__(self, file_path: str):
        with open(file_path, "r") as file:
            raw_input = file.read()
        time, distance = raw_input.split("\n")
        time = reduce(
            lambda x, y: x + y,
            [t for t in time.split(" ") if t not in ["", "Time:", "Distance:"]],
            "",
        )
        distance = reduce(
            lambda x, y: x + y,
            [d for d in distance.split(" ") if d not in ["", "Time:", "Distance:"]],
            "",
        )
        self.race = [(int(time), int(distance))]

    def get_race_times(self):
        result = 1
        for r in self.race:
            print(f"starting race: {r}")
            min_hold, max_hold = calc_solution_range(r[0], r[1])
            print(
                f"Winning hold time: [{min_hold}, {max_hold}], that's {(max_hold-min_hold+1)} solutions"
            )
            result *= max_hold - min_hold + 1
        return result


if __name__ == "__main__":
    path = "./data/day6/input.txt"
    b = BoatRacerTwo(path)
    print(b.get_race_times())
