"""
Advent of Code 2023: Problem 2
"""

import re
from pathlib import Path
import argparse

CUBE_COLOR_INDICES = {"red": 0, "green": 1, "blue": 2}


def read_game_data(game_line: str) -> tuple[int, tuple[tuple[int]]]:
    """
    Reads the outputs of a game.

    For each game, two values are returned. The first output is the game ID. The second output
    is a tuple of tuples containing the results of all draws in that game.

    The tuple of tuples is structured as follows: The nth draw is represented as the nth element
    of the outer tuple. In each draw (that is, any element of the outer tuple), the number of
    drawn cubes for each color are recorded based on the indices set in CUBE_COLOR_INDICES. So,
    for example, the number of cubes of color key_color in nth draw of the given game are
    recorded at the CUBE_COLOR_INDICES[key_color] index of the nth element of the output tuple
    of tuples -- that is, at out[n][CUBE_COLOR_INDICES[key_color]] if id, out are the outputs
    of this function.
    """
    # Split game line into game id and separate draws
    game_id, game_draws = game_line.split(":")
    game_draws = game_draws.strip().split(";")
    # Identify game ID
    game_id = re.findall("[0-9]+", game_id)
    game_id = int(game_id[0])
    # Parse draws
    game_out = []
    for game_draw in game_draws:
        out_draw = list(range(len(CUBE_COLOR_INDICES)))
        for color, ind_color in CUBE_COLOR_INDICES.items():
            # Search for given color
            m = re.findall(f"[0-9]+(?= {color})", game_draw)
            # Convert to integer and sum
            out_draw[ind_color] = sum(int(match_num) for match_num in m)
        # Convert to tuple and append
        game_out.append(tuple(out_draw))
    # Convert out to tuple and return
    return game_id, tuple(game_out)


def check_game_possible(game_draws: tuple[tuple[int]], total_cubes: tuple[int]) -> bool:
    """
    Checks if given game is possible, given all the draws in the game (game_draws) and the total
    number of cubes of each color in the bag (total_cubes).

    game_draws is expected in the same format that read_game_data outputs -- that is, the nth draw
    is stored in game_draws[n], with number of cubes of color key_color drawn in the nth draw stored
    in game_draws[n][CUBE_COLOR_INDICES[key_color]]. total_cubes is supposed to store the total
    numbers of cubes of color key_color in total_cubes[CUBE_COLOR_INDICES[key_color]].

    Given this, the function checks if any draws in game_draws have more cubes of a color than those
    given in total_cubes. Draws are assumed to be done with replacement. If any draw in the game has
    more cubes for any color than the number of cubes in total_cubes for that color, the function
    returns False -- that is the game is impossible. Otherwise, the function returns True --
    that is, the game is possible.
    """
    # Assume game is possible at first
    for game_draw in game_draws:
        # Check each color in draw -- given assumption of same structure in game_draws[n]
        # and total_cubes, no need to call CUBE_COLOR_INDICES
        for game_draw_color, total_cubes_color in zip(game_draw, total_cubes):
            if game_draw_color > total_cubes_color:
                # More cubes than what total_cubes has have been drawn -- game is impossible
                return False
    # If here -- game is possible. Return True
    return True


def get_game_possible_min_cubes(game_draws: tuple[tuple[int]]) -> tuple[int]:
    """
    Returns the minimum number of cubes of each color required for all draws of a game -- given as
    game_draws -- to be possible.

    game_draws is expected in the same format that read_game_data outputs -- that is, the nth draw
    is stored in game_draws[n], with number of cubes of color key_color drawn in the nth draw stored
    in game_draws[n][CUBE_COLOR_INDICES[key_color]]. min_cubes -- which is returned -- stores the
    minimum required number of cubes of color key_color in min_cubes[CUBE_COLOR_INDICES[key_color]].

    The minimum number of cubes required for all draws to be possible is the maximum number of cubes
    observed for each color in the draws. This function calculates the maximum number of cubes, for
    each color separately, observed in game_draws.
    """
    min_cubes = [0 for _ in CUBE_COLOR_INDICES]
    for game_draw in game_draws:
        # Given assumption of same structure in game_draws[n] and min_cubes,
        # no need to call CUBE_COLOR_INDICES
        for ind, (game_draw_color, min_cubes_color) in enumerate(
            zip(game_draw, min_cubes)
        ):
            if min_cubes_color < game_draw_color:
                min_cubes[ind] = game_draw_color
    return min_cubes


def get_power(set_cubes: tuple[int]) -> int:
    """
    Returns the product of the number of cubes of each color, specified in set_cubes.
    """
    power = 1
    for num in set_cubes:
        power *= num
    return power


def get_possible_games(input_file: Path | str, total_cubes: tuple[int]) -> int:
    """
    Reads all games from input_file, checks each again the total number of cubes given in
    total_cubes, and returns the sum of indices of games which are possible.

    total_cubes is assumed to store the total numbers of cubes of color key_color in
    total_cubes[CUBE_COLOR_INDICES[key_color]]. All draws in each game are supposed to be with
    replacement.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        possible_game_id_sum = 0
        for line in f:
            game_id, game_draws = read_game_data(line)
            if check_game_possible(game_draws, total_cubes):
                possible_game_id_sum += game_id
    return possible_game_id_sum


def get_power_min_cubes(input_file: Path | str) -> int:
    """
    Reads all games from input_file, calculates the minimum set of cubes needed for each game,
    calculates the power of the minimum set, and returns the sum of these powers.
    
    All draws in each game are supposed to be with replacement.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        sum_power_min_cubes = 0
        for line in f:
            _, game_draws = read_game_data(line)
            min_cubes = get_game_possible_min_cubes(game_draws)
            sum_power_min_cubes += get_power(min_cubes)
    return sum_power_min_cubes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 2")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument(
        "--total_cubes",
        "-tc",
        help=f"Total number of cubes ({''.join([f'{ind_color}th for {color}, ' for color, ind_color in CUBE_COLOR_INDICES.items()])})",
        nargs=len(CUBE_COLOR_INDICES),
        type=int,
    )
    args = parser.parse_args()

    if args.total_cubes is not None:
        # Print sum of game IDs of possible games for given total cubes if total cubes is set
        print(
            f"Sum of game IDs of possible games is: {get_possible_games(Path(args.input_file),args.total_cubes)}"
        )
    else:
        # Print sum of powers of minimum set of cubes for each game if total cubes is not set
        print(
            f"Sum of powers of minimum set of all games is: {get_power_min_cubes(Path(args.input_file))}"
        )
