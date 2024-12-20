#!/bin/env python3
# ------------------------------------------

day = 20
expected = (44, 285)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import numpy as np

WALL = 1000000
CHEAT_MAX = 20

def get_data(filename):
    raw = np.array([[c for c in row] for row in open(filename).read().splitlines()])
    raw = np.pad(raw, pad_width=CHEAT_MAX, constant_values="#")
    start = np.where(raw == "S")
    goal = np.where(raw == "E")
    maze = np.full(shape=raw.shape, dtype=int, fill_value=WALL)
    maze[raw != "#"] = -1
    return maze, (start[1][0], start[0][0]), (goal[1][0], goal[0][0])


def traverse_normal(maze, start, goal):
    p = start
    dist = 0
    maze[p[1], p[0]] = dist
    while p != goal:
        dist += 1
        neighbours = [(p[0] - 1, p[1]), (p[0] + 1, p[1]), (p[0], p[1] - 1), (p[0], p[1] + 1)]
        for n in neighbours:
            if maze[n[1], n[0]] == -1:
                maze[n[1], n[0]] = dist
                p = n
                break
        else:
            print("Did not reach goal")
            return None
    return maze


def find_num_cheats(maze, min_saved, max_cheat_duration):
    # Instead of checking all possible combinations of cheat start and end positions,
    # compute the entire matrix of time savings for each possible cheat *offset* in
    # one go. Some care needs to be taken not to double count combinations.
    cheats = 0
    for cheat_dist in range(2, max_cheat_duration + 1):
        for offset_x in range(cheat_dist + 1):
            offset_y = cheat_dist - offset_x
            saved = np.abs(np.roll(np.roll(maze, shift=offset_x, axis=1), shift=offset_y, axis=0) - maze) - cheat_dist
            cheats += sum((saved.flat >= min_saved) & (saved.flat < WALL / 2))
            if offset_x == 0 or offset_y == 0:
                continue
            saved = np.abs(np.roll(np.roll(maze, shift=-offset_x, axis=1), shift=offset_y, axis=0) - maze) - cheat_dist
            cheats += sum((saved.flat >= min_saved) & (saved.flat < WALL / 2))            
    return cheats


def part_one(maze):
    min_saved = 100 if len(maze) > 100 else 2
    return find_num_cheats(maze, min_saved, max_cheat_duration=2)


def part_two(maze):
    min_saved = 100 if len(maze) > 100 else 50
    return find_num_cheats(maze, min_saved, max_cheat_duration=20)


def get_answers(filename):
    maze, start, goal = get_data(filename)
    maze = traverse_normal(maze, start, goal)
    return part_one(maze), part_two(maze)


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
