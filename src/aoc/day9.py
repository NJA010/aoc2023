import logging
from functools import reduce
import structlog

structlog.configure(logger_factory=structlog.stdlib.LoggerFactory())


# class StructlogAdapter(logging.LoggerAdapter):
#     def process(self, msg: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
#         return f"[{self.extra['module']}] {msg}", kwargs


# Using structlog's wrapper for the stdlib logger
logger = structlog.get_logger()
logging.basicConfig(level=logging.DEBUG)


def get_diff(sequence: list[int]):
    # no numpy?
    return [s1 - s2 for s1, s2 in zip(sequence[1:], sequence[:-1])]


class EnvHist:
    def __init__(self, file_path: str):
        with open(file_path, "r") as file:
            raw_input = file.read()

        self.sequences = [
            [int(number) for number in seq.split(" ")] for seq in raw_input.splitlines()
        ]

    def get_history_forward(self):
        extrapolate = []
        for current_sequence in self.sequences:
            logger.info(f"Current sequence: {current_sequence}")
            # fill diffs with last value from sequence for cum sum
            diffs = [current_sequence[-1]]
            current_diff = current_sequence
            while not all([d == 0 for d in current_diff]):
                current_diff = get_diff(current_diff)
                logger.debug(f"diff {current_diff}")
                diffs.append(current_diff[-1])
            logger.info(f"All last diffs: {diffs}")
            # sum of last values in difference sequence is the total
            extrapolate.append(sum(diffs))
            logger.info(f"Next value: {extrapolate[-1]}")
        return extrapolate

    def get_history_backward(self):
        extrapolate = []
        for current_sequence in self.sequences:
            logger.info(f"Current sequence: {current_sequence}")
            # fill diffs with last value from sequence for cum sum
            diffs = [current_sequence[0]]
            current_diff = current_sequence
            i = 1
            while not all([d == 0 for d in current_diff]):
                current_diff = get_diff(current_diff)
                logger.debug(f"diff {current_diff}")
                # if uneven diff sequence, subtract otherwise add
                if (i % 2 == 0):
                    diffs.append(current_diff[0])
                else:
                    diffs.append(-current_diff[0])
                i+=1

            logger.info(f"All first diffs: {diffs}")
            # sum of last values in difference sequence is the total
            extrapolate.append(sum(diffs))
            logger.info(f"Previous value: {extrapolate[-1]}")
        return extrapolate


if __name__ == "__main__":
    path = "./data/day9/input.txt"
    b = EnvHist(path)
    # 1921197374
    print(sum(b.get_history_backward()))
