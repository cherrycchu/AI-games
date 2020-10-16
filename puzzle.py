from __future__ import division
from __future__ import print_function
from collections import deque

import sys
import math
import time
import queue as Q
import heapq
import resource

## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []
        self.g        = cost
        self.h        = cost
        self.depth    = 0

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])       # shoudn't 3 be replaced by self.n

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index < self.n:
            return None
        else:
            state = PuzzleState(list(self.config), self.n)
            blank = state.blank_index - self.n
            temp = state.config[state.blank_index]
            state.config[state.blank_index] = state.config[blank]
            state.config[blank] = temp
            state.blank_index = blank
            state.action = 'Up'
            state.parent = self
        return state
        
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index >= self.n * (self.n - 1):
            return None
        else:
            state = PuzzleState(list(self.config), self.n)
            blank = state.blank_index + self.n
            temp = state.config[state.blank_index]
            state.config[state.blank_index] = state.config[blank]
            state.config[blank] = temp
            state.blank_index = blank
            state.action = 'Down'
            state.parent = self
        return state
    
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == 0:
            return None
        else:
            state = PuzzleState(list(self.config), self.n)
            blank = state.blank_index - 1
            temp = state.config[state.blank_index]
            state.config[state.blank_index] = state.config[blank]
            state.config[blank] = temp
            state.blank_index = blank
            state.action = 'Left'
            state.parent = self
        return state

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if (self.blank_index + 1) % self.n == 0:
            return None
        else:
            state = PuzzleState(list(self.config), self.n)
            blank = state.blank_index + 1
            temp = state.config[state.blank_index]
            state.config[state.blank_index] = state.config[blank]
            state.config[blank] = temp
            state.blank_index = blank
            state.action = 'Right'
            state.parent = self
        return state
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt
            
def writeOutput(string, file="output.txt"):
    ### Student Code Goes here
    f = open(file, "a+")
    f.write(string)
    f.close()
    return


def backtracking(state, max_dep, expanded):
    path = deque()
    path_cost = 0
    while state.parent != None:
        path_cost += 1
        path.appendleft(	state.action)
        state = state.parent
    writeOutput("path_to_goal: " + str(list(path)) + "\n" +
                "cost_of_path: " + str(path_cost) + "\n" +
                "nodes_expanded: " + str(expanded) + "\n" +
                "search_depth: " + str(path_cost) + "\n" +
                "max_search_depth: " + str(max_dep) + "\n")
    return
    

def bfs_search(initial_state):
    """BFS search"""
    # initial_state -> PuzzleState
    frontier = Q.Queue()
    explored = set()
    visited = set()
    expanded = 0
    max_dep = 0
    
    frontier.put(initial_state)
    visited.add(str(initial_state.config))
    while not frontier.empty():
        state = frontier.get()
        explored.add(state)
        
        if test_goal(state):
            backtracking(state, max_dep, expanded)
            return "Success"
        
        state.expand()
        expanded += 1
        for child in state.children:
            if str(child.config) not in visited:
                child.depth = state.depth + 1
                if child.depth > max_dep:
                    max_dep = child.depth
                frontier.put(child)
                visited.add(str(child.config))
    return "Failure"
   
def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    frontier = deque()
    visited = set()
    expanded = 0
    max_dep = 0
    
    frontier.append(initial_state)
    visited.add(str(initial_state.config))
    while len(frontier):
        state = frontier.pop()
        
        if test_goal(state):
            backtracking(state, max_dep, expanded)
            return "Success"
        
        state.expand()
        expanded += 1
        for child in reversed(state.children):
            if str(child.config) not in visited:
                child.depth = state.depth + 1
                if child.depth > max_dep:
                    max_dep = child.depth
                frontier.append(child)
                visited.add(str(child.config))

    return "Failure"

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    config_to_p = {}
    frontier = []
    expanded = 0
    max_dep = 0
    
    heapq.heapify(frontier)
    calculate_total_cost(initial_state)
    heapq.heappush(frontier, (initial_state.cost, initial_state))
    
    config_to_p[tuple(initial_state.config)] = initial_state

    while len(frontier):
        state = heapq.heappop(frontier)[1]
        
        if test_goal(state):
            backtracking(state, max_dep, expanded)
            return "Success"
        
        state.expand()
        expanded += 1
        for child in state.children:
            if tuple(child.config) in config_to_p:
                child = config_to_p[tuple(child.config)]
                if (child.cost, child) in frontier and state.g < child.parent.g:
                    idx = frontier.index((child.cost, child))
                    calculate_total_cost(child)
                    child.depth = state.depth + 1
                    if child.depth > max_dep:
                        max_dep = child.depth
                    frontier[idx] = (child.cost, child)
                    heapq.heapify(frontier)
            else:
                child.depth = state.depth + 1
                if child.depth > max_dep:
                    max_dep = child.depth
                calculate_total_cost(child)
                heapq.heappush(frontier, (child.cost, child))
                config_to_p[tuple(child.config)] = child

    return "Failure"

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    if state.parent is None:
        state.g = 0
    else:
        state.g = state.parent.g + 1
    state.h = 0
    for idx, value in enumerate(state.config):
        state.h += calculate_manhattan_dist(idx, value, state.n)
    state.cost = state.g + state.h
    return

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    if value == 0:
        return 0
    return abs(value%3 - idx%3) + abs(value/3 - idx/3)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    return puzzle_state.config == [0, 1, 2, 3, 4, 5, 6, 7, 8]

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    factor = 1024E3             # factor for calculating ram usage
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    time_used = round(end_time-start_time, 8)
    ram_used = round(resource.getrusage(resource.RUSAGE_SELF)[2]/factor, 8)
    writeOutput("running_time: " + str(time_used) + "\n" +
                "max_ram_usage: " + str(ram_used) + "\n\n")

if __name__ == '__main__':
    main()
