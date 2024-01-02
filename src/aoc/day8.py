import logging
from multiprocessing import Pool
from functools import reduce
import structlog

structlog.configure(logger_factory=structlog.stdlib.LoggerFactory())


# class StructlogAdapter(logging.LoggerAdapter):
#     def process(self, msg: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
#         return f"[{self.extra['module']}] {msg}", kwargs


# Using structlog's wrapper for the stdlib logger
logger = structlog.get_logger()
logging.basicConfig(level=logging.DEBUG)


def get_gcd(a, b):
    while b != 0:
        remainder = a % b
        a = b
        b = remainder
    return a


def get_lcm(a, b):
    return a*b / get_gcd(a, b)


class NodeManager:
    def __init__(self, file_path: str):
        with open(file_path, "r") as file:
            raw_input = file.read()

        self.intructions = raw_input.splitlines()[0]
        self.nodes = self.ingest_nodes(raw_input.splitlines()[2:])

    def ingest_nodes(self, input_list: list[str]) -> dict[str]:
        """
        save dictionary of each node with a list current node = [left_node, right_node]
        :param input_list:
        :return:
        """
        node_dict = {}
        for n in input_list:
            current_node, node_adj = n.split(" = ")
            node_adj = node_adj.replace("(", "").replace(")", "").split(", ")
            node_dict[current_node] = node_adj
        return node_dict

    def traverse_map_one(self, start_node: str = "AAA") -> int:
        logger.info(f"Starting traverse for: {start_node}")
        i = 0
        number_of_instructions = len(self.intructions)
        current_node = start_node
        while not current_node.endswith("Z"):
            step_direction = self.intructions[i % number_of_instructions]
            current_node = self.get_node(current_node, step_direction)
            i += 1
        logger.info(
            f"Finished traverse for: {start_node} -> {current_node}, steps: {i}"
        )
        return i

    def traverse_map_two(self) -> int:
        """
        traverse map for multiple starts. Approach: find the steps by start and multiply them. All finish nodes are
        the start node but reversed.
                left -> ... -> finish
        start /
              \
               right -> ... -> finish
        :return:
        """
        current_nodes = [n for n in self.nodes.keys() if n.endswith("A")]
        logger.info(f"Starting nodes: {current_nodes}")

        # multiply number of starts with each other
        with Pool() as pool:
            total_steps = pool.map(self.traverse_map_one, current_nodes)
        # for start_node in current_nodes:
        #     total_steps *= self.traverse_map_one(start_node)
        # obtain least common multiple. It's just a loop...
        # get lcm per pair and reduce
        return reduce(get_lcm, total_steps, total_steps[0])

    def find_node(self, start_node: str, end_node: str, i: int = 0) -> int:
        """
        Traverse graph from start node to end node
        """
        logger.info(f"Starting traverse for: {start_node} -> {end_node}")
        number_of_instructions = len(self.intructions)
        current_node = start_node
        while not (current_node == end_node):
            step_direction = self.intructions[i % number_of_instructions]
            current_node = self.get_node(current_node, step_direction)
            i += 1
        logger.info(
            f"Finished traverse for: {start_node} -> {current_node}, steps: {i}"
        )
        return i

    def get_node(self, current_node: str, step_direction: str) -> str:
        step_direction = 1 if step_direction == "R" else 0
        return self.nodes[current_node][step_direction]


if __name__ == "__main__":
    path = "./data/day8/input.txt"
    b = NodeManager(path)
    # 15893216212025112758644933
    # 590825881487922400000000
    print(b.traverse_map_two())
