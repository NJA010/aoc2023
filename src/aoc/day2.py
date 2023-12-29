from functools import reduce


class GameChecker:
    def __init__(self, file_path: str, cubes: dict):
        self.cubes = cubes
        with open(file_path, "r") as file:
            self.input = file.read()

    def check_game(self) -> (dict, int):
        result = {}
        power = 0
        for line in self.input.splitlines():
            # parse string to dictionary
            game_id, game_dict = self._parse_line(line)
            # check whether the game is valid
            result[game_id] = self._is_valid(game_dict)
            power += self._get_power_set(game_dict)
        return result, power

    def _is_valid(self, single_game: dict) -> bool:
        set_valid = []
        # loop over sets in a game
        for set_id, cubes in single_game.items():
            # for each set, loop over number, color combinations. Must be smaller or equal than the self.cubes
            set_valid.append(
                all([self.cubes[color] >= number for color, number in cubes.items()])
            )
        return all(set_valid)

    def _get_power_set(self, single_game: dict):
        max_cubes = {"red": 0, "green": 0, "blue": 0}
        # loop over sets in a game
        for set_id, cubes in single_game.items():
            for color, number in cubes.items():
                if number > max_cubes[color]:
                    max_cubes[color] = number
        return reduce(lambda x, y: x * y, max_cubes.values(), 1)

    def _parse_line(self, input_string: str) -> (str, dict):
        game, sets = input_string.split(": ")
        game_dict = {}
        sets = sets.split("; ")
        for i, s in enumerate(sets):
            game_dict[i] = {}
            for c in s.split(", "):
                number, color = c.split(" ")
                game_dict[i][color] = int(number)
        return game.split(" ")[-1], game_dict


if __name__ == "__main__":
    path = "./data/day2/input.txt"
    cubes = {"red": 12, "green": 13, "blue": 14}
    g = GameChecker(path, cubes)
    valid_games, power = g.check_game()
    print(sum([int(game) * valid for game, valid in valid_games.items()]))
    print(power)
