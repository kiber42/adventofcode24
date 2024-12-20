#!/bin/env python3
# ------------------------------------------

day = 16
expected = (11048, 64)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

from collections import defaultdict
from heapq import heappop, heappush

def get_data(filename):
    grid = {(x, y):c for y, row in enumerate(open(filename).read().splitlines())
                     for x, c in enumerate(row) if c != "#"}
    start = next(pos for pos in grid if grid[pos] == "S")
    goal = next(pos for pos in grid if grid[pos] == "E")
    return grid, start, goal


def find_paths(grid, start, goal):
    offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    todo = [(0, start, 1, [start])] # score, pos, orientation, path
    scores = defaultdict(lambda: 1000000)
    best_to_goal = None
    spots_along_best_paths = set()
    # priority queue (evaluate lowest scores first)
    while todo:
        score, (x, y), orientation, path = heappop(todo)
        if score > scores[x, y, orientation]:
            continue
        else:
            scores[x, y, orientation] = score
        if (x, y) == goal:
            # because we're using a priority queue,
            # the first path we find that reaches the goal
            # is necessarily one with the lowest possible score
            if best_to_goal is None:
                best_to_goal = score
            if score == best_to_goal:
                spots_along_best_paths.update(path)
            continue
        for step_dir in range(4):
            dx, dy = offsets[step_dir]
            next_pos = (x + dx, y + dy)
            if next_pos in grid:
                next_score = score + (1 if orientation == step_dir else 1001)
                heappush(todo, (next_score, next_pos, step_dir, path + [next_pos]))
    return best_to_goal, spots_along_best_paths


def get_answers(filename):
    grid, start, goal = get_data(filename)
    best, spots = find_paths(grid, start, goal)
    return best, len(spots)


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
