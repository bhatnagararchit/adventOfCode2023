"""
Advent of Code 2023: Problem 16
"""

import argparse
from pathlib import Path
import re

PART_NAMES = ["x", "m", "a", "s"]


def read_part(part_string: str) -> dict[str, int]:
    """
    Reads the part specified in string of the form {x=%d,m=%d,a=%d,s=%d}.
    Returns a dictionary with keys 'x','m','a','d', with values as the
    corresponding numbers in part_string.
    """
    return {
        part_name: int(re.search(f"(?<={part_name}=)\\d+", part_string).group(0))
        for part_name in PART_NAMES
    }


def read_workflows(workflows: list[str]) -> dict[str, list[str]]:
    """
    Reads the given list of workflows, and returns a dictionary. Each string in
    workflows is of the form name{rule,rule,...,rule}. See apply_workflow for the
    format of rule. The return dictionary is of the form {name: [rule,rule,...]}.
    """
    workflow_dict = {}
    for workflow_string in workflows:
        name, rules, _ = re.split(r"\{|\}", workflow_string)
        workflow_dict[name] = rules.split(",")
    return workflow_dict


def read_file(input_file: Path) -> tuple[dict[str, list[str]], list[dict[str, int]]]:
    """
    Reads given file for workflows and parts. In given file, each line from the start
    is a workflow (see format in read_workflows); until an empty line is reached.
    After the empty line, each line is a part (see format in read_part).

    Returns a dictionary with the workflows, and a list of dictionaries for the parts.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()
    workflows, parts = data.split("\n\n")
    workflows = read_workflows(workflows.splitlines())
    parts = [read_part(part) for part in parts.splitlines()]
    return workflows, parts


def apply_workflow(rules: list[str], part_dict: dict[str, int]) -> str:
    """
    Applies workflow specified in rules to the part described in part_dict.
    Returns the name of the workflow to follow next.

    rules is a list of strings which are applied in order. Each rule is of
    the one of 2 forms -- condition:name or name. If a rule is of form
    condition:name, then the condition is evaluated for the given part. If
    True, the function returns the name of the workflow corresponding to the
    condition that should be followed next. If rule is of the form name, then
    the name is returned directly.
    """
    for rule in rules:
        try:
            cond, name = rule.split(":")
            part_name, val = re.split(r"\<|\>", cond)
            if "<" in cond:
                return_flag = part_dict[part_name] < int(val)
            else:
                return_flag = part_dict[part_name] > int(val)
            if return_flag:
                return name
        except ValueError as _:
            return rule
    raise ValueError("Workflow terminated with no output workflow.")


def apply_workflows(
    workflows: dict[str, list[str]],
    part_dict: dict[str, int],
    starting_workflow_name: str = "in",
) -> bool:
    """
    Given as input the workflows to apply (see read_workflows for format), the
    part description (as part_dict, see return value of read_part); this function
    applies the workflows starting from given starting_workflow_name (default 'in').
    Returns True if part is accepted, False is part is rejected.

    A part is accepted (rejected) if the workflow to follow at any point has name
    'A' ('R').
    """
    workflow_name = starting_workflow_name
    while workflow_name not in ["A", "R"]:
        workflow_name = apply_workflow(workflows[workflow_name], part_dict)
    return workflow_name == "A"


def sum_part(part_dict: dict[str, int]) -> int:
    """
    Sums up the attribute values of given part.
    """
    return sum(part_dict.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 16")
    parser.add_argument("input_file", help="Input file", type=Path)
    args = parser.parse_args()

    user_workflows, user_parts = read_file(args.input_file)
    user_parts_sum = sum(
        sum_part(user_part)
        for user_part in user_parts
        if apply_workflows(user_workflows, user_part)
    )
    print(f"Sum of all ratings of all accepted parts is: {user_parts_sum}")
