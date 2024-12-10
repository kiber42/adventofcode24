#!/bin/env python3
# ------------------------------------------

day = 9
expected = (1928, 2858)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

def get_diskmap(filename):
    return [int(x) for x in open(filename).read().strip()]


def unpack_layout(diskmap):
    blocks = []
    id = 0
    is_free = False
    for size in diskmap:
        if is_free:
            blocks.extend([-1] * size)
            is_free = False
        else:
            blocks.extend([id] * size)
            is_free = True
            id += 1
    return blocks


def defrag(blocks):
    first_free = -1
    last_data = len(blocks)
    while True:
        first_free = next(i for i in range(first_free + 1, len(blocks)) if blocks[i] == -1)
        last_data = next(i for i in range(last_data - 1, 0, -1) if blocks[i] >= 0)
        if first_free > last_data:
            break
        blocks[first_free] = blocks[last_data]
        blocks[last_data] = -1


def defrag_improved(diskmap):
    files = []
    spaces = []
    pos = 0
    for i, size in enumerate(diskmap):
        if i % 2 == 0:
            files.append((i // 2, pos, size))
        else:
            spaces.append((pos, size))
        pos += size
    blocks = [-1] * pos 

    files.reverse()
    for fid, fpos, fsize in files:
        target = next(((index, (pos, size)) for index, (pos, size) in enumerate(spaces) if pos < fpos and size >= fsize), None)
        if target is None:
            for i in range(fsize):
                blocks[i + fpos] = fid
            continue
        tindex, (tpos, tsize) = target
        spaces[tindex] = (tpos + fsize, tsize - fsize)
        # unpack for checksum computation
        for i in range(fsize):
            blocks[i + tpos] = fid            
    return blocks


def compute_checksum(blocks):
    checksum = 0
    for pos, id in enumerate(blocks):
        if id > 0:
            checksum += id * pos
    return checksum


def part_one(diskmap):
    blocks = unpack_layout(diskmap)
    defrag(blocks)
    return compute_checksum(blocks)


def part_two(diskmap):
    blocks = defrag_improved(diskmap)
    return compute_checksum(blocks)


def get_answers(filename):
    diskmap = get_diskmap(filename)    
    return part_one(diskmap), part_two(diskmap)


if __name__ == "__main__":
    verify = get_answers(examplefile)
    #print(verify)
    #exit()
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
