class Calibration:
    def __init__(self, file_path: str):
        self.numbers = [str(i) for i in range(10)]
        with open(file_path, "r") as file:
            self.input = file.read()
        self.values = []

    def transcribe(self) -> list[int]:
        for line in self.input.splitlines():
            first = None
            last = None
            line_number = self._string_to_num(line)
            for c in line_number:
                if c in self.numbers and first is None:
                    first = c
                if c in self.numbers:
                    last = c
            self.values.append(int(first + last))
        return self.values

    def _string_to_num(self, input_string: str) -> str:
        """
        from line return (number, index)
        :param input_string:
        :return:
        """
        mapper = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
        for old_str, new_str in mapper.items():
            input_string = input_string.replace(
                old_str, old_str + str(new_str) + old_str
            )
        return input_string


# twone

# two2twone
# two2twone1one

# twone
# 2ne

if __name__ == "__main__":
    path = "./data/day1/input-1.txt"
    c = Calibration(path)
    v = c.transcribe()
    print(sum(v))
