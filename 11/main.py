"""
Advent of Code 2023: Problem 11
"""

import argparse
from pathlib import Path
import re
from itertools import combinations


def read_map(map_file: Path | str) -> list[list[int, int]]:
    """
    Reads the input galaxy map from given file, returning a list of coordinates of the
    galaxies in the input map.

    Galaxies are represented by #, empty space by . in the input file.
    """
    galaxy_location = []
    with open(map_file, "r", encoding="utf-8") as f:
        for ind_line, line in enumerate(f):
            galaxy_location.extend(
                [[ind_line, m.start()] for m in re.finditer("#", line)]
            )
    return galaxy_location


def expand_galaxy_coords(galaxy_coords: list[list[int, int]]) -> list[list[int, int]]:
    """
    Takes as input galaxy coordinates before expansion, and returns the galaxy coordinates
    after expansion.

    Rows and columns which do not contain any galaxies expand. In other words, if there
    is no galaxy in row r or column c, then all galaxies in rows r+1,... or column c+1,...
    are shifted by 1 (i.e., galaxies in rows r+1,... -> r+2,... and same for columns).
    Repeated application of this rule yields the coordinates of the galaxies after expansion.
    """
    # Get list of rows and columns where atleast one galaxy is present
    row_present = []
    col_present = []
    for row, col in galaxy_coords:
        row_present.append(row)
        col_present.append(col)
    row_present = sorted(set(row_present))
    col_present = sorted(set(col_present))

    # Expansion by shifting rows and columns by one
    def num_shifts(ind, ind_present):
        return ind - sum(ind_p < ind for ind_p in ind_present)

    new_galaxy_coords = [
        (row + num_shifts(row, row_present), col + num_shifts(col, col_present))
        for row, col in galaxy_coords
    ]
    return new_galaxy_coords


def pairwise_manhattan_dist(coords: list[int, int]) -> list[int]:
    """
    Returns the pairwise manhattan distance between given coords as a list.
    Indices in list are as per the convention of itertools.combinations.
    """
    dist = []
    for coord1, coord2 in combinations(coords, 2):
        dist_row = abs(coord1[0] - coord2[0])
        dist_col = abs(coord1[1] - coord2[1])
        dist.append(dist_row + dist_col)
    return dist


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 11")
    parser.add_argument("input_file", help="Input file", type=Path)
    args = parser.parse_args()

    user_galaxy_coords = read_map(args.input_file)
    user_expanded_galaxy_coords = expand_galaxy_coords(user_galaxy_coords)
    user_dists = pairwise_manhattan_dist(user_expanded_galaxy_coords)
    print(f"Sum of pairwise distances between galaxies: {sum(user_dists)}")
