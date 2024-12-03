import random
import pygame
import sys
import math
import numpy

ROWS_NUMBER = 6
COLUMNS_NUMBER = 7


def DrawBoard():
    board = numpy.zeros((ROWS_NUMBER,COLUMNS_NUMBER))
    return board

def DropToken(board, row, column, token):
    board[row][column] = token


def LocationValid(board, column):
    return board[ROWS_NUMBER - 1][column] == 0

def NextRow(board,column):
    for r in range(ROWS_NUMBER):
        if board[r][column] == 0:
            return r
        
def Win(board, token):
#checks horizontal for any wins
    for c in range(COLUMNS_NUMBER - 3):
        for r in range(ROWS_NUMBER):
            if board[r][c] == token and board[r][c+1] == token and board[r][c+2] == token and board[r][c+3] == token:
                return True
#checks horizontal for any wins
    for c in range(COLUMNS_NUMBER):
        for r in range(ROWS_NUMBER - 3):
            if board[r][c] == token and board[r+1][c] == token and board[r+2][c] == token and board[r+3][c] == token:
                return True               
            
#checking diaginals to the right
    for c in range(COLUMNS_NUMBER - 3):
        for r in range(ROWS_NUMBER - 3 ):
            if board[r][c] == token and board[r+1][c+1] == token and board[r+2][c+2] == token and board[r+3][c+3] == token:
                return True


#checking diagonals to the left
    for c in range(COLUMNS_NUMBER - 3):
        for r in range(3, ROWS_NUMBER - 3 ):
            if board[r][c] == token and board[r-1][c+1] == token and board[r-2][c+2] == token and board[r-3][c+3] == token:
                return True            

def FlipBoard(board):
    print(numpy.flip(board,0))


board = DrawBoard()
FlipBoard(board)
turn = 0
gameOver = False


while not gameOver:
    # Player 1 input
    if turn == 0:
        column = int(input("Player 1s choice: "))
        if LocationValid(board, column):
            row = NextRow(board, column)
            DropToken(board, row, column, 1)
            if Win(board,1):
                print("Player 1 is the winner!")
                gameOver = True
                break
    
    # Player 2 input
    else: 
        column = int(input("Player 2s choice: "))
        if LocationValid(board, column):
            row = NextRow(board, column)
            DropToken(board, row, column, 2)       
            if Win(board,2):
                print("Player 2 is the winner!")
                gameOver = True
                break             

    FlipBoard(board)
    turn +=1
    turn = turn % 2

