## Kenechukwu Okwoli - 23010818

import random
import pygame
import sys
import math
import numpy

# Constants
Rows_number = 6 # number of rows on the board
Column_number = 7 # number of columns on the board
Black = (0, 0, 0) # RGB for black
Blue = (0, 0, 255) # RGB for blue
Yellow = (255, 255, 0) # RGB for yellow - player token colour
Red = (255, 0, 0) # RGB for red - AI token colour
set_length = 4 # Number of consecutive tokens needed to win
empty_slot = 0 # Value representing an empty slot on the board
player_token = 1 # Value representing the player's token
agent_token = 2 # Value representing the AI's token


 #Creates an empty Connect 4 board. Returns a 2D numpy array initialised to zeros.  
def DrawBoard():       
    return numpy.zeros((Rows_number, Column_number))

#Places a token on the board at the specified row and column.
def PlaceToken(board, row, column, token):  # board: 2D numpy array representing the game board. Row: Row index where the token will be placed
    board[row][column] = token # token: Token value (player_token or agent_token)

#  Checks if a column is valid for placing a token.
def LocationValid(board, column): 
    return board[Rows_number - 1][column] == 0 # column: Column index where the token will be placed

# Finds the next available row in a column.
def NextRow(board, column):
    for row in range(Rows_number):
        if board[row][column] == 0:
            return row

# Checks if a player has won the game.
def Win(board, token):
    # Horizontal
    for c in range(Column_number - 3):
        for r in range(Rows_number):
            if board[r][c] == token and board[r][c+1] == token and board[r][c+2] == token and board[r][c+3] == token:
                return True
    # Vertical
    for c in range(Column_number):
        for r in range(Rows_number - 3):
            if board[r][c] == token and board[r+1][c] == token and board[r+2][c] == token and board[r+3][c] == token:
                return True
    # Diagonal (Right)
    for c in range(Column_number - 3):
        for r in range(Rows_number - 3):
            if board[r][c] == token and board[r+1][c+1] == token and board[r+2][c+2] == token and board[r+3][c+3] == token:
                return True
    # Diagonal (Left)
    for c in range(Column_number - 3):
        for r in range(3, Rows_number):
            if board[r][c] == token and board[r-1][c+1] == token and board[r-2][c+2] == token and board[r-3][c+3] == token:
                return True
    return False

# Heuristic funtion - Evaluates a set of 4 consecutive slots on the board and scores them based on their value.
def CheckBoard(set, token):
# set: List of 4 values from the board
    score = 0
    other_token = player_token if token == agent_token else agent_token
    if set.count(token) == 4:
        score += 100
    elif set.count(token) == 3 and set.count(empty_slot) == 1:
        score += 10
    elif set.count(token) == 2 and set.count(empty_slot) == 2:
        score += 5
    if set.count(other_token) == 3 and set.count(empty_slot) == 1:
        score -= 80
    return score

# Heuristic funtion -  Calculates the overall score of the board for a given token.
def Score(board, token):
    score = 0
    # Vertical
    for c in range(Column_number):
        c_array = [int(i) for i in list(board[:, c])]
        for r in range(Rows_number - 3):
            set = c_array[r:r+set_length]
            score += CheckBoard(set, token)
    # Horizontal
    for r in range(Rows_number):
        r_array = [int(i) for i in list(board[r, :])]
        for c in range(Column_number - 3):
            set = r_array[c:c+set_length]
            score += CheckBoard(set, token)
    # Diagonal (Right)
    for r in range(Rows_number - 3):
        for c in range(Column_number - 3):
            set = [board[r+i][c+i] for i in range(set_length)]
            score += CheckBoard(set, token)
    # Diagonal (Left)
    for r in range(Rows_number - 3):
        for c in range(Column_number - 3):
            set = [board[r+3-i][c+i] for i in range(set_length)]
            score += CheckBoard(set, token)
    return score

# Checks if the game has reached a terminal state. Used in the minimax.
def IsTerminal(board):
    return Win(board, player_token) or Win(board, agent_token) or len(OptionalLocations(board)) == 0

# Implements the MiniMax algorithm with alpha-beta pruning for decision-making.
def MiniMax(board, depth, alpha, beta, max_player): #  max_player: True if it's the maximising player's turn, False otherwise
    locations = OptionalLocations(board)
    terminal_node = IsTerminal(board)
    if depth == 0 or terminal_node:
        if terminal_node:
            if Win(board, agent_token):
                return None, 1000000
            elif Win(board, player_token):
                return None, -1000000
            else:
                return None, 0
        else:
            return None, Score(board, agent_token)
    if max_player:
        value = -math.inf # Initialises the value to negative infinity for the maximising player (AI).
        best_column = random.choice(locations)
        for column in locations:
            row = NextRow(board, column)
            board_copy = board.copy() # board_copy: Creates a deep copy of the current game board to simulate moves without modifying the original board.
            PlaceToken(board_copy, row, column, agent_token)
            new_score = MiniMax(board_copy, depth-1, alpha, beta, False)[1] # Calculates the score of the current move by recursively calling MiniMax. 
            if new_score > value:                                           # The [1] extracts the score from the (column, score) tuple returned by MiniMax.
                value = new_score
                best_column = column # Stores the column index of the best move for the current player.
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_column, value
    else:
        value = math.inf
        best_column = random.choice(locations)
        for column in locations:
            row = NextRow(board, column)
            board_copy = board.copy()
            PlaceToken(board_copy, row, column, player_token)
            new_score = MiniMax(board_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_column = column
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_column, value

# Finds all valid columns where a token can be placed.
def OptionalLocations(board):
    return [col for col in range(Column_number) if LocationValid(board, col)]

def VisualBoard(board):
# Renders the Connect 4 board and tokens on the screen.
    for c in range(Column_number):
        for r in range(Rows_number):
            pygame.draw.rect(screen, Blue, (c*square_size, r*square_size + square_size, square_size, square_size))
            pygame.draw.circle(screen, Black, (int(c*square_size + square_size/2), int(r*square_size + square_size/2 + square_size)), Radius)
    for c in range(Column_number):
        for r in range(Rows_number):
            if board[r][c] == player_token:
                pygame.draw.circle(screen, Yellow, (int(c*square_size + square_size/2), board_height - int(r*square_size + square_size/2)), Radius)
            elif board[r][c] == agent_token:
                pygame.draw.circle(screen, Red, (int(c*square_size + square_size/2), board_height - int(r*square_size + square_size/2)), Radius)
    pygame.display.update()

#  Displays the difficulty selection menu and allows the player to choose Easy or Hard mode.
def DifficultySelection():
    screen.fill(Black)
    font = pygame.font.SysFont("monospace", 50)
    easy_rect = pygame.Rect(board_width // 4 - 100, board_height // 2 - 50, 200, 100)
    hard_rect = pygame.Rect(3 * board_width // 4 - 100, board_height // 2 - 50, 200, 100)
    pygame.draw.rect(screen, Blue, easy_rect)
    pygame.draw.rect(screen, Red, hard_rect)
    easy_label = font.render("Easy", True, Yellow)
    hard_label = font.render("Hard", True, Yellow)
    screen.blit(easy_label, (easy_rect.x + 50, easy_rect.y + 25))
    screen.blit(hard_label, (hard_rect.x + 50, hard_rect.y + 25))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    return 1
                elif hard_rect.collidepoint(event.pos):
                    return 4

# Game Initialisation
pygame.init()
square_size = 100 # Size of each square on the board
Radius = int(square_size/2 - 8) # Radius of the tokens
board_width = Column_number * square_size # Width of the board
board_height = Rows_number * square_size + square_size # Height of the board (including top buffer)
size = (board_width, board_height) # Screen dimensions
screen = pygame.display.set_mode(size) # Initialise the display
depth = DifficultySelection()  # Difficulty Selection

# Displays the winning message in green at the center of the screen.
def DisplayWinnerMessage(message):
    screen.fill(Black)  # Clear the screen
    font = pygame.font.SysFont("monospace", 75)  # Create a font object
    text_surface = font.render(message, True, (0, 255, 0))  # Render the text in green
    text_rect = text_surface.get_rect(center=(board_width // 2, board_height // 2))  # Center the text
    screen.blit(text_surface, text_rect)  # Draw the text on the screen
    pygame.display.update()  # Update the display
    pygame.time.wait(3000)  # Wait for 3 seconds


# Game Loop
board = DrawBoard()
VisualBoard(board)
turn = random.randint(0, 1) # Randomly select which player goes first (0: player, 1: AI)
gameOver = False # Game state flag

# Main game loop: Runs until the game is over
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black, (0, 0, board_width, square_size))
            x_pos = event.pos[0] # Get current mouse position
            if turn == 0:
                pygame.draw.circle(screen, Yellow, (x_pos, square_size//2), Radius)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN: # Detects mouse click for player move
            if turn == 0:
                x_pos = event.pos[0]
                column = x_pos // square_size # Calculate the selected column
                if LocationValid(board, column): # Check if the move is valid
                    row = NextRow(board, column)
                    PlaceToken(board, row, column, player_token)
                    if Win(board, player_token):
                        DisplayWinnerMessage("You Win. Nice!")
                        gameOver = True
                    turn = (turn + 1) % 2 # Switch turn to AI
                    VisualBoard(board) # Update the board display

    if turn == 1 and not gameOver: # AI's turn: Determines and executes the AI's move
        column, _ = MiniMax(board, depth, -math.inf, math.inf, True) # AI chooses the best move using MiniMax
        if LocationValid(board, column):
            row = NextRow(board, column)
            PlaceToken(board, row, column, agent_token) # Place the AI's token
            if Win(board, agent_token):
                DisplayWinnerMessage("AI Agent wins!")
                gameOver = True
            turn = (turn + 1) % 2
            VisualBoard(board)

pygame.time.wait(3000)
