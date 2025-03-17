# Authors: Yoav Shimoni, Adam Brooks

from django.shortcuts import render
import random
# Create your views here.

def bingo_view(request):
    # Get or create board layout
    board_layout = request.session.get("board_layout", None)
    if board_layout is None:
        # First time visiting - create new random board
        numbers = random.sample(range(1, 16+1), 16)
        board_layout = []
        for i in range(4):
            row = []
            for j in range(4):
                row.append(numbers.pop())
            board_layout.append(row)
        request.session["board_layout"] = board_layout

    # Get completed challenges
    completed_challenges = request.session.get("completed_challenges", [])
    
    # Create board with completion status
    board = [[None]*4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            challenge = board_layout[i][j]
            board[i][j] = {
                "status": (challenge in completed_challenges),
                "challenge": str(challenge),
                "url": f"/game{challenge}/"
            }

    return render(request, 'bingo.html', {'board': board})

# Returns generated board variable with random integer values
# 4x4
'''def make_board(rows,cols, completed_challenges=[]):
    # status: complete or incomplete
    # challenge: the text displayed
    # url: links to the challenge page

    numbers = random.sample(range(1, 16+1), 16)
    board = [ [0]*4 for i in range(4)]
    for i in range(0,4):
        for j in range(0,4):
            challenge = numbers.pop()
            status = (challenge in completed_challenges)
            board[i][j] = {"status": status, "challenge": str(challenge), "url": "/game" +str(challenge)+"/"}

    return board'''

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
                board[i][j]["status"] = 1
                return board

    # Square was not found.
    return board
