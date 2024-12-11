#!/bin/env python3
# ------------------------------------------

day = 11
expected = (55312, None)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

from collections import defaultdict

def get_data(filename):
    return [int(x) for x in open(filename).read().split()]


def process_n(stones, n):
    updated = defaultdict(int)
    for stone in stones:
        updated[stone] += 1
    for _ in range(n):
        current, updated = updated.items(), defaultdict(int)
        for stone, amount in current:
            if stone == 0:
                updated[1] += amount
            else:
                s = str(stone)
                n = len(s)
                if n % 2 == 0:
                    updated[int(s[:n//2])] += amount
                    updated[int(s[n//2:])] += amount
                else:
                    updated[stone * 2024] += amount
    return sum(updated.values())


def get_answers(filename):
    stones = get_data(filename)    
    return process_n(stones, 25), process_n(stones, 75)


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
