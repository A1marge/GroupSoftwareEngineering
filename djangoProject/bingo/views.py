# Authors: Yoav Shimoni, Adam Brooks

from django.shortcuts import render
import random
# Create your views here.

def bingo_view(request):
    board = make_board(rows=5, cols=5)
    return render(request, 'bingo.html', {'board': board})

# Returns generated board variable with random integer values
# 4x4
def make_board(rows,cols):
    # status: complete or incomplete
    # challenge: the text displayed
    # url: links to the challenge page

    numbers = random.sample(range(1, 16+1), 16)
    board = [ [0]*4 for i in range(4)]
    for i in range(0,4):
        for j in range(0,4):
            challenge = numbers.pop()
            board[i][j] = {"status": bool(random.getrandbits(1)), "challenge": str(challenge), "url": "/game" +str(challenge)+"/"}

    return board

# Checks the provided board for bingos. Returns True if bingo, False otherwise.
def checkBingo(board):

    # Check Rows
    for i in range(4):
        if all(board[i][j]["status"] == 1 for j in range(4)):
            return True

    # Check Cols
    for i in range(4):
        if all(board[j][i]["status"] == 1 for j in range(4)):
            return True

    # Check Leading Diagonal
    if all(board[i][i]["status"] == 1 for i in range(4)):
        return True

    # Check Anti-Diagonal
    if all(board[i][3 - i]["status"] == 1 for i in range(4)):
        return True

    return False

# Marks the square with the given ID on the given board. Returns board.
def markSquare(board, squareID):
    # Invalid ID
    if(squareID > 16 or squareID < 1):
        return board

    # Find square with provided ID
    for i in range(0,4):
        for j in range(0,4):
            challenge = board[i][j]["challenge"]
            if(challenge == squareID):
                # Square Found!
                board[i][j]["status"] == 1
                return board

    # Square was not found.
    return board
