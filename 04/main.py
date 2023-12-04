"""
Advent of Code 2023: Problem 2
"""

import re
import argparse
from pathlib import Path


def get_card_score(winning_numbers: list[int], numbers_you_have: list[int]) -> int:
    """
    Returns the score of the card, given the winning numbers and numbers you have.
    If there are n numbers in numbers_you_have that also occur in winning_numbers,
    the score for the card is 2**(n-1) if n >= 1 and zero otherwise
    """
    score = sum((num in winning_numbers) for num in numbers_you_have)
    return int(2 ** (score - 1))


def read_card(card_string: str) -> tuple[list[int], list[int]]:
    """
    Reads card and returns two lists of integers -- list of winning numbers and
    list of numbers you have
    """
    # Separate into card id, winning numbers and numbers you have
    _, numbers = card_string.split(":")
    winning_numbers, numbers_you_have = numbers.split("|")
    # Get numbers and convert to int
    winning_numbers = [int(num) for num in re.findall(r"\d+", winning_numbers)]
    numbers_you_have = [int(num) for num in re.findall(r"\d+", numbers_you_have)]
    return winning_numbers, numbers_you_have


def get_total_score(input_file: Path | str) -> int:
    """
    Reads all cards in given file (one line per card), calculates score for each
    card, and returns the sum.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        total_score = sum(get_card_score(*read_card(line)) for line in f)
    return total_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 4")
    parser.add_argument("input_file", help="Input file")
    args = parser.parse_args()

    print(f"Total points for given cards is: {get_total_score(Path(args.input_file))}")
