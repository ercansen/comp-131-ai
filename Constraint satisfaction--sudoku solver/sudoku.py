# Comp 131: AI
# HW 3: Constraint Satisfaction Problem
# October 30, 2019
# Steven Attardo and Ercan Sen

import numpy as np
from operator import itemgetter
import sys
import random

# Size of sudoku grid (n x n)
n = 9
sqn = int(np.sqrt(n))

# Check if any constraints are violated in state
def check_valid(state):
    # Check rows
    for i in range(n):
        row = list(state[i,:])
        z = row.count(0)
        duplicates = len(row)-len(set(row))
        if (duplicates-np.max([z-1,0])) > 0:
            return False
    # Check columns
    for i in range(n):
        col = list(state[:,i])
        z = col.count(0)
        duplicates = len(col)-len(set(col))
        if (duplicates-np.max([z-1,0])) > 0:
            return False
    # Check squares
    for i in range(sqn):
        for j in range(sqn):
            square = list((state[i*sqn:(i+1)*sqn,j*sqn:(j+1)*sqn]).flatten())
            z = square.count(0)
            duplicates = len(square)-len(set(square))
            if (duplicates-np.max([z-1,0])) > 0:
                return False
    # Valid
    return True

# Generate remaining possible values for empty squares in state
def calc_possibilities(state):
    pos=[[[] for i in range(n)] for j in range(n)]
    for i in range(n): # row
        for j in range(n): #col
            # Square i,j already filled
            if state[i,j] != 0:
                pos[i][j] = state[i,j]
            else:
                # Start with all values
                remaining = list(range(1,n+1))
                # Remove conflicts in row
                for k in range(n):
                    if state[i,k] != 0:
                        remaining.remove(state[i,k])
                # Remove conflicts in column
                for k in range(n):
                    if state[k,j] != 0:
                        try:
                            remaining.remove(state[k,j])
                        except:
                            pass
                # Remove conflicts in region
                si = (i//sqn)*sqn
                sj = (j//sqn)*sqn
                square = list((state[si:si+sqn,sj:sj+sqn]).flatten())
                for k in range(n):
                    if square[k] != 0:
                        try:
                            remaining.remove(square[k])
                        except:
                            pass
                # Store remaining possibilities
                pos[i][j].extend(remaining)
    return pos                          

# Return location of square with fewest possible values
def select_variable(pos):
    num_choices = []
    for i in range(n):
        for j in range(n):
            # If value at i,j not already fixed,
            ## add square to selection set
            if isinstance(pos[i][j],list):
                num_choices.append((len(pos[i][j]),i,j))
    # Randomize order, so ties don't always choose lowest index
    random.shuffle(num_choices)
    # Sort by number of possibilities only
    num_choices.sort(key=itemgetter(0))
    if num_choices[0][0] > 0:
        # Every square has at least one possible value
        i = num_choices[0][1]
        j = num_choices[0][2]
        return i,j
    else:
        # Some square has no possible values
        return -1,-1

# Check if state is completed puzzle
def check_done(state):
    unique, counts = np.unique(state,return_counts=True)
    c = dict(zip(unique,counts))
    if 0 in c.keys():
        return False
    else:
        return True

# Recursively solve puzzle given state
def backtracking(parent_state,depth):
    # Copy state, otherwise original modified by reference
    state = parent_state.copy()

    if check_done(state):
        return state
    
    # Calculate possible values left for each empty square
    possible = calc_possibilities(state)
    # Choose square with fewest possible values
    i, j = select_variable(possible)
    if i < 0:
        # Some square has no possible value
        return False
    # Possibilities for i,j
    local_pos = possible[i][j]
    # Try to solve for each possibility
    for current in local_pos:
        state[i,j] = current
        if check_valid(state):
            result = backtracking(state,depth+1)
            # Result either false or solution
            # If boolean then false
            if type(result) != type(False):
                return result
    # No solution for any of the possible values, must backtrack
    return False
            
# Initialize starting state of puzzle by name    
def initial_state(select):
    global n
    global sqn
    # 0's used to represent unfilled squares
    easy = [[6,0,8,7,0,2,1,0,0],
            [4,0,0,0,1,0,0,0,2],
            [0,2,5,4,0,0,0,0,0],
            [7,0,1,0,8,0,4,0,5],
            [0,8,0,0,0,0,0,7,0],
            [5,0,9,0,6,0,3,0,1],
            [0,0,0,0,0,6,7,5,0],
            [2,0,0,0,9,0,0,0,8],
            [0,0,6,8,0,5,2,0,3]]

    hard = [[0,7,0,0,4,2,0,0,0],
            [0,0,0,0,0,8,6,1,0],
            [3,9,0,0,0,0,0,0,7],
            [0,0,0,0,0,4,0,0,9],
            [0,0,3,0,0,0,7,0,0],
            [5,0,0,1,0,0,0,0,0],
            [8,0,0,0,0,0,0,7,6],
            [0,5,4,8,0,0,0,0,0],
            [0,0,0,6,1,0,0,5,0]]

    if select == 'easy':
        return np.array(easy)
    elif select == 'hard':
        return np.array(hard)
    elif select == 'empty' or select == 'empty3':
        return np.zeros((n,n),dtype=int)
    elif select == 'empty4':
        n = 16
        sqn = int(np.sqrt(n))
        return np.zeros((n,n),dtype=int)
#    elif select == 'empty5':
#        # can take a very long time
#        n = 25
#        sqn = int(np.sqrt(n))
#        return np.zeros((n,n),dtype=int)
    else:
        print('No puzzle named',select)

def main(puzzle):
    state = initial_state(puzzle)
    print('Puzzle Start:')
    print(str(state).replace('0',' '))

    solution = backtracking(state,0)
    print('\nDone!\nPuzzle Solution:')
    print(solution)

if __name__== '__main__':
    if len(sys.argv) > 1:
        puzzle = sys.argv[1]
    else:
        puzzle = 'easy'
        print('Defaulting to puzzle: easy')
        print('To select: sudoku.py <easy|hard|empty>')

    main(puzzle)
