#!/bin/env python3
# ------------------------------------------

day = 10
expected = (36, 81)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------
import numpy as np

def get_profile(filename):
    return np.array([[int(x) for x in row] for row in open(filename).read().splitlines()])


# "grow" input by shifting it by 1 cell in 4 directions
def expand(mask):
    return mask + \
        np.roll(mask, shift=-1, axis=0) + np.roll(mask, shift=+1, axis=0) + \
        np.roll(mask, shift=-1, axis=1) + np.roll(mask, shift=+1, axis=1)


def analyze_trailheads(profile):
    starts = np.where(profile == 0)
    # add border around profile to prevent as otherwise
    # shifting the bitmasks can wrap elements around.
    profile = np.pad(profile, pad_width=1, mode="constant", constant_values = 0)
    starts = [(row + 1, col + 1) for row, col in zip(starts[0], starts[1])]
    score, rating = 0, 0
    for start in starts:
        reachable = np.zeros_like(profile, dtype=int)
        reachable[start] = 1
        height = 0
        while height < 9:
            height += 1
            reachable = expand(reachable) * (profile == height)
        score += np.count_nonzero(reachable)
        rating += sum(sum(reachable))
    return score, rating


def get_answers(filename):
    area_profile = get_profile(filename)
    return analyze_trailheads(area_profile)


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
