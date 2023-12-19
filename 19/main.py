"""
Advent of Code 2023: Problem 16
"""

import argparse
from pathlib import Path
import re

PART_NAMES = ["x", "m", "a", "s"]
MIN_PART_VALUE = {part: 1 for part in PART_NAMES}
MAX_PART_VALUE = {part: 4000 for part in PART_NAMES}


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
    for rule in rules[:-1]:
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


def get_all_accept_paths(
    workflows: dict[str, list[str]]
) -> list[dict[str, list[str] | str]]:
    """
    Part 2
    """
    for name, rules in workflows.items():
        for ind, rule in enumerate(rules[:-1]):
            cond, w_name = rule.split(":")
            workflows[name][ind] = {"cond": [cond], "name": w_name}
        workflows[name][-1] = {"cond": [], "name": workflows[name][-1]}
        for ind, val in enumerate(workflows[name][1:]):
            val["cond"].extend(
                [f"!{c}" if c[0] != "!" else c for c in workflows[name][ind]["cond"]]
            )

    current_workflow = workflows["in"]
    flag_not_all_ar = True
    while flag_not_all_ar:
        flag_not_all_ar = False
        next_workflow = []
        for option in current_workflow:
            if not (option["name"] == "A" or option["name"] == "R"):
                flag_not_all_ar = True
                for val in workflows[option["name"]]:
                    val["cond"] = val["cond"].copy()
                    val["cond"].extend(option["cond"])
                    next_workflow.append(val)
            else:
                next_workflow.append(option)
        current_workflow = next_workflow

    return current_workflow


def num_per_accept_path(accept_path_cond: list[str]) -> int:
    """
    Part 2
    """
    part_values = {
        name: [
            [True, val] for val in range(MIN_PART_VALUE[name], MAX_PART_VALUE[name] + 1)
        ]
        for name in PART_NAMES
    }
    for cond in accept_path_cond:
        part_name, val = re.split(r"\<|\>", cond)
        val = int(val)
        if "<" in cond:
            if "!" in cond:
                part_values[part_name[1:]] = [
                    [b and not (pv < val), pv] for b, pv in part_values[part_name[1:]]
                ]
            else:
                part_values[part_name] = [
                    [b and (pv < val), pv] for b, pv in part_values[part_name]
                ]
        else:
            if "!" in cond:
                part_values[part_name[1:]] = [
                    [b and not (pv > val), pv] for b, pv in part_values[part_name[1:]]
                ]
            else:
                part_values[part_name] = [
                    [b and (pv > val), pv] for b, pv in part_values[part_name]
                ]

    num_accept_paths = 1
    for name in PART_NAMES:
        s = sum(b for b, _ in part_values[name])
        num_accept_paths *= s
    return num_accept_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC 2023 Problem 16")
    parser.add_argument("input_file", help="Input file", type=Path)
    parser.add_argument("--all-accept", action="store_true")
    args = parser.parse_args()

    user_workflows, user_parts = read_file(args.input_file)
    if not args.all_accept:
        user_parts_sum = sum(
            sum_part(user_part)
            for user_part in user_parts
            if apply_workflows(user_workflows, user_part)
        )
        print(f"Sum of all ratings of all accepted parts is: {user_parts_sum}")
    else:
        num_paths = sum(
            num_per_accept_path(accept_path["cond"])
            for accept_path in get_all_accept_paths(user_workflows)
            if accept_path["name"] == "A"
        )
        print(f"Total number of distinct acceptable combinations: {num_paths}")
