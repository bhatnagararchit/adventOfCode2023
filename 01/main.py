"""
Advent of Code 2023: Problem 1
"""

import re
import argparse
from pathlib import Path


def get_calibration_number(input_string: str) -> int:
    """
    Calculates from given input_string the first and last digit, and combines to
    give a single two-digit number
    """
    # Get all digits from the string
    m = re.findall("[0-9]", input_string)
    # Concatenate first and last digit and return as integer
    return int(m[0] + m[-1])


def get_calibration_sum(input_file: Path | str) -> int:
    """
    Reads file, calculates calibration number for each line, returns sum of these
    calibration numbers
    """
    with open(input_file, "r", encoding="utf-8") as f:
        calibration_sum = 0
        for line in f:
            calibration_sum += get_calibration_number(line)
    return calibration_sum


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 1")
    parser.add_argument("input_file", help="Input file")
    args = parser.parse_args()

    # Print sum of calibration numbers
    print(f"Calibration sum is: {get_calibration_sum(Path(args.input_file))}")
