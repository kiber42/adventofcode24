#!/bin/env python3
# ------------------------------------------

day = 24
expected = (2024, None)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

from collections import defaultdict

def get_data(filename):
    data = [block.splitlines() for block in open(filename).read().split("\n\n")]
    initial = {name:int(value) for name, value in [line.split(": ") for line in data[0]]}
    wiring = {out:(a, b, op) for a, op, b, _, out in [line.split(" ") for line in data[1]]}
    return initial, wiring


def compute(zbit, state, gates):
    if zbit in state:
        return state[zbit]
    a, b, op = gates[zbit]
    state[zbit] = -1
    a = compute(a, state, gates)
    b = compute(b, state, gates)
    if a == -1 or b == -1:
        raise RecursionError
    if op == "OR":
        result = a or b
    elif op == "AND":
        result = a and b
    else: # XOR
        result = a != b
    state[zbit] = result
    return result


def retrieve_zbits(state, gates):
    return [compute(wire, state, gates) for wire in sorted(gates.keys()) if wire.startswith("z")]


def part_one(initial, wiring):
    zbits = retrieve_zbits(initial, wiring)
    return sum(zbit << pos for pos, zbit in enumerate(zbits))


def part_two(wiring):
    if len(wiring) < 100:
        # Skip example
        return None

    N = max(int(name[1:]) for name in wiring.keys() if name.startswith("z"))

    # Add helper data structure: which gates are affected by each input
    affected = defaultdict(lambda: set())
    for out, (a, b, _) in wiring.items():
        affected[a].add(out)
        affected[b].add(out)

    # A correctly wired ripple carry adder (see Wikipedia) is a sequence of
    # a single half-adder followed by any number of full-adders.
    # In our case, the carry bit of the final full-adder is also part of the output.
    # The following rules can be inferred for each type of gate:
    # XOR: always directly after a pair of input bits or directly before an output bit
    #      (i.e. never used in the computation of carry bits)
    # OR:  generate carry bits. Carry bits are used twice in the following full-adder,
    #      once with an XOR (for the sum) and once with an AND (for the next carry bit).
    # AND: Serve as inputs for the carry bit computation (full-adder: AND,AND -> OR -> carry,
    #      half-adder: x00 AND y00 -> carry)

    # Find all gates that violate these rules:
    incorrect = []
    expected_affected_ops = {"AND": ["OR"], "XOR": ["AND", "XOR"], "OR": ["AND", "XOR"]}
    for out, (a, b, op) in wiring.items():
        # Checks for output bits
        if out.startswith("z"):
            if int(out[1:]) < N:
                if op != "XOR":
                    incorrect.append(out)
            elif op != "OR":
                incorrect.append(out)
            continue

        # Checks for input bits
        a, b = sorted([a, b])
        if (a[0], b[0]) == ("x", "y"):
            # Special case: half-adder for first bit
            if op == "AND" and (a, b) == ("x00", "y00"):
                continue
            # Inputs are never OR-ed
            if op == "OR":
                incorrect.append(out)
        elif op == "XOR":
            # XOR must be applied on inputs directly
            # (or must output to a "z-wire", checked above)
            incorrect.append(out)
            continue

        # Check the type of the operations that will be performed on the current output
        affected_ops = sorted(wiring[x][2] for x in affected[out])
        if affected_ops != expected_affected_ops[op]:
            incorrect.append(out)

    # We don't even have to find out the pairings between the incorrect wires :)
    return ",".join(sorted(incorrect))


def get_answers(filename):
    initial, wiring = get_data(filename)
    return part_one(initial, wiring), part_two(wiring)


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
