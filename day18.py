#!/bin/env python3
# ------------------------------------------

day = 18
expected = (22, "6,1")

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import numpy as np

def get_data(filename):
    return [tuple(int(n) for n in row.split(",")) for row in open(filename).read().strip().splitlines()]


def build_maze(data, size):
    maze = np.zeros((size, size))
    for x, y in data:
        maze[y, x] = 1
    return np.pad(maze, pad_width=1, constant_values=1)


def find_path(maze):
    # goal is in the bottom right corner (account for border)
    goal = (maze.shape[1] - 2, maze.shape[0] - 2)
    visited = set([(1, 1)])
    updated = set([(1, 1)])
    steps = 0
    while len(updated) > 0:
        previous = updated
        updated = set()
        steps += 1
        for x, y in previous:
            neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for pos in neighbours:
                if maze[pos[1], pos[0]] != 0 or pos in visited:
                    continue
                if pos == goal:
                    return steps
                visited.add(pos)
                updated.add(pos)
    return None


def part_one(data):
    # Part one only uses part of the input
    if len(data) > 1024:
        maze = build_maze(data[:1024], 71)
    else:
        maze = build_maze(data[:12], 7)
    
    return find_path(maze)


def part_two(data):
    n = 71 if len(data) > 1024 else 7

    max_num_blocks = len(data)
    min_num_blocks = 1024 if max_num_blocks > 1024 else 12
    # Bisect the possible interval of number of blocks
    # to find the exact block which disrupts the path.
    while min_num_blocks < max_num_blocks:
        num_blocks = (min_num_blocks + max_num_blocks) // 2
        maze = build_maze(data[:num_blocks], n)
        if find_path(maze):
            min_num_blocks = num_blocks + 1
        else:
            max_num_blocks = num_blocks
    block_index = min_num_blocks - 1
    x, y = data[block_index]
    return f"{x},{y}"


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
