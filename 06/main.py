"""
Advent of Code 2023: Problem 6
"""

import re
import argparse
from pathlib import Path
from math import floor, ceil, sqrt


def read_file(
    input_file: Path | str, ignore_spaces: bool = False
) -> list[tuple[int, int]]:
    """
    Reads input file and returns the time and distance recorded for
    each race, as a list of tuples race_records. The time and distance
    recorded for the nth race are returned as race_records[n][0] and
    race_records[n][1] respectively, where n = 0,1,2,...

    If ignore_spaces is True, the spaces in time and distances recorded
    are ignored. The returned list then has only one tuple.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        # First line is time, second line is distance
        time, distance = list(f)
        time = re.findall(r"\d+", time)
        distance = re.findall(r"\d+", distance)
        if ignore_spaces:
            time = ["".join(time)]
            distance = ["".join(distance)]
        # Record as numbers
        race_records = [(int(t), int(d)) for t, d in zip(time, distance)]
    return race_records


def get_num_win(
    time: int, distance: int, init_vel: int = 0, vel_change: int = 1
) -> int:
    """
    Returns the numbers of ways to win a race -- that is, go a longer distance
    than given distance in the same amount of time. In a given race, the boat
    has a initial velocity of init_vel, which can be increased by pressing a button
    on the boat at the start in vel_change increments -- the velocity changes by
    vel_change for each time unit the button is held down. The boat does not move
    when the button is held down.

    To get the numbers of ways to win, let x be the amount of time the button is pressed
    and y the distance that the boat travels. Then, by above, we have:
        y = (init_vel + vel_change*x)*(time - x)
    We want the integer solutions for x where y > distance, which implies solving the
    quadratic inequality:
        vel_change*(x**2) + (init_vel - time*vel_change)*(x) + (distance - time*init_vel) < 0
    under the constraint 0 <= x <= time
    """
    if vel_change == 0:
        # Inequality becomes x < time - (distance/init_vel)
        if init_vel == 0:
            # No solution possible unless distance is 0
            if distance == 0:
                return time + 1
            return 0
        return ceil(time - distance / init_vel)
    # Calculate roots of quadratic
    b = time - init_vel / vel_change
    disc = b**2 - 4 * (distance - time * init_vel) / (vel_change)
    if disc <= 0:
        # No or equal roots -- look at sign of vel_change
        # We need to exceed the distance traveled -- equal roots is not good enough
        if vel_change > 0:
            return 0
        if floor(b / 2) == ceil(b / 2):
            # Integer root for vel_change < 0 corresponds to equal distance traveled
            return time
        return time + 1
    # Get distinct roots
    x_plus = 0.5 * (b + sqrt(disc))
    x_minus = 0.5 * (b - sqrt(disc))
    roots = [x_plus, x_minus]
    if vel_change > 0:
        # Solution within roots
        min_root = (
            min(roots) + 1 if floor(min(roots)) == ceil(min(roots)) else min(roots)
        )
        max_root = (
            max(roots) - 1 if floor(max(roots)) == ceil(max(roots)) else max(roots)
        )
        min_sol = ceil(max([0, min_root]))
        max_sol = floor(min([time, max_root]))
        return max_sol - min_sol + 1
    # vel_change is negative -- solution outside roots
    max_root = max(roots) + 1 if floor(max(roots)) == ceil(max(roots)) else max(roots)
    min_root = min(roots) - 1 if floor(min(roots)) == ceil(min(roots)) else min(roots)
    if min(roots) < 0 and max(roots) > time:
        return 0
    if min(roots) < 0:
        return time - ceil(max(roots)) + 1
    if max(roots) > time:
        return floor(min(roots)) + 1
    return floor(min(roots)) + 1 + time - ceil(max(roots)) + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 6")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument(
        "--ignore-spaces",
        help="If given, all spaces between numbers in time and distance line are ignored",
        action="store_true",
    )
    args = parser.parse_args()

    prod = 1
    for t, d in read_file(Path(args.input_file),args.ignore_spaces):
        prod *= get_num_win(t, d)
    print(f"Total number of ways to win are: {prod}")
