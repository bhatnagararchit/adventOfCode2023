"""
Advent of Code 2023: Problem 14
"""

import argparse
from pathlib import Path
import numpy as np
import numpy.typing as npt


def read_map(map_file: Path | str) -> npt.NDArray[np.int32]:
    """
    Reads given map of rocks into a numpy array.
    """
    with open(map_file, "r", encoding="utf-8") as f:
        rock_map = []
        for line in f:
            rock_map.append([])
            for char in line.strip():
                match char:
                    case ".":
                        rock_map[-1].append(0)
                    case "O":
                        rock_map[-1].append(1)
                    case "#":
                        rock_map[-1].append(-1)
                    case _:
                        raise ValueError(f"Unknown character {char}")
    return np.array(rock_map, dtype=np.int32)


def rotate_tilt_map(
    rock_map: npt.NDArray[np.int32], num: int = 1
) -> npt.NDArray[np.int32]:
    """
    Rotates the map by 90 degrees to the left, then tilts the map towards the
    left. All rollable rocks in any column roll until they reach the top or
    hit another rock. This is done for num number of times, default to 1.
    The rotated and tilted map is returned.
    """
    old_rock_maps = []
    ind_rotate = 0
    while ind_rotate < num:
        #print(ind_rotate)
        # Rotate map and pad for easier comparison in tilting
        rock_map = np.pad(np.rot90(rock_map, -1), 1, "constant", constant_values=-1)
        # Tilt map
        for row in rock_map:
            ind_unroll = np.where(row < 0)[0]
            for ind1, ind2 in zip(ind_unroll[:-1], ind_unroll[1:]):
                row[(ind1 + 1) : ind2].sort()
        # Unpad
        rock_map = rock_map[1:-1, 1:-1]
        # Jump by number of times if matches
        for ind_map, old_rock_map in enumerate(old_rock_maps):
            if (old_rock_map == rock_map).all():
                len_cycle = len(old_rock_maps) - ind_map
                ind_rotate += ((num - ind_rotate) // len_cycle)*len_cycle + 1
                old_rock_maps = []
                break
        else:
            # Copy into old_rock_maps
            old_rock_maps.append(rock_map.copy())
            ind_rotate += 1
    return rock_map


def get_load(rock_map: npt.NDArray[np.int32], num: int = 1) -> int:
    """
    Calculates the load on the left by each row. Returns sum of load.

    The load of a row is calculated by assigning each rollable rock in
    the row a score based on how close it is to the left edge of the row:
    for a rollable rock at the left edge, it is assigned a score of the
    length of the row, and for a rollable rock at the right edge the score
    assigned is 1. The load of the row is then the sum of the assigned
    scores.
    """
    num_rows, num_cols = rock_map.shape
    match num % 4:
        case 0:
            score_map = np.tile((np.arange(num_rows)[::-1] + 1)[:, None], (1, num_cols))
        case 1:
            score_map = np.tile((np.arange(num_cols) + 1)[None, :], (num_rows, 1))
        case 2:
            score_map = np.tile((np.arange(num_rows) + 1)[:, None], (1, num_cols))
        case 3:
            score_map = np.tile((np.arange(num_cols)[::-1] + 1)[None, :], (num_rows, 1))
    rock_map[rock_map < 0] = 0
    return int(np.sum(score_map * rock_map))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 14")
    parser.add_argument("input_file", help="Input file", type=Path)
    parser.add_argument(
        "--rotate",
        "-r",
        help="Number of rotations, default 1. A spin (NWSE) can be simulated by 4 rotations.",
        default=1,
        type=int,
    )
    args = parser.parse_args()

    user_map = read_map(args.input_file)
    tilt_map = rotate_tilt_map(user_map, args.rotate)
    print(
        f"Total load on north after tilting is: {get_load(tilt_map,args.rotate)}"
    )
