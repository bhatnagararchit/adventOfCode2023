"""
Advent of Code 2023: Problem 7
"""

import argparse
from pathlib import Path
from math import copysign, floor
from functools import cmp_to_key
from operator import itemgetter

CARD_VALUE = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def compare_hands(hand_a: str, hand_b: str) -> int:
    """
    Compares hand_a to hand_b. Returns +1 if hand_a is stronger,
    -1 if hand_b is stronger and 0 if both are equal.
    """
    # Check hand types
    type_a = get_hand_type(hand_a)
    type_b = get_hand_type(hand_b)
    if type_a != type_b:
        return int(copysign(1, type_a - type_b))
    # Check cards from left
    for card_a, card_b in zip(hand_a, hand_b):
        if CARD_VALUE[card_a] != CARD_VALUE[card_b]:
            return int(copysign(1, CARD_VALUE[card_a] - CARD_VALUE[card_b]))
    # Cards are equal
    return 0


def get_hand_type(hand: str) -> int:
    """
    Returns type of hand for given hand as int between 0 and 6.

    6 - Five of a kind
    5 - Four of a kind
    4 - Full house
    3 - Three of a kind
    2 - Two pair
    1 - One pair
    0 - High card

    Return values for the hands are ordered by their strength.
    """
    hand_type = 0  # Default to high pair
    match len(set(hand)):
        case 1:  # Five of a kind
            hand_type = 6
        case 2:  # Four of a kind or Full house
            match sum(hand[0] == h for h in hand[1:]):
                case 0 | 3:  # Four of a kind
                    hand_type = 5
                case 1 | 2:  # Full house
                    hand_type = 4
        case 3:  # Three of a kind or Two pair
            match sum(hand[0] == h for h in hand[1:]):
                case 2:  # Three of a kind
                    hand_type = 3
                case 1:  # Two paie
                    hand_type = 2
                case 0:  # Unknown, test next character
                    match sum(hand[1] == h for h in hand[2:]):
                        case 2 | 0:  # Three of a kind
                            hand_type = 3
                        case 1:  # Two pair
                            hand_type = 2
        case 4:  # One pair
            hand_type = 1
    return hand_type


def get_winnings(input_file: Path | str) -> int:
    """
    Returns the winnings
    """
    with open(input_file, "r", encoding="utf-8") as f:
        ranked_hands = []
        for line in f:
            # Get hand and bid
            hand, bid = line.split()
            ranked_hands.append((hand, int(bid)))
    winnings = 0
    ranked_hands.sort(key=lambda tup: cmp_to_key(compare_hands)(tup[0]))
    for rank, (_, bid) in enumerate(ranked_hands,start=1):
        winnings += rank * bid
    return winnings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 7")
    parser.add_argument("input_file", help="Input file")
    args = parser.parse_args()

    print(f"Winnings: {get_winnings(Path(args.input_file))}")
