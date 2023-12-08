"""
Advent of Code 2023: Problem 5
"""

import re
import argparse
from pathlib import Path
import warnings
from math import inf


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


def apply_map_number(map_array: list[list[int]], source_number: int) -> int:
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


def apply_map_range(
    map_array: list[list[int]], source_ranges: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """
    Given a map array and a source_range, applies the map onto the input
    number and returns the numbers that the source_range is mapped to.

    map_array is a list of lists. Each list in map_array is of len(3):
    [destination_start, source_start, range_len]. source_range is a 2 element
    tuple (source_num_start, source_num_len), which represents numbers from
    source_num_start to source_num_start + source_num_len - 1. For each number
    in
    """
    mapped_numbers = []
    for destination_start, source_start, range_len in map_array:
        new_source_ranges = []
        for source_range in source_ranges:
            if (
                source_start + range_len - 1 < source_range[0]
                or source_range[0] + source_range[1] - 1 < source_start
            ):
                new_source_ranges.append(source_range)
                continue
            # Map given range
            mapped_start = max(source_start, source_range[0])
            mapped_end = min(
                source_start + range_len - 1, source_range[0] + source_range[1] - 1
            )
            mapped_len = mapped_end - mapped_start + 1
            mapped_numbers.append(
                (mapped_start + destination_start - source_start, mapped_len)
            )
            # Split source into remaining ranges
            if (
                mapped_start == source_range[0] and mapped_len == source_range[1]
            ):  # Full match
                continue
            elif mapped_start == source_range[0]:
                new_source_ranges.append((mapped_end + 1, source_range[1] - mapped_len))
            elif mapped_end == source_range[0] + source_range[1] - 1:
                new_source_ranges.append(
                    (source_range[0], source_range[1] - mapped_len)
                )
            else:
                new_source_ranges.append(
                    (source_range[0], mapped_start - source_range[0])
                )
                new_source_ranges.append(
                    (mapped_end + 1, source_range[0] + source_range[1] - 1 - mapped_end)
                )
        source_ranges = new_source_ranges
    # Add unmapped back
    mapped_numbers.extend(source_ranges)
    return mapped_numbers


def apply_map(
    map_array: list[list[int]],
    source_input: list[tuple[int, int]] | int,
    is_range: bool,
) -> list[tuple[int, int]] | int:
    """
    Wrapper for applying maps to numbers or ranges
    """
    if is_range:
        return apply_map_range(map_array, source_input)
    return apply_map_number(map_array, source_input)


def get_seed_numbers(
    seed_string: str, is_range: bool
) -> tuple[list[int] | list[tuple[int, int]], bool]:
    """
    Returns the seed numbers in seed_string. The function reads all the
    numbers in the given seed_string. Seed numbers are then intepreted
    based on value of is_range. If is_range is False, the numbers read
    from seed_string are considered the given seed numbers and returned
    as is. If is_range is True, the numbers in seed_string are intepreted
    as a set of pairs written consecutively. In each pair, the first
    number describes the starting value and the second number the length
    of the range using the starting value.

    For example, if seed_string is 'seeds: 79 14 55 13', then:
    If is_range is False: seed numbers are 79,14,55,13
    If is_range is True: seed numbers are 79,80,...,92 , 55,56,...67

    If there are odd number of numbers read in seed_string and is_range is
    set to True, a warning is raised and is_range is set to False.
    """
    seed_num_read = [int(num) for num in re.findall(r"\d+", seed_string)]
    if len(seed_num_read) % 2 != 0 and is_range:
        warnings.warn("Odd number of input seed numbers, cannot divide into pairs")
        is_range = False
    if is_range:
        return [
            (seed_num_read[ind], seed_num_read[ind + 1])
            for ind in range(0, len(seed_num_read), 2)
        ], is_range
    else:
        return seed_num_read, is_range


def get_min_seed_mapping_number(seed_numbers: list[int], map_strings: list[str]) -> int:
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

    is_range is passed to get_seed_numbers, which interprets the seeds:... line
    to obtain the seed numbers. See get_seed_numbers for details.

    Returns a list of tuples -- each containing the initial seed number as the
    first element and the final mapped number as the second element.
    """
    min_mapping = inf
    for seed in seed_numbers:
        seed_mapped = seed
        for map_string in map_strings:
            seed_mapped = apply_map(read_map(map_string), seed_mapped, False)
        if min_mapping > seed_mapped:
            min_mapping = seed_mapped
    return min_mapping


def get_min_seed_mapping_ranges(
    seed_ranges: list[tuple[int, int]], map_strings: list[str]
) -> int:
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

    is_range is passed to get_seed_numbers, which interprets the seeds:... line
    to obtain the seed numbers. See get_seed_numbers for details.

    Returns a list of tuples -- each containing the initial seed number as the
    first element and the final mapped number as the second element.
    """
    for map_string in map_strings:
        seed_ranges = apply_map(read_map(map_string), seed_ranges, True)
    return min(seed_ranges, key=lambda tup: tup[0])[0]


def get_min_seed_mapping(
    seed_input: list[tuple[int, int]] | list[int],
    map_strings: list[str],
    is_range: bool,
) -> int:
    """
    Gets minimum mapping for input seeds using maps in map_strings. is_range defines
    if seed_input is a list of numbers (is_range == False) or a list of tuples, each
    defining a range of seed numbers (is_range == True).
    """
    if is_range:
        return get_min_seed_mapping_ranges(seed_input, map_strings)
    return get_min_seed_mapping_number(seed_input, map_strings)


def get_min_location(input_file: Path | str, is_range: bool) -> int:
    """
    Reads given file for seed numbers and maps. Applies all maps sequentially to seed
    numbers, and returns the lowest mapped value. is_range determines if the read
    seed numbers are interpreted as ranges (is_range == True) or numbers
    (is_ranges == False).
    """
    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()
    data = data.split("\n\n")
    # Get seeds
    seed_numbers, is_range = get_seed_numbers(data[0], is_range)
    # Get maps
    map_strings = [map_string.split(":")[1] for map_string in data[1:]]
    # Return minimum mapping
    return get_min_seed_mapping(seed_numbers, map_strings, is_range)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 5")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument(
        "--seed-range",
        "-sr",
        help="If given, seed line is interpreted as ranges",
        action="store_true",
    )
    args = parser.parse_args()

    # Get lowest mapped location
    print(
        f"The lowest location number is {get_min_location(Path(args.input_file),args.seed_range)}"
    )
