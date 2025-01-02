#!/bin/env python3
# ------------------------------------------

day = 6
expected = (41, 6)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import bisect

def get_obstacles_and_starting_pos(filename):
    rows = open(filename).read().strip().splitlines()
    obstacles = [[c == "#" for c in row] for row in rows]
    start = next((x, y) for y, row in enumerate(rows) for x, c in enumerate(row) if c == "^")
    return obstacles, start


# Follow the guard's regular path (which is known to leave the map eventually)
def follow_normal_path(obstacles, start):
    (x, y), dir = start, 0
    visited = set([start])
    while True:
        # directions: 0: up, 1: right, 2: down, 3: left
        x_new = x + (1 if dir == 1 else -1 if dir == 3 else 0)
        y_new = y + (1 if dir == 2 else -1 if dir == 0 else 0)
        if x_new >= 0 and y_new >= 0 and y_new < len(obstacles) and x_new < len(obstacles[0]):
            is_obstacle = obstacles[y_new][x_new]
        else:
            break
        if is_obstacle:
            dir = (dir + 1) % 4
        else:
            x, y = x_new, y_new
            visited.add((x, y))
    return visited


def check_loop(obstacles_per_row, obstacles_per_col, start):
    visited = set()
    def has_visited(x, y, dir):
        n = len(visited)
        visited.add((x, y, dir))
        return len(visited) == n

    def approach_next_obstacle(obstacles_in_line, current_coord, delta):
        obstacle_index = bisect.bisect(obstacles_in_line, current_coord) + (0 if delta > 0 else -1)
        if obstacle_index < 0 or obstacle_index > len(obstacles_in_line):
            raise IndexError
        obstacle_coord = obstacles_in_line[obstacle_index]
        return obstacle_coord - delta

    (x, y), dir = start, 0
    while not has_visited(x, y, dir):
        try:
            if dir == 0:   y = approach_next_obstacle(obstacles_per_col[x], y, -1)
            elif dir == 1: x = approach_next_obstacle(obstacles_per_row[y], x, +1)
            elif dir == 2: y = approach_next_obstacle(obstacles_per_col[x], y, +1)
            else:          x = approach_next_obstacle(obstacles_per_row[y], x, -1)
            dir = (dir + 1) % 4
        except IndexError:
            # No obstacle found -> guard will leave the map -> no loop
            return False
    # Loop detected
    return True


def count_valid_spots(grid, start, candidate_positions):
    max_x, max_y = len(grid[0]), len(grid)
    obstacles_per_row = [[x for x in range(max_x) if grid[y][x]] for y in range(max_y)]
    obstacles_per_col = [[y for y in range(max_y) if grid[y][x]] for x in range(max_x)]
    num_valid = 0
    candidate_positions.remove(start)
    for pos in candidate_positions:
        x, y = pos
        bisect.insort(obstacles_per_row[y] ,x)
        bisect.insort(obstacles_per_col[x], y)
        if check_loop(obstacles_per_row, obstacles_per_col, start):
            num_valid += 1
        obstacles_per_row[y].remove(x)
        obstacles_per_col[x].remove(y)
    return num_valid


def get_answers(filename):
    obstacles, start = get_obstacles_and_starting_pos(filename)
    normal_path = follow_normal_path(obstacles, start)
    return len(normal_path), count_valid_spots(obstacles, start, normal_path)


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
