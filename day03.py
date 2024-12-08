#!/bin/env python3
# ------------------------------------------

day = 3
expected = (161, 48)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import re

def get_data(filename):
    return open(filename).read()


def get_mul_result(data):
    pattern = re.compile("mul\\((\\d+),(\\d+)\\)")
    factors = [match.group(1, 2) for match in pattern.finditer(data)]
    return sum(int(a) * int(b) for a, b in factors)


def get_mul_result_do_or_dont(data):
    pattern = re.compile("(?:mul\\((\\d+),(\\d+)\\)|do\\(\\)|don't\\(\\))")
    enabled = True
    result = 0
    for match in pattern.finditer(data):        
        if match.group(1) is not None:
            if enabled:
                result += int(match.group(1)) * int(match.group(2))
        else:
            enabled = match.group(0) == "do()"
    return result


def get_answers(filename):
    data = get_data(filename)
    return get_mul_result(data), get_mul_result_do_or_dont(data)


if __name__ == "__main__":
    verify = get_answers(examplefile)
    if verify[0] != expected[0]:
        print("Part 1: expected", expected[0], "but computed", verify[0])
    else:
        result = get_answers(inputfile)
        print("Part 1:", result[0])
        if expected[1] != None:
            if verify[1] != expected[1]:
                print("Part 2: expected", expected[1], "but computed", verify[1])
            else:
                print("Part 2:", result[1])#!/bin/env python3
