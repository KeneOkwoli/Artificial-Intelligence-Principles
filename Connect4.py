import random
import pygame
import sys
import math
import numpy

ROWS_NUMBER = 6
COLUMNS_NUMBER = 7
Black = (0,0,0)
Blue = (0,0,255)
Yellow = (255,255,0)
Red = (255,0,0)


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
        for r in range(3, ROWS_NUMBER):
            if board[r][c] == token and board[r-1][c+1] == token and board[r-2][c+2] == token and board[r-3][c+3] == token:
                return True            

def FlipBoard(board):
    print(numpy.flip(board,0))


board = DrawBoard()
FlipBoard(board)
turn = 0
gameOver = False



pygame.init()
square_size = 100
Radius = int(square_size/2 -8)
board_width = COLUMNS_NUMBER * square_size
board_height = ROWS_NUMBER * square_size
size = (board_width,board_height)
screen = pygame.display.set_mode(size)
pygame.display.update()

def visual_board(board):
    for i in range(COLUMNS_NUMBER):
        for j in range(ROWS_NUMBER):
            pygame.draw.rect(screen, Blue , (i*square_size , j*square_size + square_size, square_size, square_size))
            pygame.draw.circle(screen, Black, (int(i*square_size+square_size/2), int(j*square_size+square_size/2)),Radius)
	
    for i in range(COLUMNS_NUMBER):
        for j in range(ROWS_NUMBER):
            if board [j][i] == 1:
                pygame.draw.circle(screen, Yellow, (int(i*square_size+square_size/2), board_height-int(j*square_size+square_size/2)),Radius)
            if board [j][i] == 2:
                pygame.draw.circle(screen, Red, (int(i*square_size+square_size/2), board_height-int(j*square_size+square_size/2)),Radius)                
    pygame.display.update()

visual_board(board)
pygame.display.update()

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black ,(0,0,board_width, square_size))
            x_pos = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen,Yellow, (x_pos,int(square_size/2)) , Radius)
            else:
                pygame.draw.circle(screen,Red, (x_pos,int(square_size/2)) , Radius)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
             # Player 1 input
            if turn == 0:
                x_pos = event.pos[0]
                column = int(math.floor(x_pos/square_size))

                if LocationValid(board, column):
                    row = NextRow(board, column)
                    DropToken(board, row, column, 1)
                    if Win(board,1):
                        print("Player 1 is the winner!")
                        gameOver = True
                        
            
            # Player 2 input
            else: 
                x_pos = event.pos[0]
                column = int(math.floor(x_pos/square_size))
                if LocationValid(board, column):
                    row = NextRow(board, column)
                    DropToken(board, row, column, 2)       
                    if Win(board,2):
                        print("Player 2 is the winner!")
                        gameOver = True
                                    

            FlipBoard(board)
            visual_board(board)
            turn +=1
            turn = turn % 2 

            if gameOver:
                pygame.time.wait(3000)

