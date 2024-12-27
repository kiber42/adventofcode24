#!/bin/env python3
# ------------------------------------------

day = 22
expected = (37327623, 24)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

from collections import defaultdict

def get_data(filename):
    return [int(secret) for secret in open(filename).read().splitlines()]


def evolve(secret, n = 1):
    for _ in range(n):
        secret = (secret ^ (secret << 6)) % 0x1000000
        secret ^= secret >> 5
        secret ^= secret << 11
    return secret % 0x1000000


def part_one(secrets):
    return sum(evolve(secret, 2000) for secret in secrets)


def part_two(secrets):
    bananas = defaultdict(lambda: 0)
    for secret in secrets:
        seen = set()
        def is_new_combination(combo):
            n = len(seen)
            seen.add(combo)
            return len(seen) > n
        deltas = []
        for _ in range(2000):
            prev, secret = secret, evolve(secret)
            deltas.append((secret % 10) - (prev % 10))
            if len(deltas) < 4:
                continue
            combo = tuple(deltas)
            if is_new_combination(combo):
                bananas[combo] += secret % 10
            deltas = deltas[1:]
    return max(bananas.values())


def get_answers(filename):
    secrets = get_data(filename)    
    return part_one(secrets), part_two(secrets)


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
