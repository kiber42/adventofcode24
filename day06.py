#!/bin/env python3
# ------------------------------------------

day = 6
expected = (41, 6)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

def get_obstacles_and_starting_pos(filename):
    rows = open(filename).read().strip().split("\n")
    obstacles = [[c == "#" for c in row] for row in rows]
    start = next((x, y) for y, row in enumerate(rows) for x, c in enumerate(row) if c =="^")
    return obstacles, start


def trace_path(obstacles, start):
    def is_inside(x, y, max_x=len(obstacles[0]), max_y=len(obstacles)):
        return x >=0 and x < max_x and y >= 0 and y < max_y
    visited = set()
    def has_visited(x, y, dir):
        n = len(visited)
        visited.add((x, y, dir))
        return len(visited) == n
    x, y = start
    dir = 0
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    while True:
        if has_visited(x, y, dir):
            return None
        x_new, y_new = x + dirs[dir][0], y + dirs[dir][1]
        if not is_inside(x_new, y_new):
            break
        if obstacles[y_new][x_new]:
            dir = (dir + 1) % 4
        else:
            x, y = x_new, y_new
    return set((x, y) for x, y, _ in visited) # discard direction information


def count_valid_spots(obstacles, start, candidate_positions):
    num_valid = 0
    candidate_positions.remove(start)
    for pos in candidate_positions:
        x, y = pos
        obstacles[y][x] = True
        if trace_path(obstacles, start) is None:
            num_valid += 1
        obstacles[y][x] = False
    return num_valid


def get_answers(filename):
    obstacles, start = get_obstacles_and_starting_pos(filename)
    path = trace_path(obstacles, start)
    return len(path), count_valid_spots(obstacles, start, path)


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
