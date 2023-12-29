class Scratcher:
    def __init__(self, file_path: str):
        with open(file_path, "r") as file:
            self.input = file.read()

    def get_total_score(self, input_split=None):
        scores = []
        if input_split is None:
            input_split = self.input.splitlines()
        for card in input_split:
            card_id, numbers = card.split(": ")
            scores.append(self.get_single_score(numbers))
        return scores

    def get_single_score(self, numbers):
        winning, owned = numbers.split("| ")
        winning = self._parse_numbers(winning)
        owned = self._parse_numbers(owned)
        n_matches = sum([True for n in owned if n in winning])
        if n_matches:
            return 2 ** (n_matches - 1)
        else:
            return 0

    def get_total_score_copies(self):
        cards_in_play = self.input.splitlines()
        score = len(cards_in_play)
        while cards_in_play:
            cards_in_play, n_copies = self.get_copies_to_play(cards_in_play)
            score += n_copies
        return score

    def get_copies_to_play(self, input_split=None):
        copies_id = []
        cards_to_play = []
        if input_split is None:
            input_split = self.input.splitlines()
        # obtain copies
        for card in input_split:
            card_id, numbers = card.split(": ")
            copies_id += self.get_copies(numbers, int(card_id.split(" ")[-1]))
        # obtain copy cards
        for c in copies_id:
            cards_to_play.append(self.input.splitlines()[c-1])
        return cards_to_play, len(cards_to_play)

    def get_copies(self, numbers, card_id):
        winning, owned = numbers.split("| ")
        winning = self._parse_numbers(winning)
        owned = self._parse_numbers(owned)
        n_matches = sum([True for n in owned if n in winning])
        return list(range(card_id + 1, card_id + n_matches + 1))

    def _parse_numbers(self, numbers_string):
        numbers = numbers_string.split(" ")
        numbers = [int(n) for n in numbers if n != ""]
        return numbers


if __name__ == "__main__":
    path = "./data/day4/input.txt"
    srt = Scratcher(path)
    scores = srt.get_total_score()
    scores_copies = srt.get_total_score_copies()
    print(sum(scores))
    print(scores_copies)
