"""
Advent of Code 2023: Problem 8
"""

import argparse
from pathlib import Path
import re
from math import lcm


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
    start_nodes: list[str],
    end_nodes: list[str],
) -> tuple[list[str], int]:
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

    Starting and ending nodes are given as a list of tuples start_end_nodes =
    [(start_node,end_node)]. Paths for all tuples in the list are followed
    simultaneously. That is, if start_end_nodes has a single tuple, then the path
    is followed from start_node to end_node -- terminating if reached end_node,
    otherwise returning the current node and steps. However, if start_end_nodes
    has multiple tuples, path is followed for each tuple simultaneously -- a step
    now involving moving left or right for each tuple. Path is terminated only
    if all the end_node's are reached. Otherwise, a list of current_node's is
    returned.
    """
    current_nodes = start_nodes
    for ind, step in enumerate(network_path):
        if set(current_nodes) <= set(end_nodes):
            # At end nodes, terminate
            return end_nodes, ind
        ind_step = 0 if step == "L" else 1
        current_nodes = [
            network_map[current_node][ind_step] for current_node in current_nodes
        ]
    # If here, path did not terminate. Return current node
    return current_nodes, len(network_path)


def go_path(
    network_path: str,
    network_map: dict[str : tuple[str, str]],
    start_nodes: list[str],
    end_nodes: list[str],
) -> int:
    """
    Starting from given start_nodes, applies the given network_path repeatedly
    until end_nodes is reached. network_path is applied using network_map.
    Returns the number of steps it took to get to end_nodes. Starting and ending
    nodes are given using start_end_nodes = [(start_node,end_node)]. If
    start_end_nodes has mutiple tuples, each start_node is followed to its end_node
    simultaneously. All end_node's must be reached together for the function to
    finish.

    A ValueError is thrown is a loop is detected.
    """
    steps = 0
    current_nodes = [start_nodes]
    while not set(current_nodes[-1]) <= set(end_nodes):
        next_nodes, next_steps = go_path_one(
            network_path, network_map, current_nodes[-1], end_nodes
        )
        if next_nodes in current_nodes:  # Path loops back to the same position
            raise ValueError("Loop detected. Infinite steps needed")
        current_nodes.append(next_nodes)
        steps += next_steps
    return steps


def get_nodes(pattern: str, nodes: list[str]) -> list[str]:
    """
    Returns a list of nodes in nodes matching a given pattern
    """
    return [node for node in nodes if re.match(pattern, node)]

def go_path_lcm(
    network_path: str,
    network_map: dict[str : tuple[str, str]],
    start_nodes: list[str],
    end_nodes: list[str],
) -> int:
    """
    Calculates the steps to reach from each start_node to any end_node.
    Returns the lowest common multiplier of these steps.
    """
    steps = [
        go_path(network_path,network_map,[start_node],end_nodes) for start_node in start_nodes
    ]
    return lcm(*steps)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 8")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument(
        "--ghost", "-g", help="Follow map like a ghost if given.", action="store_true"
    )
    parser.add_argument(
        "--lcm",
        "-l",
        help="Uses LCM for ghost problem. Only used if --ghost is given",
        action="store_true",
    )
    args = parser.parse_args()

    user_path, user_map = read_map(Path(args.input_file))
    if args.ghost:
        user_start_nodes = get_nodes(r".{2}A", user_map.keys())
        user_end_nodes = get_nodes(r".{2}Z", user_map.keys())
    else:
        user_start_nodes = ["AAA"]
        user_end_nodes = ["ZZZ"]

    try:
        if not args.lcm:
            print(
                f"Path took {go_path(user_path,user_map,user_start_nodes,user_end_nodes)}"
            )
        else:
            print(
                f"Path took {go_path_lcm(user_path,user_map,user_start_nodes,user_end_nodes)}"
            )
    except ValueError as _:
        print("Cannot reach ZZZ from AAA using given path.")
