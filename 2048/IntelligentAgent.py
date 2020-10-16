import time
#import math
from BaseAI import BaseAI

# DONE: use clock to time each move
# DONE: implement expectiminimax
# DONE: alpha-beta pruning
# DONE: use # of free tiles, then move on to more complex

MAX_DEPTH = 5
POS_INF = float('Inf')
NEG_INF = float('-Inf')
TIME_LIMIT = 0.15
CHANCE = {"two":0.9, "four":0.1}

def compare(x, y):
    if x > y:
        return -1
    elif x < y:
        return 1
    else:
        return 0


def free_tiles(state):
    """ evaluation of a state """
    # count number of free tiles
    count = 0;
    (move, grid) = state
    for x in range(grid.size):
        for y in range(grid.size):
            if grid.map[x][y] == 0:
                count += 1
    return count*grid.getMaxTile()
    #return count


def monotonicity(state):
    (__, grid) = state
    mono = 0
    for i in range(4):
        #prev = compare(grid.map[i][0], grid.map[i][1])
        for j in [1, 2, 3]:
            current = compare(grid.map[i][j-1], grid.map[i][j])
            if current == 1:
                #mono -= 1
                mono -= abs(grid.map[i][j-1] - grid.map[i][j])
    for j in range(4):
        #prev = compare(grid.map[0][j], grid.map[1][j])
        for i in [1, 2, 3]:
            current = compare(grid.map[i-1][j], grid.map[i][j])
            if current == 1:
                #mono -= 1
                mono -= abs(grid.map[i-1][j] - grid.map[i][j])
    return mono


def smoothness(state):
    (__, grid) = state
    smooth = 0
    #for i in [1, 2, 3]:
    #    for j in [1, 2, 3]:
    #        if (grid.map[i][j-1] * grid.map[i][j]) != 0:
    #            smooth -= abs((grid.map[i][j-1] - grid.map[i][j]))
    #            smooth -= abs((grid.map[i-i][j] - grid.map[i][j]))
    for i in range(4):
        for j in [1, 2, 3]:
            smooth -= abs((grid.map[i][j-1] - grid.map[i][j]))
    for j in range(4):
        for i in [1, 2, 3]:
            smooth -= abs((grid.map[i][j-1] - grid.map[i][j]))
    return smooth

 
def utility(state):
    #print(free_tiles(state), monotonicity(state), smoothness(state))
    return (free_tiles(state) + 5*monotonicity(state) + 2*smoothness(state))
    #return (1/100*free_tiles(state) + monotonicity(state) + smoothness(state))

def decision(state, time_limit, depth):
    """ return optimal move """
    ((move, __), __) = maximize(state, NEG_INF, POS_INF, time_limit, depth+1)
    #print(f"time used: {end_time - start_time}")
    return move


def chance(state, alpha, beta, time_limit, depth):
    """ get average all chance event: value = {2, 4} """
    (__, two_utility) = minimize(state, 2, alpha, beta, time_limit, depth)
    (__, four_utility) = minimize(state, 4, alpha, beta, time_limit, depth)
    return (CHANCE["two"] * two_utility + CHANCE["four"] * four_utility)
    

def minimize(state, value, alpha, beta, time_limit, depth):
    """ find child state with the lowest utility value """
    # for minimize (Computer AI)
    # move = (cell, value)
    (move, grid) = state
    
    cells = grid.getAvailableCells()
    
    if (len(cells) == 0):
        return (state, utility(state))
    
    if time.clock() > time_limit or depth > MAX_DEPTH:
        return (state, utility(state))
    
    (min_child, min_utility) = ((None, None), POS_INF)
        
    for cell in cells:
        child_grid = grid.clone()
        child_grid.insertTile(cell, value)
        child = ((cell, value), child_grid)
        
        (__, child_utility) = maximize(child, alpha, beta, time_limit, depth+1)
        
        if child_utility < min_utility:
            (min_child, min_utility) = (child, child_utility)
            
        if min_utility <= alpha:
            break
        
        if min_utility < beta:
            beta = min_utility
    
    return (min_child, min_utility)


def maximize(state, alpha, beta, time_limit, depth):
    """ find child state with highest utility value """
    (move, grid) = state
    
    moveset = grid.getAvailableMoves()
    
    if (len(moveset) == 0):
        return (state, utility(state))
    
    if time.clock() > time_limit or depth > MAX_DEPTH:
        return (state, utility(state))
    
    (max_child, max_utility) = ((None, None), NEG_INF)
    
    for child in moveset:
        child_utility = chance(child, alpha, beta, time_limit, depth+1)
        
        if child_utility > max_utility:
            (max_child, max_utility) = (child, child_utility)
            
        if max_utility >= beta:
            break
        
        if max_utility > alpha:
            alpha = max_utility

    return (max_child, max_utility)    
    

class IntelligentAgent(BaseAI):
    def getMove(self, grid): 
        time_limit = time.clock() + TIME_LIMIT
        move = None
        depth = 0
        state = (move, grid)            # state: tuple(grid, move, depth)
        return decision(state, time_limit, depth)