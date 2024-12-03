import random
import pygame
import sys
import math
import numpy

ROWS_NUMBER = 6
COLUMNS_NUMBER = 7


def DrawBoard():
    board = numpy.zeros((6,7))
    return board

def DropToken(board, row, column, token):
    board[row][column] == token


def LocationValid(board, column):
    return board[ROWS_NUMBER - 1][column] == 0

def NextRow(board,column):
    for r in range(ROWS_NUMBER):
        if board[r][column] == 0:
            return r

board = DrawBoard()
print(board)
turn = 0
gameOver = False


while not gameOver:
    # Player 1 input
    if turn == 0:
        column = int(input("Player 1s choice: "))
        if LocationValid(board, column):
            row = NextRow(board, column)
            DropToken(board, row, column, 1)
    
    # Player 2 input
    else: 
        column = int(input("Player 2s choice: "))
        if LocationValid(board, column):
            row = NextRow(board, column)
            DropToken(board, row, column, 2)        

    turn +=1
    turn = turn % 2

