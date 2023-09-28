############################################################
# CIS 521: Homework 5
############################################################

student_name = "Keith Fuchs"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import collections
import copy
import itertools
import random
import math

############################################################
# Sudoku Solver
############################################################

def sudoku_cells():
    cells = []
    rows = 9
    cols = 9
    for row in range(rows):
        for col in range(cols):
            cells.append((row, col))
    return cells

def sudoku_arcs():
    # Provides a tuple of pairs of tuples.
    # The pairs are in same arc.
    arcs = []
    # Items in same row
    # Items in same column
    for row in range(9):
        for col in range(9):
            for offset in range(9):
                square = (row, col)
                horiz_arc = (row, offset)
                verti_arc = (offset, col)
                if square != horiz_arc:
                    if (square, horiz_arc) not in arcs:
                        arcs.append((square, horiz_arc))
                if square != verti_arc:
                    if (square, verti_arc) not in arcs:
                        arcs.append((square, verti_arc))
    # Items in same box
    # e.g. (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)
    boxes = []
    box = []
    offset1 = 0
    offset2 = 0
    while offset1 < 9:
        while offset2 < 9:
            box = []
            for row in range(3):
                for col in range(3):
                    square = (row + offset1, col + offset2)
                    box.append(square)
            boxes.append(box)
            offset2 += 3
        offset2 = 0
        offset1 += 3

    offset1 = 0
    offset2 = 0
    for box in boxes:
        for row in range(0 + offset2, 3 + offset2):
            for col in range(0 + offset1, 3 + offset1):
                square = (row, col)
                for item in box:
                    if item != square:
                        a1 = (item, square)
                        if a1 not in arcs:
                            arcs.append(a1)
                        a2 = (square, item)
                        if a2 not in arcs:
                            arcs.append(a2)                        
        offset1 += 3
        if offset1 == 9:
            offset1 = 0
            offset2 += 3
            
    return arcs
        
    
def read_board(path):
    board = dict()
    line = True
    lines = []
    with open(path) as f:
        while line:
            line = f.readline().strip()
            if len(line) != 0:
                lines.append(line)
    rows, cols = 9, 9
    for row in range(rows):
        for col in range(cols):
            value = lines[row][col]
            if value == '*':
                board[(row, col)] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                board[(row, col)] = set([int(value)])
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board
        self.rows = 9
        self.cols = 9

            
    def get_values(self, cell):
            return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        """
        Retrieves the set from cell1, then if cell2 has a value,
        removes that value from the set of cell1.
        """
        antagonist = self.board[cell2]
        print(antagonist)
        if len(antagonist) == 1:
            self.board[cell1].remove(antagonist.pop())
            return True
        return False
            
        
        

    def infer_ac3(self):
        pass

    def infer_improved(self):
        pass

    def infer_with_guessing(self):
        pass
    


############################################################
# Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 20

feedback_question_2 = """
f
"""

feedback_question_3 = """
f
"""

# b = read_board(".\sudoku\medium1.txt")
# print(b)
# x = Sudoku(b)
# print(x.get_values((0, 0)))
# print(x.get_values((0, 1)))
# # print(sudoku_cells())
# # print(sudoku_arcs())
# print(((0, 0), (0, 8)) in sudoku_arcs())
# print(((0, 0), (8, 0)) in sudoku_arcs())
# print(((0, 8), (0, 0)) in sudoku_arcs())
# print(((0, 0), (2, 1)) in sudoku_arcs())
# print(((2, 2), (0, 0)) in sudoku_arcs())
# print(((2, 3), (0, 0)) in sudoku_arcs())

# sudoku = Sudoku(read_board("sudoku/easy.txt"))
# print(sudoku.get_values((0, 3)))

# for col in [0, 1, 4]:
#     removed = sudoku.remove_inconsistent_values((0, 3), (0, col))
#     print(removed, sudoku.get_values((0, 3)))



