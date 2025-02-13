#from django.db import models
import random

# Data type is a 2D array with each element as a tuple,
# where each tuple contains an integer for the activity ID and a boolean for its state.


# Returns generated board variable with random integer values
# 4x4, max_id is the largest possible id.
def generateBoard():
    max_id = 16
    numbers = random.sample(range(1, max_id+1), 16)
    board = [[(numbers[i * 4 + j], False) for j in range(4)] for i in range(4)]
    return board


# Returns board where the given squareID is set to true.
def markSquare(board, squareID):
    for i in range(0,4):
        for j in range(0,4):
            if(board[i][j][0] == squareID):
                board[i][j] = (squareID, True)
                break
    return board
    
# Returns boolean representing whether the provided 4x4 2D array of
#   boolean values represents winning bingo board
def checkWin(board):

    # Check Rows
    for i in range(4):
        if all(board[i][j][1] for j in range(4)):
            print("Bingo By Row!")
            return True

    # Check Cols
    for i in range(4):
        if all(board[j][i][1] for j in range(4)):
            print("Bingo by Col!")
            return True

    # Check Leading Diagonal
    if all(board[i][i][1] for i in range(4)):
        print("Bingo by leading diag!")
        return True

    # Check Anti-Diagonal
    if all(board[i][3 - i][1] for i in range(4)):
        print("Bingo by anti diag!")
        return True

    return False



board = generateBoard()
print("Board: ", board)
while(not checkWin(board)):
    print("New Turn")
    print("")
    picked = random.randint(0,16)
    print(picked, " was picked")
    board = markSquare(board, picked)
    print("My board now looks like:")
    print(board)

print("Bingo!")
