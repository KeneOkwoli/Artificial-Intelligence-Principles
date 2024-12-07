import random
import pygame
import sys
import math
import numpy

Rows_number = 6
Column_number = 7
Black = (0,0,0)
Blue = (0,0,255)
Yellow = (255,255,0)
Red = (255,0,0)
set_length = 4
empty_slot = 0
player_token = 1
agent_token = 2


def DrawBoard():
    board = numpy.zeros((Rows_number,Column_number))
    return board

def PlaceToken(board, row, column, token):
    board[row][column] = token


def LocationValid(board, column):
    return board[Rows_number - 1][column] == 0

def NextRow(board,column):
    for r in range(Rows_number):
        if board[r][column] == 0:
            return r
        
def Win(board, token):
#checks horizontal for any wins
    for c in range(Column_number - 3):
        for r in range(Rows_number):
            if board[r][c] == token and board[r][c+1] == token and board[r][c+2] == token and board[r][c+3] == token:
                return True
#checks vertical for any wins
    for c in range(Column_number):
        for r in range(Rows_number - 3):
            if board[r][c] == token and board[r+1][c] == token and board[r+2][c] == token and board[r+3][c] == token:
                return True               
            
#checking diaginals to the right
    for c in range(Column_number - 3):
        for r in range(Rows_number - 3 ):
            if board[r][c] == token and board[r+1][c+1] == token and board[r+2][c+2] == token and board[r+3][c+3] == token:
                return True


#checking diagonals to the left
    for c in range(Column_number - 3):
        for r in range(3, Rows_number):
            if board[r][c] == token and board[r-1][c+1] == token and board[r-2][c+2] == token and board[r-3][c+3] == token:
                return True     
                   
def CheckBoard(set,token):
    score = 0
    other_token = player_token
    if token == player_token:
        other_token = agent_token
    if set.count(token) == 4:
        score += 100
    elif set.count(token) == 3 and set.count(empty_slot) == 1:
        score +=10
    elif set.count(token) == 2 and set.count(empty_slot) == 2:
        score += 5
    if set.count(other_token) == 3 and set.count(empty_slot) == 1:
        score -= 80
    return score

def Score(board,token):
    score = 0
    #Vertical
    for c in range(Column_number):
        c_array = [int(i) for i in list(board[:,c])]
        for r in range(Rows_number - 3):
            set = c_array[r:r+set_length]
            score += CheckBoard(set, token)
                
    #Horizontal
    for r in range(Rows_number):
        r_array = [int(i) for i in list(board[r,:])]
        for c in range(Column_number - 3):
            set = r_array[c:c+set_length]
            score += CheckBoard(set, token)

    #Right Diagonal
    for r in range(Rows_number -3 ):
        for c in range(Column_number - 3):
            set = [board[r+i][c+i] for i in range(set_length)]
            score += CheckBoard(set, token)

    #Left Diagonal
    for r in range(Rows_number -3 ):
        for c in range(Column_number - 3):
            set = [board[r+3-i][c+i] for i in range(set_length)]
            score += CheckBoard(set, token)

    return score    

def OptionalLocations(board):
    location = []
    for column in range(Column_number):
        if LocationValid(board, column):
            location.append(column)
    return location

def OptimalMove(board,token):
    locations = OptionalLocations(board)    
    ideal_column = random.choice(locations)
    best_score = -1000
    for column in locations:
        row = NextRow(board, column)
        temp_board = board.copy()
        PlaceToken(temp_board, row, column,token)
        points = Score(temp_board, token)
        if points > best_score:
            best_score = points
            ideal_column = column
    return ideal_column

def FlipBoard(board):
    print(numpy.flip(board,0))


board = DrawBoard()
FlipBoard(board)
turn = random.randint(0,1)
gameOver = False



pygame.init()
square_size = 100
Radius = int(square_size/2 -8)
board_width = Column_number * square_size
board_height = Rows_number * square_size
size = (board_width,board_height)
screen = pygame.display.set_mode(size)
pygame.display.update()

def VisualBoard(board):
    for i in range(Column_number):
        for j in range(Rows_number):
            pygame.draw.rect(screen, Blue , (i*square_size , j*square_size + square_size, square_size, square_size))
            pygame.draw.circle(screen, Black, (int(i*square_size+square_size/2), int(j*square_size+square_size/2)),Radius)
	
    for i in range(Column_number):
        for j in range(Rows_number):
            if board [j][i] == 1:
                pygame.draw.circle(screen, Yellow, (int(i*square_size+square_size/2), board_height-int(j*square_size+square_size/2)),Radius)
            if board [j][i] == 2:
                pygame.draw.circle(screen, Red, (int(i*square_size+square_size/2), board_height-int(j*square_size+square_size/2)),Radius)                
    pygame.display.update()

VisualBoard(board)
pygame.display.update()



while not gameOver:
    if turn == 0:
        print("Your move")
    else:
        print("AI move")
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black ,(0,0,board_width, square_size))
            x_pos = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen,Yellow, (x_pos,int(square_size/2)) , Radius)

        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
             # Player 1 input
            if turn == 0:
                x_pos = event.pos[0]
                column = int(math.floor(x_pos/square_size))

                if LocationValid(board, column):
                    row = NextRow(board, column)
                    PlaceToken(board, row, column, 1)
                    if Win(board,1):
                        print("You won!")
                        gameOver = True
                    turn +=1
                    turn = turn % 2 
                    FlipBoard(board)
                    VisualBoard(board)
                        
            
    # Player 2 input
    if turn == 1 and not gameOver: 
        #column = random.randint(0, COLUMNS_NUMBER - 1)
        column = OptimalMove(board , 2)
        if LocationValid(board, column):
            FlipBoard(board)
            VisualBoard(board)
            pygame.time.wait(1000)
            row = NextRow(board, column)
            PlaceToken(board, row, column, 2)       
            if Win(board,2):
                print("AI wins!")
                gameOver = True
                                    
            FlipBoard(board)
            VisualBoard(board)
            turn +=1
            turn = turn % 2 

    if gameOver:
        pygame.time.wait(3000)

