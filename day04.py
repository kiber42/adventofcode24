#!/bin/env python3
# ------------------------------------------

day = 4
expected = (18, 9)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import numpy as np

def get_grid(filename):
    data = open(filename).read().splitlines()
    grid = np.array([[ch for ch in line] for line in data])
    return grid


def count_occurrence(grid, phrase="XMAS"):
    g = lambda x, y: grid[y][x] if y >= 0 and x >= 0 and y < grid.shape[0] and x < grid.shape[1] else 0
    dirs = np.array([[-1, -1], [ 0, -1], [+1, -1],
                     [-1,  0],           [+1,  0],
                     [-1, +1], [ 0, +1], [+1, +1]])

    num_matches = 0
    start_it = np.nditer(grid, flags=["multi_index"])
    for start in start_it:
        if start != phrase[0]:
            continue
        sy, sx = start_it.multi_index
        for dx, dy in dirs:
            if all(g(sx + dx * i, sy + dy * i) == phrase[i] for i in range(1, len(phrase))):
                num_matches += 1
    return num_matches


def count_x_mas(grid):
    num_matches = 0
    for sy in range(1, grid.shape[0] - 1):
        for sx in range(1, grid.shape[1] - 1):
            if grid[sy][sx] != "A":
                continue
            a, b = grid[sy - 1][sx - 1], grid[sy + 1][sx + 1]
            if not ((a == "M" and b == "S") or (a == "S" and b == "M")):
                continue
            a, b = grid[sy + 1][sx - 1], grid[sy - 1][sx + 1]
            if not ((a == "M" and b == "S") or (a == "S" and b == "M")):
                continue
            num_matches += 1
    return num_matches


def get_answers(filename):
    grid = get_grid(filename)
    return count_occurrence(grid), count_x_mas(grid)


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
