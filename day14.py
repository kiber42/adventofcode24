#!/bin/env python3
# ------------------------------------------

day = 14
expected = (12, None)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

from collections import Counter
import re

def get_robots(filename):
    robots = open(filename).read().splitlines()
    pattern = re.compile("p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    return [tuple(int(g) for g in pattern.match(robot).groups()) for robot in robots]


def advance(robot, seconds, xmax, ymax):
    x, y, vx, vy = robot
    x = ((x + seconds * vx) % xmax + xmax) % xmax
    y = ((y + seconds * vy) % ymax + ymax) % ymax
    return (x, y, vx, vy)


def quadrant(robot, xmax, ymax):
    dx = robot[0] - (xmax - 1) // 2
    dy = robot[1] - (ymax - 1) // 2
    if dx == 0 or dy == 0:
        return -1
    return (2 if dx < 0 else 0) + (1 if dy < 0 else 0)


def part_one(robots):
    xmax, ymax = (101, 103) if len(robots) > 100 else (11, 7)
    robots = [advance(robot, 100, xmax, ymax) for robot in robots]
    quadrants = Counter(quadrant(robot, xmax, ymax) for robot in robots)
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def draw(robots, xmax, ymax):
    robots = set((x, y) for x, y, _, _ in robots)
    for y in range(ymax):
        print("".join(["X" if (x, y) in robots else " " for x in range(xmax)]))


def part_two_drawing(robots):
    if len(robots) < 100:
        return None
    xmax, ymax = 101, 103
    # Robots assemble in clusters in regular intervals
    # Manually determined that a vertical cluster first appears after 39 seconds
    # and then repeats every 101 seconds. A horizontal cluster first appears
    # after 99 seconds and repeats every 103 seconds.
    # (The frequencies are just the sizes of the area, which makes sense...)
    # The first co-occurence of these clusters happens after 7412 seconds.
    num_seconds = 39
    robots = [advance(robot, num_seconds, xmax, ymax) for robot in robots]
    while True:
        step = 101
        robots = [advance(robot, step, xmax, ymax) for robot in robots]
        num_seconds += step
        draw(robots, xmax, ymax)
        print(num_seconds, "*" * 100)
        if input() != "":
            break
    return num_seconds


def part_two(robots):
    if len(robots) < 100:
        return None
    # Having seen the Easter Egg, I know that it is located in a single quadrant
    # Idea: Find a minimum in the safety factor computed in part one
    xmax, ymax = 101, 103
    min_safety = 1e10
    min_safety_index = 0
    for n in range(xmax * ymax):
        robots = [advance(robot, 1, xmax, ymax) for robot in robots]
        quadrants = Counter(quadrant(robot, xmax, ymax) for robot in robots)
        safety_factor = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
        if safety_factor < min_safety:
            min_safety = safety_factor
            min_safety_index = n + 1
    return min_safety_index


def get_answers(filename):
    robots = get_robots(filename)    
    return part_one(robots), part_two(robots)


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
