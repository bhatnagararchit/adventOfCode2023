"""
Advent of Code 2023: Problem 15
"""

import argparse
from pathlib import Path
from collections import OrderedDict

BOXES = [OrderedDict() for _ in range(256)]


def read_steps(step_file: Path | str) -> list[str]:
    """
    Reads the input steps in the step_file, and returns thems as a list
    of strings.

    step_file has a comma separated list of steps. Newlines are ignored.
    """
    with open(step_file, "r", encoding="utf-8") as f:
        steps = "".join(line for line in f)
    return steps.split(",")


def holiday_hash(input_string: str) -> int:
    """
    Returns the hash of an input string using the Holiday ASCII String Helper
    algorithm.

    Starting with current value of 0, the algorithm loops through each
    character, doing the following steps:
        * Increase current value by the ASCII code of the current character
        * Multiply current value by 17 and take remainder with 256
    The final current value is returned as the hash.

    In binary, 17 == 10001. Therefore, multiplying an integer with 17 and taking
    the remainder with 256 is the same as the last 8 bits of the addition of the
    integer with itself bitshifted by 4 to the left.
    """
    curr_value = 0
    for char in input_string:
        curr_value = (char.encode("ASCII")[0] + curr_value) & 255
        curr_value = ((curr_value << 4) + curr_value) & 255
    return curr_value


def holiday_hash_map(boxes: list[OrderedDict], step_string: str) -> None:
    """
    Modifies boxes following the instruction in step_string.
    """
    if "=" in step_string:
        label, focal_length = step_string.split("=")
    else:
        label = step_string.split("-")[0]
        focal_length = -1
    focal_length = int(focal_length)
    box_ind = holiday_hash(label)
    if focal_length >= 0:
        boxes[box_ind][label] = focal_length
    else:
        boxes[box_ind].pop(label, None)


def get_box_power(boxes: list[OrderedDict]) -> int:
    """
    Returns focusing power of all lenses in all boxes, summed up.
    """
    focus_power = 0
    for ind_box, box in enumerate(boxes, start=1):
        for ind_lens, focal_length in enumerate(box.values(), start=1):
            focus_power += ind_box * ind_lens * focal_length
    return focus_power


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 15")
    parser.add_argument("input_file", help="Input file", type=Path)
    parser.add_argument(
        "--focus-power",
        "-fp",
        help="If given, calculates sum of focusing powers",
        action="store_true",
    )
    args = parser.parse_args()

    user_steps = read_steps(args.input_file)
    if not args.focus_power:
        user_hash_sum = sum(holiday_hash(step) for step in user_steps)
        print(f"Sum of hash of each step is: {user_hash_sum}")
    else:
        for step in user_steps:
            holiday_hash_map(BOXES, step)
        print(f"Focusing power sum is: {get_box_power(BOXES)}")
