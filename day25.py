#!/bin/env python3
# ------------------------------------------

day = 25
expected = (3, None)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

def get_data(filename):
    blocks = open(filename).read().strip().split("\n\n")
    locks = [get_heights(block) for block in blocks if block.startswith("#")]
    keys = [get_heights(block) for block in blocks if block.startswith(".")]
    return locks, keys


def get_heights(block):
    lines = block.splitlines()
    heights = [0] * len(lines[0])
    for line in lines:
        heights = [heights[i] + (1 if c == "#" else 0) for i, c in enumerate(line)]
    return heights


def fits(key, lock):
    return all(key[i] + lock[i] < 8 for i in range(len(key)))


def get_answers(filename):
    locks, keys = get_data(filename)
    return sum(1 if fits(key, lock) else 0 for key in keys for lock in locks), None


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
