############################################################
# CIS 521: Homework 5
############################################################

student_name = "Type your full name here."

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
    obj = Sudoku()
    pass

def sudoku_arcs():
    pass

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
            board[(row, col)] = lines[row][col]
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board
        self.rows = 9
        self.cols = 9
        
        pass

            
    def get_values(self, cell):
        if self.board[cell] == '*':
            return set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        else:
            return set([self.board[cell]])

    def remove_inconsistent_values(self, cell1, cell2):
        pass

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
feedback_question_1 = 0

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

b = read_board(".\sudoku\medium1.txt")
print(b)
x = Sudoku(b)
print(x.get_values((0, 0)))
print(x.get_values((0, 1)))
