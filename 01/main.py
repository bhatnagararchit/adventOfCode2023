"""
Advent of Code 2023: Problem 1
"""

import re
import argparse
from pathlib import Path


def get_calibration_number(input_string: str, match_type: bool) -> int:
    """
    Calculates from given input_string the first and last digit, and combines to
    give a single two-digit number
    """
    if match_type:
        # Part 2: Replace digit names with digit characters
        input_string = replace_digit_names(input_string)
    # Get all digits from the string
    m = re.findall("[0-9]", input_string)
    # Concatenate first and last digit and return as integer
    return int(m[0] + m[-1])


def replace_digit_names(input_string: str) -> str:
    """
    Replaces instances of the digit names with the digits themselves in input_string.
    Required for Part 2 of problem 1.
    """

    # Define function for replacement
    def replace_digit(matchobj):
        match matchobj.group():
            case "one":
                return "1"
            case "two":
                return "2"
            case "three":
                return "3"
            case "four":
                return "4"
            case "five":
                return "5"
            case "six":
                return "6"
            case "seven":
                return "7"
            case "eight":
                return "8"
            case "nine":
                return "9"
            case "twone":
                return "21"
            case "oneight":
                return "18"
            case "eightwo":
                return "82"
            case "threeight":
                return "38"
            case "fiveight":
                return "58"
            case "sevenine":
                return "79"
            case "nineight":
                return "98"
            case _:
                return ""

    # Replace digit names in input_string
    m = re.sub(
        "(twone|oneight|eightwo|threeight|fiveight|sevenine|nineight)", replace_digit, input_string
    )
    m = re.sub("(one|two|three|four|five|six|seven|eight|nine)",replace_digit,m)
    # Return replaced string
    return m


def get_calibration_sum(input_file: Path | str, match_type: bool) -> int:
    """
    Reads file, calculates calibration number for each line, returns sum of these
    calibration numbers
    """
    with open(input_file, "r", encoding="utf-8") as f:
        calibration_sum = 0
        for line in f:
            calibration_sum += get_calibration_number(line,match_type)
    return calibration_sum


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 1")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument(
        "-dn",
        "--digit-names",
        action="store_true",
        help="If present, digit names are replaced with digits in input strings",
    )
    args = parser.parse_args()

    # Print sum of calibration numbers
    print(f"Calibration sum is: {get_calibration_sum(Path(args.input_file),args.digit_names)}")
