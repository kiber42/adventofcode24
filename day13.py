#!/bin/env python3
# ------------------------------------------

day = 13
expected = (480, None)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import numpy as np
from scipy.linalg import solve
import re

def get_data(filename):
    machines = open(filename).read().split("\n\n")
    pattern = re.compile("Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)")    
    return [[int(g) for g in pattern.match(machine).groups()] for machine in machines]


def solve_machine(m, offset = 0):
    a = np.array([[m[0], m[2]],[m[1], m[3]]])
    b = np.array([m[4], m[5]]) + offset
    x = np.array([int(v + 0.5) for v in solve(a, b)])
    return int(3 * x[0] + 1 * x[1]) if np.all(np.dot(a, x) == b) else 0


def part_one(machines):
    return sum(solve_machine(m) for m in machines)


def part_two(machines):
    return sum(solve_machine(m, 10000000000000) for m in machines)


def get_answers(filename):
    data = get_data(filename)    
    return part_one(data), part_two(data)


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
