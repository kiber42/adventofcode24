#!/bin/env python3
# ------------------------------------------

day = 7
expected = (3749, 11387)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

def get_data(filename):
    data = []
    for line in open(filename).readlines():
        result, values = line.split(": ")
        data.append((int(result), [int(v) for v in values.split()]))
    return data


def try_satisfy(operands, test_value, operations):
    if len(operands) == 1 and operands[0] == test_value:
        return True
    if len(operands) < 2:
        return False
    if operands[0] > test_value:
        # all of the operations can only increase the value
        return False
    return any(try_satisfy([op(operands[0], operands[1])] + operands[2:], test_value, operations) for op in operations)


def total_calibration_result(data):
    operations = [lambda a, b: a + b, lambda a, b: a * b]
    return sum(value for value, operands in data if try_satisfy(operands, value, operations))


def total_calibration_result_3ops(data):
    operations = [lambda a, b: a + b, lambda a, b: a * b, lambda a, b: int(str(a) + str(b))]
    return sum(value for value, operands in data if try_satisfy(operands, value, operations))


def get_answers(filename):
    data = get_data(filename)    
    return total_calibration_result(data), total_calibration_result_3ops(data)


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
