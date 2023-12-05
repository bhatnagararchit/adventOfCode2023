"""
Advent of Code 2023: Problem 5
"""

import re
import argparse
from pathlib import Path


def read_map(map_string: str) -> list[list[int]]:
    """
    Reads a given map string into a list of list of ints. Map string
    is supposed to have only the numbers, not the header indicating which
    map it is.
    """
    map_string = map_string.strip().split("\n")
    map_array = [
        [int(num) for num in re.findall(r"\d+", row_string)]
        for row_string in map_string
    ]
    return map_array


def apply_map(map_array: list[list[int]], source_number: int) -> int:
    """
    Given a map array and an source_number, applies the map onto the input
    number and returns the number that the source_number is mapped to.

    map_array is a list of lists. Each list in map_array is of len(3):
    [destination_start, source_start, range_len]. If source_start <=
    source_number < source_start + range_len, then source_number is mapped
    to destination_start + (source_number - source_start). In this function,
    the mapped number is returned at the first hit -- that is, if a row matches
    the criteria, then no subsequent rows are checked. If no row matches the
    given criteria, then source_number is mapped to itself.
    """
    for destination_start, source_start, range_len in map_array:
        if source_start <= source_number < source_start + range_len:
            return destination_start + (source_number - source_start)
    return source_number


def get_seed_mappings(input_file: Path | str) -> list[tuple[int, int]]:
    """
    Reads the input file, extracts the seed numbers and various maps. Seed
    numbers are specified at the start of the file as 'seeds: ...\n\n' where ...
    are the seed numbers. Each map, which are applied in order of appearence
    in the file, is specified as 'map header:\n a1 b1 c1\n a2 b2 c2 ... \n\n'
    where an bn cn represent the nth row of the map. For example, the following
    file input represents a set of seeds with one map to apply:
    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    See apply_map for details on the format of the map rows.

    Returns a list of tuples -- each containing the initial seed number as the
    first element and the final mapped number as the second element.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()

    # Split into seeds and maps
    data = data.split("\n\n")
    # Get seeds
    seeds = [int(num) for num in re.findall(r"\d+", data[0].split(":")[1])]
    seeds_mapped = seeds.copy()
    # Apply each map in order
    for map_string in data[1:]:
        # Get rid of header
        map_string = map_string.split(":")[1]
        # Apply map
        for ind, seed in enumerate(seeds_mapped):
            seeds_mapped[ind] = apply_map(read_map(map_string), seed)
    return list(zip(seeds, seeds_mapped))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 5")
    parser.add_argument("input_file", help="Input file")
    args = parser.parse_args()

    # Get lowest mapped location
    mapped_locations = get_seed_mappings(Path(args.input_file))
    smallest_location_map = sorted(mapped_locations, key=lambda tup: tup[1])
    print(f"The lowest location number is {smallest_location_map[0][1]}")
