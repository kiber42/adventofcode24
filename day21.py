#!/bin/env python3
# ------------------------------------------

day = 21
expected = (126384, None)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

from itertools import pairwise

def get_data(filename):
    return open(filename).read().splitlines()


def complexity(code):
    keypositions = {
        "7": (0, 0), "8": (0, 1), "9": (0, 2),
        "4": (1, 0), "5": (1, 1), "6": (1, 2),
        "1": (2, 0), "2": (2, 1), "3": (2, 2),
                     "0": (3, 1), "A": (3, 2)}
    positions = [keypositions[key] for key in "A" + code]
    # Distances on numeric keypad
    steps0 = [(abs(y2 - y1), abs(x2 - x1)) for ((y1, x1), (y2, x2)) in pairwise(positions)]
    # Distances on first arrow keypad
    steps1 = []
    # Distances on second arrow keypad
    steps2 = []
    # Keys to be pressed directly
    sequence = []
    numeric = int(code[:-1])
    return numeric * len(sequence)


def part_one(data):
    return sum(complexity(keycode) for keycode in data)


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
