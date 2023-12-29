from functools import reduce


def obtain_score(hand: str) -> (float, float):
    """
    scores ordered highest to smallest: 6 -> 0
    :param hand:
    :return:
    """
    count = {}
    card_order = {
        "A": 13,
        "K": 12,
        "Q": 11,
        "J": 10,
        "T": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1,
    }
    # count occurences of each type and sum remainder
    remainder = []
    for cha in hand:
        if cha in count.keys():
            count[cha] += 1
        else:
            count[cha] = 1
        remainder.append(card_order[cha])

    # obtain remainder score in case of draws
    # five ok
    if len(count) == 1:
        return 6.0, remainder
    # four ok
    elif 4 in count.values():
        return 5.0, remainder
    # full house
    elif 3 in count.values() and 2 in count.values() and len(count) == 2:
        return 4.0, remainder
    # three ok
    elif 3 in count.values():
        return 3.0, remainder
    # two pair
    elif sum([2 == c for c in count.values()]) == 2:
        return 2.0, remainder
    # one pair
    elif 2 in count.values():
        return 1.0, remainder
    # highcard
    return 0.0, remainder


def obtain_score_joker(hand: str) -> (float, float):
    """
    scores ordered highest to smallest: 6 -> 0
    :param hand:
    :return:
    """
    count = {}
    card_order = {
        "A": 13,
        "K": 12,
        "Q": 11,
        "J": 1,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    # count occurences of each type and sum remainder
    remainder = []
    jokers = 0
    for cha in hand:
        if cha in count.keys():
            count[cha] += 1
        else:
            count[cha] = 1
        if cha == "J":
            jokers += 1
        remainder.append(card_order[cha])

    if jokers:
        # add jokers to highest count
        max_val = 0
        max_char = ""
        for key, value in count.items():
            if (value > max_val) & (key != "J"):
                max_val = value
                max_char = key
        if max_char:
            count[max_char] += jokers
            del count["J"]

    # obtain remainder score in case of draws
    # five ok
    if len(count) == 1:
        return 6.0, remainder
    # four ok
    elif 4 in count.values():
        return 5.0, remainder
    # full house
    elif 3 in count.values() and 2 in count.values() and len(count) == 2:
        return 4.0, remainder
    # three ok
    elif 3 in count.values():
        return 3.0, remainder
    # two pair
    elif sum([2 == c for c in count.values()]) == 2:
        return 2.0, remainder
    # one pair
    elif 2 in count.values():
        return 1.0, remainder
    # highcard
    return 0.0, remainder


class CamelGame:
    def __init__(self, file_path: str):
        with open(file_path, "r") as file:
            raw_input = file.read()

        self.card = [line.split(" ") for line in raw_input.splitlines()]

    def get_odds(self, score_func=None):
        if score_func is None:
            score_func = obtain_score

        score_list = []
        for c in self.card:
            hand, bid = c
            score, remainder = score_func(hand)
            score_list.append(
                {"hand": hand, "bid": int(bid), "score": score, "remainder": remainder}
            )
        score_list = sorted(
            score_list, key=lambda x: (x["score"], x["remainder"]), reverse=True
        )
        print(score_list)
        max_score = len(score_list)
        result = reduce(
            lambda x, y: x + y,
            [s["bid"] * (max_score - i) for i, s in enumerate(score_list)],
            0,
        )
        return result


if __name__ == "__main__":
    path = "./data/day7/input.txt"
    b = CamelGame(path)
    print(b.get_odds(obtain_score_joker))
