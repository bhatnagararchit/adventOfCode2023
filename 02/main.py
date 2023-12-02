"""
Advent of Code 2023: Problem 2
"""

import re

CUBE_COLOR_INDICES = {
    'red': 0,
    'green': 1,
    'blue': 2
}

def read_game_data(game_line: str) -> tuple[int, tuple[tuple[int]]]:
    '''
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
    '''
    # Split game line into game id and separate draws
    game_id, game_draws = game_line.split(':')
    game_draws = game_draws.strip().split(';')
    # Identify game ID
    game_id = re.findall('[0-9]+',game_id)
    game_id = int(game_id[0])
    # Parse draws
    game_out = []
    for game_draw in game_draws:
        out_draw = list(range(len(CUBE_COLOR_INDICES)))
        for color, ind_color in CUBE_COLOR_INDICES.items():
            # Search for given color
            m = re.findall(f'[0-9]+(?= {color})',game_draw)
            # Convert to integer and sum
            out_draw[ind_color] = sum(int(match_num) for match_num in m)
        # Convert to tuple and append
        game_out.append(tuple(out_draw))
    # Convert out to tuple and return
    return game_id, tuple(game_out)

