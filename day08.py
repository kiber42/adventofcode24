#!/bin/env python3
# ------------------------------------------

day = 8
expected = (14, 34)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

from collections import defaultdict

def get_antenna_positions(filename):
    antennas = defaultdict(list)
    data = open(filename).read().splitlines()
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c != ".":
                antennas[c].append((int(x), int(y)))
    size = (len(data[0]), len(data))
    return antennas, size


def count_antinodes(antennas, size):
    antinodes = set()
    for positions in antennas.values():
        for p1 in positions:
            for p2 in positions:
                if p1 == p2:
                    continue
                antinodes.add((2 * p1[0] - p2[0], 2 * p1[1] - p2[1]))
    return sum(1 if x >=0 and x < size[0] and y >= 0 and y < size[1] else 0 for x, y in antinodes)


def count_antinodes_resonances(antennas, size):
    antinodes = set()
    for positions in antennas.values():
        for p1 in positions:
            for p2 in positions:
                if p1 == p2:
                    continue
                step = (p1[0] - p2[0], p1[1] - p2[1])
                if step[0] != 0:
                    start_index = -(p1[0] // step[0])
                    num_steps = size[0] // abs(step[0]) + 1
                else:
                    start_index = -(p1[1] // step[1])
                    num_steps = size[1] // abs(step[1]) + 1
                for i in range(start_index, start_index + num_steps):
                    antinodes.add((p1[0] + i * step[0], p1[1] + i * step[1]))
    return sum(1 if x >=0 and x < size[0] and y >= 0 and y < size[1] else 0 for x, y in antinodes)


def get_answers(filename):
    antennas, size = get_antenna_positions(filename)    
    return count_antinodes(antennas, size), count_antinodes_resonances(antennas, size)


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
                print("Part 2:", result[1])
