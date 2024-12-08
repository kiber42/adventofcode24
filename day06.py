#!/bin/env python3
# ------------------------------------------

day = 6
expected = (41, 6)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

def get_obstacles_and_size_and_starting_pos(filename):
    rows = open(filename).read().strip().split("\n")
    obstacles = set()
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c == "#":
                obstacles.add((x, y))
            elif c == "^":
                start = (x, y)
    return obstacles, (len(rows[0]), len(rows)), start


# Directions: 0 up, 1 right, 2 down, 3 left
def advance(pos, dir):
    if dir == 0:
        return (pos[0], pos[1] - 1)
    if dir == 1:
        return (pos[0] + 1, pos[1])
    if dir == 2:
        return (pos[0], pos[1] + 1)
    if dir == 3:
        return (pos[0] - 1, pos[1])


def is_inside(pos, area_size):
    return pos[0] >=0 and pos[0] < area_size[0] \
        and pos[1] >= 0 and pos[1] < area_size[1]


def try_add(set_, item):
    n = len(set_)
    set_.add(item)
    return len(set_) > n


def trace_path(obstacles, area_size, start, dir=0):
    pos = start
    visited = set()
    visited_with_dir = set()
    while is_inside(pos, area_size):
        visited.add(pos)
        found_loop = not try_add(visited_with_dir, (pos, dir))
        if found_loop:
            return None
        pos_new = advance(pos, dir)
        if pos_new in obstacles:
            dir = (dir + 1) % 4
        else:
            pos = pos_new
    return visited


def count_valid_spots(obstacles, area_size, start, normal_path):
    num_valid = 0
    normal_path = trace_path(obstacles, area_size, start)
    for pos in normal_path:
        if pos == start:
            continue
        obstacles.add(pos)
        if trace_path(obstacles, area_size, start) is None:
            num_valid += 1
        obstacles.remove(pos)
    return num_valid


def get_answers(filename):
    obstacles, area_size, start = get_obstacles_and_size_and_starting_pos(filename)
    normal_path = trace_path(obstacles, area_size, start)
    return len(normal_path), count_valid_spots(obstacles, area_size, start, normal_path)


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
