"""
Advent of Code 2023: Problem 9
"""

import argparse
from pathlib import Path
import re


def diff_step(seq: list[int]) -> list[int]:
    """
    Calculates the difference between consecutive terms, and
    returns as a list out.
    out[i] = seq[i+1] - seq[i]
    len(out) = len(seq) - 1

    Raises ValueError if len(seq) is 1.
    """
    if len(seq) == 1:
        raise ValueError("Cannot calculate differences from one-length sequence")
    return [s2 - s1 for s2, s1 in zip(seq[1:], seq[:-1])]


def get_diffs(seq: list[int]) -> list[int]:
    """
    Successively builds new sequences using diff_step. Terminates
    when it reaches a zero sequence. Returns the last element of
    each sequence calculated as a list.
    """
    seq_last = []
    while sum(abs(num) for num in seq) != 0:
        seq_last.append(seq[-1])
        seq = diff_step(seq)
    return seq_last


def get_next_element(seq: str) -> int:
    """
    Reads the sequence from string, and gets the next element in the
    given sequence. The next element is the sum of the list output
    by get_diffs.
    """
    return sum(get_diffs([int(num) for num in re.findall(r"-?\d+", seq)]))


def get_history_sum(input_file: Path | str) -> int:
    """
    Reads sequences from input_file (one sequence per line), calculates
    the next element in eqch sequence, and returns the sum of the next
    element of each sequence.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        next_elem = sum(get_next_element(line) for line in f)
    return next_elem


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 9")
    parser.add_argument("input_file", help="Input file")
    args = parser.parse_args()

    print(f"Sum of next elements is: {get_history_sum(Path(args.input_file))}")
