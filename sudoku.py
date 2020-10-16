#!/usr/bin/env python
#coding:utf-8

import queue as Q
import time
from statistics import mean, stdev
import sys

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"

def get_grids(row, col):
    # get grids from row and column
    return [ r + c for c in col for r in row]

def get_neighbors(grids, neighbors_list):
    neighbors = {}
    for g in grids:
        neighbors[g] = set()
        for n in neighbors_list:
            if g in n:
                neighbors[g] |= set(n)
    return neighbors

GRIDS = get_grids(ROW, COL)

NEIGHBORS_LIST = ([get_grids(ROW, c) for c in COL] +
                  [get_grids(r, COL) for r in ROW] +
                  [get_grids(r, c) for c in ('123', '456', '789') for r in ('ABC', 'DEF', 'GHI')])

NEIGHBORS = get_neighbors(GRIDS, NEIGHBORS_LIST)

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def mrv(csp):
    # minimum remaining variable heuristic
    # return a variable e.g. A1
    return min(csp, key=csp.get)

def lcv(var, assignment, csp):
    # least constraining value
    # return list of value in lcv order
    neighbors = NEIGHBORS[var]
    unassigned_neighbors = neighbors.difference(set(assignment.keys()))
    assigned_neighbors = neighbors.intersection(set(assignment.keys()))
    constraints = [assignment[n] for n in assigned_neighbors]
     ## initialize list of domain value for a variable
    domain = {}
    for value in csp[var]:
        if value not in constraints:
            domain[value] = 0
    ## find the least contraining value by exmaining neighbor domains    
    for n in unassigned_neighbors:
        for d in csp[n]:
            if d in domain:
                domain[d] += 1       # increment value count
    ## sort the lcv dict in ascending order
    domain_in_lcv = [item[0] for item in sorted(domain.items(), key=lambda x:x[1])]
    return domain_in_lcv, unassigned_neighbors

def backtrack(assignment, csp):
    # check if assignment is complete
    if len(assignment) == 81:
        return assignment
    if len(csp) == 0:
        return "failure"
    var = mrv(csp)
    recover = {}    # for csp backtracking
    lcv_domain, unassigned_neighbors = lcv(var, assignment, csp)
    for value in lcv_domain:
        assignment[var] = value
        recover[var] = csp[var]
        del csp[var]
        result = backtrack(assignment, csp)
        if result != "failure":
            return result
        del assignment[var]
        csp[var] = recover[var]
    return "failure"

def backtracking(board):
    """Takes a board and returns solved board."""
    # setup a assignment and domain dictionary
    assignment = {}
    csp = {}
    for var in board:
        if board[var] != 0:
            assignment[var] = board[var]
        else:
            csp[var] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            #for n in neighbors_of(var):
            #    csp[var].discard(board[n])
    # restrict domains by propagating assignment
    ## commenting out the following solves hardest sudoku in 40 secs

    for var in assignment.keys():
        for n in NEIGHBORS[var]:
            if n in csp:
                csp[n].discard(assignment[var])
    solved_board = backtrack(assignment, csp)
    return solved_board


if __name__ == '__main__':
    
    """
    #  Read boards from source.
    src_filename = 'sudokus_start.txt'
    #src_filename = 'hardest_sudoku.txt'
    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()
    """
    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")

    running_time = []
    
    # Solve each board using backtracking
    line = sys.argv[1]

    # Parse boards to dict representation, scanning board L to R, Up to Down
    board = { ROW[r] + COL[c]: int(line[9*r+c])
        for r in range(9) for c in range(9)}

    # Print starting board. TODO: Comment this out when timing runs.
    print_board(board)

    # Solve with backtracking
    #start_time  = time.time()
    solved_board = backtracking(board)
    #end_time = time.time()

    # Print solved board. TODO: Comment this out when timing runs.
    print_board(solved_board)

    # Write board to file
    outfile.write(board_to_string(solved_board))
    outfile.write('\n')
    #print("running_time: " + str(end_time-start_time))
