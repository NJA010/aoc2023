import copy
from functools import reduce


class EngineChecker:
    def __init__(self, file_path: str, symbols: set):
        with open(file_path, "r") as file:
            self.input = file.read()
        s = set()
        for c in self.input:
            if (c != ".") and c not in [str(i) for i in range(10)] and (c != "\n"):
                s.add(c)
        print(s)
        self.col_len = self.input.index("\n") + 1
        self.row_len = self.input.count("\n")
        # self.input = self.input.replace("\n", "")
        self.symbols = symbols

    def get_parts(self):
        parts = []
        gears_all = {}
        start_search = 0
        adj_indices = self.get_adj_indices()
        adj_indices_values = reduce(lambda x, y: x + y, adj_indices.values(), [])
        # to select all numbers and prevent symbols from messing up, replace symbols with dot
        input_dotted = copy.deepcopy(self.input)
        for s in self.symbols:
            input_dotted = input_dotted.replace(s, ".")
        # for each number, check whether any of the number indices are inside the adj indices
        for not_dot in input_dotted.split("."):
            # skip chars that are not numbers
            if (not_dot == "") or (not_dot == "\n"):
                continue
            num_len = len(not_dot)
            first_index = input_dotted.index(not_dot, start_search)
            num_indices = [first_index + i for i in range(num_len)]
            # if any of the num indices is in the adj list all good
            is_valid_part = any([i in adj_indices_values for i in num_indices])
            # get symbol index
            symbol_indices = self.get_symbol_index(adj_indices, num_indices)
            for s_i in symbol_indices:
                if s_i not in gears_all.keys():
                    gears_all[s_i] = [int(not_dot)]
                else:
                    gears_all[s_i].append(int(not_dot))
            if is_valid_part:
                parts.append(int(not_dot))
            # finally make sure that the next search does not select the most resent search
            start_search = first_index + num_len

        return parts, gears_all

    def get_adj_indices(self):
        adj_indices = {}
        for i, c in enumerate(self.input):
            # check if char is a symbol, if so get correct part locations
            if c in self.symbols:
                adj_indices[i] = self.get_adj_index(i)
        return adj_indices

    def get_adj_index(self, char_index: int) -> list[int]:
        safe_indices = [
            # above
            char_index - self.col_len - 1,
            char_index - self.col_len,
            char_index - self.col_len + 1,
            # under
            char_index + self.col_len - 1,
            char_index + self.col_len,
            char_index + self.col_len + 1,
            # next to
            char_index - 1,
            char_index + 1,
        ]
        return safe_indices

    def get_symbol_index(self, adj_indices: dict, num_indices):
        symbol_hit = [
            symbol_i
            for symbol_i, indices in adj_indices.items()
            if any([n in indices for n in num_indices])
        ]
        # filter out non *
        filter_symbols = ["*"]

        return [s for s in symbol_hit if self.input[s] in filter_symbols]


if __name__ == "__main__":
    path = "./data/day3/input.txt"
    symbols = {"/", "=", "%", "+", "&", "$", "-", "*", "#", "@"}
    e = EngineChecker(path, symbols)
    parts, gears = e.get_parts()
    print(sum(parts))
    print(sum([reduce(lambda x, y: x*y, nums, 1) for nums in gears.values() if len(nums) == 2]))
