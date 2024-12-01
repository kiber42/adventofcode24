#!/bin/env python3
day = 1
expected = (11, 31)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

def get_columns(filename):
    numbers = [int(n) for n in open(filename).read().split()]
    left = [numbers[i] for i in range(0, len(numbers), 2)]
    right = [numbers[i] for i in range(1, len(numbers), 2)]
    return left, right


def total_distance(left, right):
    left = sorted(left)
    right = sorted(right)
    return sum(abs(a - b) for a, b in zip(left, right))


def similarity_score(left, right):
    counts = {}
    for r in right:
        counts[r] = counts.get(r, 0) + 1
    return sum(l * counts.get(l, 0) for l in left)


def get_answers(filename):
    left, right = get_columns(filename)
    return total_distance(left, right), similarity_score(left, right)


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
