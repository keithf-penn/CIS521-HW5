from queue import Queue
from queue import PriorityQueue
from copy import deepcopy

############################################################
# CIS 521: Homework 5
############################################################

student_name = "Keith Fuchs"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

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
    boxes = sudoku_boxes()
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


def sudoku_boxes():
    # Items in same box
    # e.g. (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)
    boxes = []
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
    return boxes


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
                board[(row, col)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            else:
                board[(row, col)] = {int(value)}
    return board


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    BOXES = sudoku_boxes()

    def __init__(self, board):
        self.board = board
        self.rows = 9
        self.cols = 9
    
    def check_valid(self):
        try:
            row_valid = self.check_row()
            col_valid = self.check_col()
            box_valid = self.check_box()
            if row_valid == False or col_valid == False or box_valid == False:
                return False
            else:
                return True
        except:
            return False


    def check_row(self):
        row_valid = True
        for i in range(9):
            current_row = self.puzzle[i]
            if set(current_row) != set(range(1,10)):
                row_valid = False
                break
        return row_valid

    def check_col(self):
        col_valid = True
        for i in range(9):
            current_col = []
            for j in range(9):
                current_col.append(self.puzzle[j][i])
            if set(current_col) != set(range(1,10)):
                col_valid = False
                break
        return col_valid

    def check_box(self):
        box_valid = True
        for i in range(3):
            start_row = i*3
            for j in range(3):
                start_col = j*3
                current_box = []
                for ii in range(3):
                    for jj in range(3):
                        current_box.append(self.puzzle[start_row + ii][start_col+jj])
                if set(current_box) != set(range(1,10)):
                    box_valid = False
                    break
            if box_valid == False:
                break
        return box_valid


    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        """
        Retrieves the set from cell1, then if cell2 has a single value,
        removes that value from the set of cell1. Makes sure to
        add the popped value back into the original set.
        """
        protagonist = self.board[cell1]
        antagonist = self.board[cell2]
        if len(antagonist) == 1:
            ant_value = antagonist.pop()
            if ant_value not in protagonist:
                antagonist.add(ant_value)
                return False
            protagonist.remove(ant_value)
            antagonist.add(ant_value)
            return True
        return False

    def get_neighbors(self, cell):
        above = []
        below = []
        left = []
        right = []
        # ROWS
        for row in range(0, cell[0]):
            above.append((row, cell[1]))
        for row in range(cell[0] + 1, 9):
            below.append((row, cell[1]))
        # COLS
        for col in range(0, cell[1]):
            left.append((cell[0], col))
        for col in range(cell[1] + 1, 9):
            right.append((cell[0], col))
        # BOX
        location = None
        for box in self.BOXES:
            if cell in box:
                location = box
        location = set(location)
        location.remove(cell)
        box = list(location)
        return box, above + below, left + right

    def infer_ac3(self):
        q = Queue()
        for arc in self.ARCS:
            q.put(arc)
        while not q.empty():
            # We have an arc
            arc = q.get()
            # Check arc
            if self.remove_inconsistent_values(arc[0], arc[1]):
                neighbors = self.get_neighbors(arc[0])
                # neighbors = box, above + below, left + right
                neighbors = neighbors[0] + neighbors[1] + neighbors[2]
                for item in neighbors:
                    q.put((item, arc[0]))

    def infer_improved(self):
        not_finished = True
        while not_finished:
            not_finished = False
            self.infer_ac3()
            pq = PriorityQueue()
            for cell in self.CELLS:
                priority = len(self.board[cell])
                if priority == 1:
                    # Skip any cells that have a single value assigned
                    continue
                pq.put((priority, cell))
            while not pq.empty():
                cell = pq.get()[1]
                neighbors = self.get_neighbors(cell)
                box_vals = [self.board[v] for v in neighbors[0]]
                bv = {vv for v in box_vals for vv in v}
                col_vals = [self.board[v] for v in neighbors[1]]
                cv = {vv for v in col_vals for vv in v}
                row_vals = [self.board[v] for v in neighbors[2]]
                rv = {vv for v in row_vals for vv in v}
                for potential in self.board[cell]:
                    # neighbors = box, above + below, left + right
                    if potential not in bv:
                        self.board[cell] = {potential}
                        not_finished = True
                        continue
                    if potential not in cv:
                        self.board[cell] = {potential}
                        not_finished = True
                        continue
                    if potential not in rv:
                        self.board[cell] = {potential}
                        not_finished = True
                        continue


    def infer_with_guessing(self):
        print("calling guessing...")
        self.infer_improved()
        if self.check_valid():
            print(self.board)
            return
        else:
            print("trying to guess...")
            for cell in self.CELLS:
                for val in self.board[cell]:
                    new = Sudoku(deepcopy(self.board))
                    new.board[cell] = {val}
                    new.infer_with_guessing()
        






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


s = Sudoku(read_board("sudoku/easy.txt"))
s.infer_ac3()
print(s.board)
print(s.check_valid())
#
#
b = read_board(".\sudoku\medium1.txt")
x = Sudoku(b)
y = x.infer_improved()
print(x.check_valid())
# print(x.get_neighbors((3,5)))
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
#

# print(sudoku.get_values((0, 3)))

# for col in [0, 1, 4]:
#     removed = sudoku.remove_inconsistent_values((0, 3), (0, col))
#     print(removed, sudoku.get_values((0, 3)))

# b = read_board(".\sudoku\hard1.txt")
# x = Sudoku(b)
# print(x.infer_with_guessing())
