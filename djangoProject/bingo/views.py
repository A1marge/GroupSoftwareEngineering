# Authors: Yoav Shimoni, Adam Brooks

from django.shortcuts import render
import random
from django.contrib.auth.decorators import login_required
from users.models import UserProfile, LeafcoinTransaction
# Create your views here.

@login_required
def bingo_view(request):
    board = make_board(rows=5, cols=5)
    
    if checkBingo(board):
        reward_leafcoins(request.user)

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
            board[i][j] = {"status": bool(random.getrandbits(1)), "challenge": "Challenge "+str(challenge), "url": "/game" +str(challenge)+"/"}

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

def reward_leafcoins(user):
    # Award Leafcoins when a user completes a bingo tile
    profile, created = UserProfile.objects.get_or_create(user=user)
    reward_amount = 1
    profile.leafcoins += reward_amount
    profile.save()
    LeafcoinTransaction.objects.create(user=user, amount=reward_amount, reason="Completed Bingo Tile")

