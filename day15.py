#!/bin/env python3
# ------------------------------------------

day = 15
expected = (10092, 9021)

examplefile = "example{:02}.txt".format(day)
inputfile = "input{:02}.txt".format(day)

# ------------------------------------------

import numpy as np

dirs = {"^": [-1, 0], ">": [ 0,+1], "v": [+1, 0], "<": [ 0,-1]}

def get_data(filename):
    blocks = open(filename).read().strip().split("\n\n")
    maze = np.array([[c for c in line] for line in blocks[0].splitlines()])
    moves = [m for m in blocks[1] if m in dirs]
    return maze, moves


class Maze:
    def __init__(self, maze, widen = True):
        pos = np.where(maze == '@')
        boxes = np.where(maze == 'O')
        walls = np.where(maze == '#')
        # For part 2: Widen the maze by multiplying the x coordinate.
        #             For boxes and walls, only store coordinate of left part.
        widening = 2 if widen else 1
        self.pos = (pos[0][0], widening * pos[1][0])
        self.boxes = list(zip(boxes[0], widening * boxes[1]))
        self.walls = set(zip(walls[0], widening * walls[1]))
        self.step = self.step_wide if widen else self.step_normal


    def run(self, moves):
        for move in moves:
            self.step(np.array(dirs[move]))
        return self.GPS_score()


    def step_normal(self, dir):        
        newpos = tuple(self.pos + dir)
        if newpos in self.walls:
            return
        try:
            box_index = self.boxes.index(newpos)
            pos_behind_boxes = next(tuple(self.pos + i * dir) for i in range(2, 100) if tuple(self.pos + i * dir) not in self.boxes)
            if not pos_behind_boxes in self.walls:
                # Don't move all boxes, just move the one in front to the back (hopefully no one notices!)
                self.boxes[box_index] = pos_behind_boxes
                self.pos = newpos
        except ValueError:
            # target cell is free
            self.pos = newpos

    class CannotPushException(Exception):
        pass

    def step_wide(self, dir):        
        newpos = tuple(self.pos + dir)
        # Adjust coordinate for collision check with the right part of a wall or box.
        newpos2 = tuple(self.pos + dir - (0, 1))
        if newpos in self.walls or newpos2 in self.walls:
            return
        pushed_box_index = next((i for i, b in enumerate(self.boxes) if b == newpos or b == newpos2), None)
        try:
            all_pushed_box_indices = self.prepare_push(pushed_box_index, dir)
            self.pos = newpos
            for pushed_box_index in all_pushed_box_indices:
                self.boxes[pushed_box_index] = tuple(self.boxes[pushed_box_index] + dir)
        except Maze.CannotPushException:
            pass


    def prepare_push(self, box_index, dir):
        # Each box extends one cell to the right of its nominal position.
        # As above, we also need to check one cell to the left to account for the width
        # of other boxes or walls.
        if box_index is None:
            return []
        boxpos = self.boxes[box_index]
        boxpos_updated = [tuple(boxpos + dir + (0, i)) for i in range(-1, 2)] # grow box 1 cell each to the left and right
        if any(b in self.walls for b in boxpos_updated):
            raise Maze.CannotPushException()
        # Find directly pushed boxes
        directly_pushed = [i for i, b in enumerate(self.boxes) if b in boxpos_updated and i != box_index]
        # Recurse to find all pushed boxes. Boxes might be pushed by two neighbouring boxes, so it's essential to use a set!
        indirectly_pushed = set()
        for pushed in directly_pushed:
            indirectly_pushed.update(self.prepare_push(pushed, dir))
        return [box_index] + list(indirectly_pushed)


    def GPS_score(self):
        return sum(100 * y + x for y, x in self.boxes)


def get_answers(filename):
    maze, moves = get_data(filename)    
    return Maze(maze, widen=False).run(moves), Maze(maze).run(moves)


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
