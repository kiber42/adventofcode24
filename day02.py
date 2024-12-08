#!/bin/env python3
# ------------------------------------------

day = 2
expected = (2, 4)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import itertools

def get_reports(filename):
    return [[int(n) for n in line.split()] for line in open(filename).readlines()]


def num_safe_reports(reports):
    def safe(report):
        diffs = [y - x for x, y in itertools.pairwise(report)]
        min_diff, max_diff = min(diffs), max(diffs)
        return (min_diff >= 1 and max_diff <= 3) or (min_diff >= -3 and max_diff <= -1)
    return sum(1 if safe(report) else 0 for report in reports)


def num_safe_reports_dampener(reports):
    def safe(report):
        diffs = [y - x for x, y in itertools.pairwise(report)]
        min_diff, max_diff = min(diffs), max(diffs)
        return (min_diff >= 1 and max_diff <= 3) or (min_diff >= -3 and max_diff <= -1)
    def safe_with_dampener(report):
        if safe(report):
            return True
        # This extra loop is probably not necessary, but the inputs are not very long
        for skip_index in range(len(report)):
            short = [r for i, r in enumerate(report) if i != skip_index]
            if safe(short):
                return True
        return False
    return sum(1 if safe_with_dampener(report) else 0 for report in reports)


def get_answers(filename):
    reports = get_reports(filename)
    return num_safe_reports(reports), num_safe_reports_dampener(reports)


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
