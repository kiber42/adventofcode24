#!/bin/env python3
# ------------------------------------------

day = 19
expected = (6, 16)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

def get_data(filename):
    towels, layouts = open(filename).read().strip().split("\n\n")
    return towels.split(", "), layouts.splitlines()


def get_answers(filename):
    towels, layouts = get_data(filename)
    cache = {"":1}
    def num_options(layout):
        try:
            return cache[layout]
        except KeyError:
            pass
        options = sum(num_options(layout[len(towel):]) for towel in towels if layout.startswith(towel))
        cache[layout] = options
        return options
    return (sum(1 for layout in layouts if num_options(layout) > 0),
            sum(num_options(layout) for layout in layouts))


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
