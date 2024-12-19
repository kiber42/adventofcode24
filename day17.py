#!/bin/env python3
# ------------------------------------------

day = 17
expected = ("4,6,3,5,6,3,5,2,1,0", None)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import random

def get_data(filename):
    blocks = open(filename).read().strip().split("\n\n")
    registers = [int(x.split(": ")[-1]) for x in blocks[0].splitlines()]
    program = [int(x) for x in blocks[1].split(": ")[-1].split(",")]
    return registers, program


def run(registers, program):
    def combo(opcode):
        if opcode < 4: return opcode
        if opcode < 7: return registers[opcode - 4]
    instruction = 0
    output = []
    while instruction < len(program):
        opcode = program[instruction]
        operand = program[instruction + 1]
        if opcode == 0: # adv
            registers[0] >>= combo(operand)
        elif opcode == 1: # bxl
            registers[1] ^= operand
        elif opcode == 2: # bst
            registers[1] = combo(operand) % 8
        elif opcode == 3: # jnz
            if registers[0] != 0:
                instruction = operand
                continue
        elif opcode == 4: # bxc
            registers[1] ^= registers[2]
        elif opcode == 5: # out
            value = combo(operand) % 8
            output.append(combo(operand) % 8)
        elif opcode == 6: # bdv
            registers[1] = registers[0] >> combo(operand)
        elif opcode == 7: # cdv
            registers[2] = registers[0] >> combo(operand)
        else:
            raise RuntimeError("Invalid opcode", opcode)
        instruction += 2
    return output


def get_output(registers, program):
    return ",".join(str(o) for o in run(registers, program))


# The program in my case can be summarized as follows:
# while register A > 0, compute and print register B using:
# bst A   B = A % 8
# bxl 5   B = B ^ 5
# cdv B   C = A >> B
# adv 3   A = A >> 3
# bxc -   B = B ^ C
# bxl 6   B = B ^ 6
# This can be simplified to:
# B = (A ^ 3 ^ (A >> ((A & 0b111) ^ 5))) & 0b111
# A >>= 3
def simplified(A):
    output = []
    while A > 0:
        output.append((A ^ 3 ^ (A >> ((A % 8) ^ 5))) % 8)
        A >>= 3
    return output


def quine_reverse_engineered(program):
    # This doesn't work on the example input
    if len(program) < 10:
        return

    # We need to look at the simplified version of the program to solve this
    # in a reasonable amount of time.

    # Each printed digit depends on the final 3 bits of A at the time, and some
    # other bits; the position of those also depends on the final 3 bits of A.
    # B = (A ^ 3 ^ (A >> ((A & 0b111) ^ 5))) & 0b111
    #      -----   ^     -----------------
    #        ^     |            ^
    #        |     |            |
    #        |     |            \--- shift amount  
    #        |     |
    #        |     \--- "shifted term"
    #        \--- 3 least significant bits (at that time)

    # We build up A starting from the most significant bits, i.e. the final part
    # of the program. This part produces the last output character, so we need
    # to work through the desired output in reverse order.
    # For each group of 3 bits, there might be multiple consistent choices that
    # produce the next desired output character. Since we want to find the
    # smallest permissible value for A, we pick the first choice that works out,
    # but this might cause issues later on, so we need to try this recursively.
    def recurse(A, program_index):
        if program_index < 0:
            return A
        A <<= 3
        for next_3_bits in range(8):
            A_candidate = A + next_3_bits
            shift_amount = next_3_bits ^ 5
            required_shifted_term = next_3_bits ^ 3 ^ program[program_index]
            # Check whether the computed shift term is consistent with the bits
            # we've determined so far.
            if (A_candidate >> shift_amount) % 8 == required_shifted_term:
                # Looks promising, recurse further
                result = recurse(A_candidate, program_index - 1)
                if result >= 0:
                    return result
        # No possible solution from given starting point
        return -1

    solution = recurse(0, len(program) - 1)
    print(solution, "produces output", simplified(solution))
    return solution


def get_answers(filename):
    registers, program = get_data(filename)
    return get_output(registers, program), quine_reverse_engineered(program)


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
