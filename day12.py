#!/bin/env python3
# ------------------------------------------

day = 12
expected = (1930, 1206)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import numpy as np
from scipy.ndimage import label

def get_data(filename):
    return np.array([[ord(c) for c in row] for row in open(filename).read().splitlines()])


def find_patches(data):
    # First, find the areas with the same type of crop
    groups = [data == index for index in np.unique(data)]
    # Each area might be disjoint and contain multiple patches
    patches = []
    for group in groups:
        labelled, num_labels = label(group)
        patches.extend(labelled == index for index in range(1, num_labels + 1))
    return patches


def fence_price(patch):
    area = sum(patch.reshape(-1))
    patch = np.pad(patch, pad_width=1, mode="constant", constant_values = False)
    perimeter = 0
    coords = np.where(patch)
    for y, x in zip(coords[0], coords[1]):
        assert(patch[y][x])
        if not patch[y - 1][x]: perimeter += 1
        if not patch[y + 1][x]: perimeter += 1
        if not patch[y][x - 1]: perimeter += 1
        if not patch[y][x + 1]: perimeter += 1
    return area * perimeter


def discounted_fence_price(patch):
    area = sum(patch.reshape(-1))
    patch = np.pad(patch, pad_width=1, mode="constant", constant_values = False)
    corners = 0 # There are as many corners as sides in a closed contour
    coords = np.where(patch)
    for y, x in zip(coords[0], coords[1]):
        # There are 8 types of corners, 4 convex and 4 concave
        if not patch[y - 1][x]:
            if not patch[y][x - 1]: corners += 1 # convex top left
            if not patch[y][x + 1]: corners += 1 # convex top right
        else:
            if patch[y][x - 1] and not patch[y - 1][x - 1]: corners += 1 # concave top left
            if patch[y][x + 1] and not patch[y - 1][x + 1]: corners += 1 # concave top right
        if not patch[y + 1][x]:
            if not patch[y][x - 1]: corners += 1 # convex bottom left
            if not patch[y][x + 1]: corners += 1 # convex bottom right
        else:
            if patch[y][x - 1] and not patch[y + 1][x - 1]: corners += 1 # concave bottom left
            if patch[y][x + 1] and not patch[y + 1][x + 1]: corners += 1 # concave bottom right
    return area * corners


def get_answers(filename):
    patches = find_patches(get_data(filename))
    return sum(fence_price(patch) for patch in patches), \
           sum(discounted_fence_price(patch) for patch in patches)


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
