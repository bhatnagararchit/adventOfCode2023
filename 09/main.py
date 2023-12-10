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


def get_diffs(seq: list[int], backward: bool) -> list[int]:
    """
    Successively builds new sequences using diff_step. Terminates
    when it reaches a zero sequence. Returns the last element of
    each sequence calculated as a list.

    If backward flag is True, then instead of returning the last
    elements, the function returns a list of the first elements.
    """
    seq_last = []
    while sum(abs(num) for num in seq) != 0:
        seq_last.append(seq[0] if backward else seq[-1])
        seq = diff_step(seq)
    return seq_last


def get_next_element(seq: str, backward: bool) -> int:
    """
    Reads the sequence from string, and gets the next element in the
    given sequence.

    If backward is False, the next element is the sum of the list
    returned by get_diffs.

    If backward is True, the next element is the alternating sum of
    the list returned by get_diffs.

    backward flag is also passed to get_diffs.
    """

    # Make generator for generating alternating or direct sum
    def gen_ones(alternating: bool) -> int:
        """
        If alternating is True, returns a generator that produces the
        sequence 1,-1,1,-1,... . Otherwise, produces the sequence
        1,1,1,1,...
        """
        x = 1
        while True:
            yield x
            x = -x if alternating else x

    diff_seq = get_diffs([int(num) for num in re.findall(r"-?\d+", seq)], backward)
    return sum(alt * num for alt, num in zip(gen_ones(backward), diff_seq))


def get_history_sum(input_file: Path | str, backward: bool) -> int:
    """
    Reads sequences from input_file (one sequence per line), calculates
    the next element in eqch sequence, and returns the sum of the next
    element of each sequence.

    backward flag is passed to get_next_element.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        next_elem = sum(get_next_element(line, backward) for line in f)
    return next_elem


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 9")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument(
        "--backward",
        "-b",
        help="If given, returns the sum of elements extrapolated in the left direction.",
        action="store_true",
    )
    args = parser.parse_args()

    print(
        f"Sum of next elements is: {get_history_sum(Path(args.input_file),args.backward)}"
    )
