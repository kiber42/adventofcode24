#!/bin/env python3
# ------------------------------------------

day = 23
expected = (7, "co,de,ka,ta")

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

from bisect import bisect
from collections import defaultdict

def get_data(filename):
    return [tuple(sorted(line.split("-"))) for line in open(filename).read().splitlines()]


def get_triplets(pairs):
    direct = defaultdict(lambda: set())
    for a, b in pairs:
        direct[a].add(b)
        direct[b].add(a)
    return [(a, b, c) for a, b in pairs for c in direct[a].intersection(direct[b]) if c > b]


def find_party(direct, doublets):
    # Don't go for a completely generic solution.
    # The nodes in the full input each have 13 direct neighbours.
    # If there was a disjoint cluster of 14 nodes, that would be too easy.
    # It is relatively easy to find fully connected groups of size 12.
    # So the target group must have size 13.

    # As an intermediate step, we build quadruplets, and then look for
    # 3 matching quadruplets and one extra connected node. We only keep
    # quadruplets that have sufficiently many connected nodes in common.

    # Work with sorted doublets (a < b) and only build sorted quadruplets,
    # to avoid creating redundant entries.
    doublets = [(min(a, b), max(a, b)) for a, b in doublets]
    doublets.sort()

    quadruplets = []
    for i in range(len(doublets)):
        a, b = doublets[i]
        octet_neighbours = direct[a].intersection(direct[b])
        # Only want quadruplets with a < b < c < d  => find first c > b
        j_start = bisect(doublets, (b, 0), i + 1, len(doublets))
        for j in range(j_start, len(doublets)):
            c, d = doublets[j]
            if c in octet_neighbours and d in octet_neighbours:
                quadruplets.append((a, b, c, d))

    if len(quadruplets) == 1:
        # Presumably running on example input
        return quadruplets[0]

    # Precompute sets of common neighbour nodes for each quadruplet.
    # Need 9 common neighbours to possibly find a connected group of size 13.
    selected = []
    quad_neighbours = []
    for quadruplet in quadruplets:
        neighbours = direct[quadruplet[0]].copy()
        for node in quadruplet[1:]:
            neighbours.intersection_update(direct[node])
        if len(neighbours) >= 9:
            selected.append(quadruplet)
            quad_neighbours.append(neighbours)
    quadruplets = selected

    for i in range(len(quadruplets)):
        j_start = bisect(quadruplets, (quadruplets[i][3], 0), i + 1, len(quadruplets))
        for j in range(i + 1, len(quadruplets)):
            if not all(q in quad_neighbours[i] for q in quadruplets[j]):
                continue
            octet_neighbours = quad_neighbours[i].intersection(quad_neighbours[j])
            if len(octet_neighbours) < 5:
                continue
            k_start = bisect(quadruplets, (quadruplets[j][3], 0), j + 1, len(quadruplets))
            for k in range(k_start, len(quadruplets)):
                if not all(q in octet_neighbours for q in quadruplets[k]):
                    continue
                more_neighbours = octet_neighbours.intersection(quad_neighbours[k])
                if len(more_neighbours) > 0:
                    party = quadruplets[i] + quadruplets[j] + quadruplets[k] + tuple(more_neighbours)
                    return party
    return []


def part_one(pairs):
    triplets = get_triplets(pairs)
    return sum(1 for triplet in triplets if any(t.startswith("t") for t in triplet))


def part_two_bron_kerbosch(pairs):
    neighbours = defaultdict(lambda: set())
    for a, b in pairs:
        neighbours[a].add(b)
        neighbours[b].add(a)

    def recurse(R, P, X):
        if len(P) == 0 and len(X) == 0:
            yield R
        while P:
            # Attempt to move vertex p from P to R.
            # Only neighbours of p remain in P and X, any other vertex will no
            # longer be considered for finding a clique.
            p = P.pop()
            yield from recurse(R | {p}, P & neighbours[p], X & neighbours[p])
            X.add(p)

    maximal_cliques = recurse(set(), set(neighbours.keys()), set())
    longest = max(maximal_cliques, key=len)
    return ",".join(sorted(longest))


def part_two_bruteforce(pairs):
    # map names to integers, hopefully slightly more performant
    index = -1
    def get_index():
        nonlocal index
        index += 1
        return index
    indices = defaultdict(get_index)

    # Compile direct neighbourhood of each node, and convert
    # pairs of named nodes to pairs of corresponding indices
    direct = defaultdict(lambda: set())
    doublets = []
    for a, b in pairs:
        doublets.append([index_a:=indices[a], index_b:=indices[b]])
        direct[index_a].add(index_b)
        direct[index_b].add(index_a)
    names = {v:k for k, v in indices.items()}

    party = find_party(direct, doublets)
    return ",".join(sorted(names[pc] for pc in party))


def get_answers(filename):
    pairs = get_data(filename)
    return part_one(pairs), part_two_bron_kerbosch(pairs)


if __name__ == "__main__":
    verify = get_answers(examplefile)
    if verify[0] != expected[0]:
        print("Part 1: expected", expected[0], "but computed", verify[0])
    elif expected[1] is not None and verify[1] != expected[1]:
        print("Part 2: expected", expected[1], "but computed", verify[1])
        result = get_answers(inputfile)
        print("Part 1:", result[0])
    else:
        result = get_answers(inputfile)
        print("Part 1:", result[0])
        print("Part 2:", result[1])
