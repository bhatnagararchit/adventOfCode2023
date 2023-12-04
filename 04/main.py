"""
Advent of Code 2023: Problem 2
"""

import re
import argparse
from pathlib import Path
from collections import deque


def get_match_card(winning_numbers: list[int], numbers_you_have: list[int]) -> int:
    """
    Returns the number of numbers_you_have that are present in winning_numbers
    """
    return sum((num in winning_numbers) for num in numbers_you_have)


def get_card_score(winning_numbers: list[int], numbers_you_have: list[int]) -> int:
    """
    Returns the score of the card, given the winning numbers and numbers you have.
    If there are n numbers in numbers_you_have that also occur in winning_numbers,
    the score for the card is 2**(n-1) if n >= 1 and zero otherwise
    """
    score = get_match_card(winning_numbers, numbers_you_have)
    return int(2 ** (score - 1))


def read_card(card_string: str) -> tuple[list[int], list[int]]:
    """
    Reads card and returns two lists of integers: list of winning numbers and
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


def get_total_number_cards(input_file: Path | str) -> int:
    """
    Returns total number of cards obtained under scoring scheme in Part 2. In
    Part 2, a card wins 1 copy each of the next n cards if n numbers on the
    right side of the card (numbers you have) are also on the right (winning
    numbers). Given a set of cards ordered by their IDs, this function returns
    the total number of cards (including the original cards) that are obtained
    via this scheme. To get only the number of copies, subtract the initial
    numbers of cards.

    Implementation is done via maintaining a queue of the number of copies of
    the next cards, and looping through the cards. At each card, the queue
    stores the number of copies for next consecutive cards that is known based
    on the previous cards. The number of copies of the current card is obtained
    by popping at the left the number of copies created by the previous card of
    the current card and adding one to it. If the queue is empty, that means no
    previous copies of the current card were made. The queue is then updated
    with the copies that the current card makes. If the queue already contains
    information about the next cards, it is updated. If not, the queue is appended
    to.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        # Queue to keep track of copies
        queue_copies = deque()
        # Total number of cards
        num_cards = 0
        for card in f:
            # Get number of copies of this card
            try:
                num_copies = queue_copies.popleft() + 1
            except IndexError as _:
                num_copies = 1
            num_cards += num_copies
            # Get how many cards to copy next
            copy_cards = get_match_card(*read_card(card))
            # Update queue
            for ind in range(copy_cards):
                try:
                    queue_copies[ind] += num_copies
                except IndexError as _:
                    queue_copies.append(num_copies)
    return num_cards


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 4")
    parser.add_argument("input_file", help="Input file")
    args = parser.parse_args()

    print(
        f"(Part 1) Total points for given cards is: {get_total_score(Path(args.input_file))}"
    )
    print(
        f"(Part 2) Total number of cards obtained is: {get_total_number_cards(Path(args.input_file))}"
    )
