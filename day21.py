#!/bin/env python3
# ------------------------------------------

day = 21
expected = (126384, None)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

from collections import defaultdict
from itertools import pairwise

def get_data(filename):
    return open(filename).read().splitlines()


# There seem to be some heuristics out there to identify the best path, but none
# of the explanations are convincing in my opinion, so we just try all, pick the
# one that results in the shortest overall sequence, and memoize it.
def find_possible_inputs_for_path(from_pos, to_pos, avoid):
    if from_pos == avoid:
        return []
    x1, y1, x2, y2 = *from_pos, *to_pos
    dx, dy = x2 - x1, y2 - y1
    key_x, step_x = ("<", -1) if dx < 0 else (">", +1)
    key_y, step_y = ("^", -1) if dy < 0 else ("v", +1)
    if dy == 0:
        return [key_x * abs(dx) + "A"]
    if dx == 0:
        return [key_y * abs(dy) + "A"]
    return [key_x + next for next in find_possible_inputs_for_path((x1 + step_x, y1), to_pos, avoid)] + \
           [key_y + next for next in find_possible_inputs_for_path((x1, y1 + step_y), to_pos, avoid)]


cache = [defaultdict(lambda: -1) for _ in range(27)]
def find_cheapest_path_along(positions, avoid, num_input_robots):
    if num_input_robots == 0:
        num_keypresses = len(positions) - 1
        return num_keypresses
    cheapest_total = 0
    for path_segment in pairwise(positions):
        cheapest = cache[num_input_robots][path_segment]
        if cheapest == -1:
            paths = find_possible_inputs_for_path(*path_segment, avoid)
            cheapest = min(find_cheapest_path_arrows(desired_output, num_input_robots - 1) for desired_output in paths)
            cache[num_input_robots][path_segment] = cheapest
        cheapest_total += cheapest
    return cheapest_total


def find_cheapest_path_numpad(desired_output, num_robots):
    key_positions = {
        "7": (0, 0), "8": (1, 0), "9": (2, 0),
        "4": (0, 1), "5": (1, 1), "6": (2, 1),
        "1": (0, 2), "2": (1, 2), "3": (2, 2),
                     "0": (1, 3), "A": (2, 3)}
    output_positions = [key_positions[key] for key in "A" + desired_output]
    return find_cheapest_path_along(output_positions, (0, 3), num_robots)

def find_cheapest_path_arrows(desired_output, num_input_robots):
    key_positions = {"^": (1, 0), "A": (2, 0),
        "<": (0, 1), "v": (1, 1), ">": (2, 1)}
    output_positions = [key_positions[key] for key in "A" + desired_output]
    return find_cheapest_path_along(output_positions, (0, 0), num_input_robots)


def complexity(code, num_robots):
    cheapest_sequence = find_cheapest_path_numpad(code, num_robots)
    numeric = int(code[:-1])
    return cheapest_sequence * numeric


def part_one(codes):
    return sum(complexity(keycode, num_robots=3) for keycode in codes)


def part_two(codes):
    return sum(complexity(keycode, num_robots=26) for keycode in codes)


def get_answers(filename):
    codes = get_data(filename)
    return part_one(codes), part_two(codes)


if __name__ == "__main__":
    verify = get_answers(examplefile)
    if verify[0] != expected[0]:
        print("Part 1: expected", expected[0], "but computed", verify[0])
    else:
        result = get_answers(inputfile)
        print("Part 1:", result[0])
        if result[1] != None:
            if expected[1] != None and verify[1] != expected[1]:
                print("Part 2: expected", expected[1], "but computed", verify[1])
            else:
                print("Part 2:", result[1])
