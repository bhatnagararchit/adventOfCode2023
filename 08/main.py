"""
Advent of Code 2023: Problem 8
"""

import argparse
from pathlib import Path
import re


def read_map(map_file: Path | str) -> tuple[str, dict[str : tuple[str, str]]]:
    """
    Reads the map from map_file. The file is assumed to have the path
    instructions in the first line, then a blank line and each line
    after describing the nodes of the map as
    (node) = (node_left,node_right)
    where node_left and node_right are nodes on the left or right of
    node respectively.

    Returns the path string as the first argument, and the map as a
    second argument. The map is stored as a dictionary of the form:
    {node: (node_left,node_right)}
    """
    with open(map_file, "r", encoding="utf-8") as f:
        # Get path string
        network_path = next(f).strip()
        # Ignore blank line
        next(f)
        # Get map
        network_map = {}
        for line in f:
            node, node_left, node_right = re.findall(r"[A-Z]+", line)
            network_map[node] = (node_left, node_right)
    return network_path, network_map


def go_path_one(
    network_path: str,
    network_map: dict[str : tuple[str, str]],
    start_node: str,
    end_node: str,
) -> tuple[str, int]:
    """
    Follows the given network_path once, through the network_map. Starts
    from given start_node. If end_node is encountered anytime, terminates.

    Network_path consists of 'L' and 'R' characters. At each step in the path,
    'L' indicates to go to the left node in the map and 'R' to the right. Each
    node in the map is indicated as a key, with a tuple as value. First element
    in the tuple is the left node, and second the right for that node.

    If end_node is not encountered in the path, returns the node where the path
    ends. If end_node is encountered in the path, returns the end_node. In both
    cases, returns the number of steps taken as the second argument in the path.
    """
    current_node = start_node
    for ind, step in enumerate(network_path):
        if current_node == end_node:
            # At end node, terminate
            return end_node, ind
        ind_step = 0 if step == "L" else 1
        current_node = network_map[current_node][ind_step]
    # If here, path did not terminate. Return current node
    return current_node, len(network_path)


def go_path(
    network_path: str,
    network_map: dict[str : tuple[str, str]],
    start_node: str = "AAA",
    end_node: str = "ZZZ",
) -> int:
    """
    Starting from given start_node, applies the given network_path repeatedly
    until end_node is reached. network_path is applied using network_map.
    Returns the number of steps it took to get to end_node.

    start_node and end_node default to 'AAA' and 'ZZZ' respectively.

    A ValueError is thrown is a loop is detected.
    """
    steps = 0
    current_node = [start_node]
    while current_node[-1] != end_node:
        next_node, next_steps = go_path_one(
            network_path, network_map, current_node[-1], end_node
        )
        if next_node in current_node:  # Path loops back to the same position
            raise ValueError("Loop detected. Infinite steps needed")
        current_node.append(next_node)
        steps += next_steps
    return steps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 8")
    parser.add_argument("input_file", help="Input file")
    args = parser.parse_args()

    user_path, user_map = read_map(Path(args.input_file))
    try:
        print(f"Path took {go_path(user_path,user_map)}")
    except ValueError as _:
        print("Cannot reach ZZZ from AAA using given path.")
