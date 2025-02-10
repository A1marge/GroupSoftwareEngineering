#from django.db import models


# Returns boolean representing whether the provided 4x4 2D array of
#   boolean values represents winning bingo board
def checkWin(board):
    
    # Check Rows/Cols
    for i in range(4):
        if all(board[i]):
            return True
        if all(board[j][i] for j in range(4)):
            return True

    # Check Diagonals
    if all(board[i][i] for i in range(4)):
        return True

    if all(board[i][3 - i] for i in range(4)):
        return True

    return False


board = [
    [True, True, False, True],
    [False, True, True, False],
    [True, False, True, False],
    [True, False, True, True]]


print(checkWin(board))
