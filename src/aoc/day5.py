from multiprocessing import Pool
import structlog
import logging
from tqdm import tqdm
from typing import Any, Dict, Tuple

import cProfile

# Configure structlog to use the stdlib logging module
structlog.configure(logger_factory=structlog.stdlib.LoggerFactory())


# class StructlogAdapter(logging.LoggerAdapter):
#     def process(self, msg: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
#         return f"[{self.extra['module']}] {msg}", kwargs


# Using structlog's wrapper for the stdlib logger
logger = structlog.get_logger()
logging.basicConfig(level=logging.DEBUG)


class SoilMapping:
    def __init__(self, map_raw: str):
        raw_input = map_raw.split("\n")
        self.name = raw_input[0]
        logger.info(f"Creating SoilMapping instance: {self.name}", module="SoilMapping")

        map_input = [
            [int(i) for i in single_map.split(" ")] for single_map in raw_input[1:]
        ]
        self.map_list = self._get_maps(map_input)

    @staticmethod
    def _get_maps(map_input):
        logger.info("Generating maps", module="SoilMapping")
        map_list = []
        for m in map_input:
            destination_start, source_start, length = m
            value_range = (source_start, source_start + length)

            transformer = destination_start - source_start

            map_list.append({"range": value_range, "transformer": transformer})
        return map_list

    def get(self, source: int):
        # prefill with default transformer (nothing)
        transformer = 0
        for m in self.map_list:
            if (source >= m["range"][0]) & (source < m["range"][1]):
                transformer = m["transformer"]
                break

        result = source + transformer
        logger.info(f"Mapping applied: {source} -> {result}", module="SoilMapping")
        return result

    def __str__(self):
        return self.name


class SoilPlanterManager:
    def __init__(self, file_path: str, seed_strategy=None):
        logger.info("Creating SoilPlanterManager instance", module="SoilPlanterManager")
        with open(file_path, "r") as file:
            raw_input = file.read()

        # each element of this list is a map, seed->soil, soil->fert, etc.
        with Pool() as pool:
            self.maps = pool.map(SoilMapping, raw_input.split("\n\n")[1:])
        # self.maps = [SoilMapping(i) for i in raw_input.split("\n\n")]

        # input seeds
        if seed_strategy is None:
            seed_strategy = self._get_seeds_single

        self.seeds = seed_strategy(raw_input)

    def feed_forward(self):
        """
        apply mapping elements in sequential order to all seeds
        :return:
        """
        destination = []
        for seed in self.seeds:
            source = seed
            logger.info(
                f"Applying mappings for seed: {source}", module="SoilPlanterManager"
            )
            for m in self.maps:
                source = m.get(source)
            logger.info(
                f"Final destination for seed {source}", module="SoilPlanterManager"
            )
            destination.append(source)
        return destination

    def get_final_route(self):
        last_range = [
            min(r[0] for r in self.split_range(input_range, depth=0))
            for input_range in self.seeds
        ]
        return last_range

    @staticmethod
    def _get_seeds_single(raw_input):
        logger.info("Extracting seeds", module="SoilPlanterManager")
        end_first_line = raw_input.index("\n")
        seeds = raw_input[:end_first_line]
        # del seed row and empty row
        # make sure ints
        seeds = [int(s) for s in seeds.split(" ")[1:]]
        return seeds

    def cut_up_range(self, input_range: tuple[int, int]) -> list[tuple[int, int]]:
        ranges = []
        this_cut = [m["range"][0] for m in self.maps[0].map_list]
        for m in self.maps[1:]:
            next_cuts = [m["range"][0] for m in m.map_list]
            ranges.append(self.split_range(input_range, this_cut, next_cuts))
            this_cut = next_cuts
        return ranges

    def split_range(
        self, input_range: tuple[int, int], depth: int
    ) -> list[tuple[int, int]]:
        ranges = []
        # transformations = 0
        current_min = input_range[0]
        current_max = input_range[1]
        this_range_cuts = sorted([m["range"][0] for m in self.maps[depth].map_list])
        for cut in this_range_cuts:
            if (cut >= current_min) & (cut < current_max) & (cut > 0):
                ranges.append(
                    (self.maps[depth].get(current_min), self.maps[depth].get(cut - 1))
                )
                current_min = cut
        ranges.append(
            (self.maps[depth].get(current_min), self.maps[depth].get(current_max))
        )

        # Recursively split each outer subrange based on next split values
        if (depth + 1) < len(self.maps):
            new_subranges = []
            for subrange in ranges:
                inner_subranges = self.split_range(subrange, depth + 1)
                new_subranges += inner_subranges
            return new_subranges
        return ranges


def _get_seeds_range(raw_input):
    logger.info("Extracting seeds", module="SoilPlanterManager")
    end_first_line = raw_input.index("\n")
    seed_ranges = raw_input[:end_first_line]
    # make sure ints
    seed_ranges = [int(s) for s in seed_ranges.split(" ")[1:]]
    starts = seed_ranges[0::2]
    lens = seed_ranges[1::2]

    seeds = [(st, st + le) for st, le in zip(starts, lens)]
    logger.info(seeds, module="SoilPlanterManager")

    return seeds


if __name__ == "__main__":
    path = "./data/day5/input.txt"
    profile = cProfile.Profile()
    profile.enable()
    manager = SoilPlanterManager(path, seed_strategy=_get_seeds_range)
    # result = manager.feed_forward()
    result = manager.get_final_route()
    profile.disable()
    logger.info(f"Results: {result}", module="main")
    logger.info(f"Results: {min(result)}", module="main")
    logger.info("Script completed", module="main")

    profile.print_stats(sort="cumulative")
