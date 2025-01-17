#!/bin/env python3
# ------------------------------------------

day = 12
expected = (1930, 1206)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

from collections import defaultdict
import numpy as np

def get_data(filename):
    return np.array([[ord(c)-ord("A") for c in row] for row in open(filename).read().splitlines()], dtype=int)


def find_disconnected_patches(field):
    # Add a border to make our life easier
    field = np.pad(field, 1, mode="constant", constant_values=1000)    
    rows, cols = field.shape
    num_patches = 0

    def flood_fill(y0, x0, new_color):
        to_process = set([(y0, x0)])
        old_color = field[y0, x0]
        while len(to_process) > 0:
            y, x = to_process.pop()
            if field[y, x] == old_color:
                field[y, x] = new_color
                to_process.add((y - 1, x))
                to_process.add((y + 1, x))
                to_process.add((y, x - 1))
                to_process.add((y, x + 1))

    for y in range(rows):
        for x in range(cols):
            if field[y, x] < 1000:
                num_patches += 1
                flood_fill(y, x, 1000 + num_patches)

    return field


def calculate_prices(patches):
    area = defaultdict(lambda: 0)
    perimeter = defaultdict(lambda: 0)
    # count corners instead of sides (they are identical on a closed contour)
    corners = defaultdict(lambda: 0)

    # iterate over 3 x 3 submatrices to identify boundaries and corners
    rows, cols = patches.shape
    for y in range(rows - 2):
        for x in range(cols - 2):
            sub = patches[y:y + 3, x:x + 3]
            current = sub[1, 1]
            area[current] += 1
            same_above = current == sub[0, 1]
            same_below = current == sub[2, 1]
            same_on_left = current == sub[1, 0]
            same_on_right = current == sub[1, 2]
            if same_above:
                if same_on_left and current != sub[0, 0]: corners[current] += 1 # concave top left
                if same_on_right and current != sub[0, 2]: corners[current] += 1 # concave top right
            else:
                perimeter[current] += 1
                if not same_on_left: corners[current] += 1 # convex top left
                if not same_on_right: corners[current] += 1 # convex top right
            if same_below:
                if same_on_left and current != sub[2, 0]: corners[current] += 1 # concave bottom left
                if same_on_right and current != sub[2, 2]: corners[current] += 1 # concave bottom right
            else:
                perimeter[current] += 1
                if not same_on_left: corners[current] += 1 # convex bottom left
                if not same_on_right: corners[current] += 1 # convex bottom right
            if not same_on_left: perimeter[current] += 1
            if not same_on_right: perimeter[current] += 1
    price, discounted = 0, 0
    for crop in area.keys():
        price += area[crop] * perimeter[crop]
        discounted += area[crop] * corners[crop]
    return price, discounted


def get_answers(filename):
    patches = find_disconnected_patches(get_data(filename))
    return calculate_prices(patches)


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
