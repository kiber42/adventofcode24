#!/bin/env python3
# ------------------------------------------

day = 24
expected = (2024, None)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

def get_data(filename):
    blocks = open(filename).read().strip().split("\n\n")
    initial = {}
    for line in blocks[0]:
        gate, value = line.split(": ")
        initial[gate] = int(value)
    wirings = blocks[1]
    # ...
    return initial, wirings


def part_one(data):
    print(data)
    return None


def part_two(data):
    return None


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
