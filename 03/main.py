"""
Advent of Code 2023: Problem 2
"""

import re
from pathlib import Path
import argparse


def read_input_file(input_file: str | Path) -> list[str]:
    """
    Reads given input file and returns a list of string. Each element in the list is a
    line in the input_file. Empty lines are discarded.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        out = [line.strip() for line in f if line.strip()]
    return out


def get_number_adjacent_elements(
    row_ind: int, col_start: int, col_end: int, input_matrix: list[str]
) -> str:
    """
    Given the location of a number -- which row (row index) and which columns it spans
    (col_start and col_end), looks into the input_matrix and returns the set of characters
    that are adjacent to the number in the input_matrix as a string.

    This function does not perform sanity checks on the indices -- if the indices are out-of-bounds
    or if the adjacent elements will be out-of-bounds, the output is non-sensical.
    """
    # Row and column indices of original input_matrix are now shifted by one
    row_above = input_matrix[row_ind - 1][col_start - 1 : col_end + 2]
    row_below = input_matrix[row_ind + 1][col_start - 1 : col_end + 2]
    col_left = input_matrix[row_ind][col_start - 1]
    col_right = input_matrix[row_ind][col_end + 1]
    # Return all adjacent
    return "".join([row_above, row_below, col_left, col_right])


def pad_matrix(
    input_matrix: list[str], num_row_pad: int = 1, num_col_pad: int = 1
) -> list[str]:
    """
    Pads input_matrix with given number of rows and columns. Padded rows and columns only have '.'
    Padding is done symmetrically in rows and columns.
    """
    # Pad columns first
    pad_col = "".join(["." for _ in range(num_col_pad)])
    padded_matrix = ["".join([pad_col, line, pad_col]) for line in input_matrix]
    pad_row = "".join(["." for _ in padded_matrix[0]])
    for _ in range(num_row_pad):
        padded_matrix.append(pad_row)
        padded_matrix.insert(0, pad_row)
    return padded_matrix


def get_part_numbers(input_matrix: list[str]) -> list[int]:
    """
    Finds all numbers in input_matrix that are adjacent (even diagonally) to a symbol (that is,
    not a number and not '.').
    """
    part_numbers = []
    # Create padded matrix for get adjacent elements -- 1 row and 1 col padding
    padded_matrix = pad_matrix(input_matrix)
    for ind_row, line in enumerate(padded_matrix):
        # Find numbers
        for num in re.finditer(r"\d+", line):
            # Check if this is a part number
            adjacent_elements = get_number_adjacent_elements(
                ind_row, num.start(), num.end() - 1, padded_matrix
            )
            if re.search(r"[^\d\.]+", adjacent_elements):
                part_numbers.append(int(num.group(0)))
    return part_numbers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 3")
    parser.add_argument("input_file", help="Input file")
    args = parser.parse_args()

    user_input_matrix = read_input_file(Path(args.input_file))
    print(f"Sum of part numbers is: {sum(get_part_numbers(user_input_matrix))}")
