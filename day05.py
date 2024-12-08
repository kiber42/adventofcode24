#!/bin/env python3
# ------------------------------------------

day = 5
expected = (143, 123)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import itertools

def get_updates_and_rules(filename):
    rules, updates = [block.strip().split("\n") for block in open(filename).read().split("\n\n")]
    updates = [[int(id) for id in update.split(",")] for update in updates]
    rules = set(tuple(int(id) for id in rule.split("|")) for rule in rules)
    return updates, rules


def is_correctly_ordered(update, rules):
    return not any((b,a) in rules for a, b in itertools.pairwise(update))


def fixup(update, rules):
    good = 0
    while good < len(update) - 1:
        if (update[good + 1], update[good]) in rules:
            # Swap entries that are in the wrong order
            update[good + 1], update[good] = update[good], update[good + 1]
            # This may invalidate the previous entry
            good = max(good - 1, 0)
        else:
            good += 1

def get_answers(filename):
    updates, rules = get_updates_and_rules(filename)
    correct_checksum = 0
    incorrect_checksum = 0
    for update in updates:
        if is_correctly_ordered(update, rules):
            correct_checksum += update[len(update)//2]
        else:
            fixup(update, rules)
            incorrect_checksum += update[len(update)//2]
    return correct_checksum, incorrect_checksum


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
