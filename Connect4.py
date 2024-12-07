import random
import pygame
import sys
import math
import numpy

# Constants
Rows_number = 6
Column_number = 7
Black = (0, 0, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Red = (255, 0, 0)
set_length = 4
empty_slot = 0
player_token = 1
agent_token = 2

# Helper Functions
def DrawBoard():
    return numpy.zeros((Rows_number, Column_number))

def PlaceToken(board, row, column, token):
    board[row][column] = token

def LocationValid(board, column):
    return board[Rows_number - 1][column] == 0

def NextRow(board, column):
    for row in range(Rows_number):
        if board[row][column] == 0:
            return row

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

def CheckBoard(set, token):
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

def IsTerminal(board):
    return Win(board, player_token) or Win(board, agent_token) or len(OptionalLocations(board)) == 0

def MiniMax(board, depth, alpha, beta, max_player):
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
        value = -math.inf
        best_column = random.choice(locations)
        for column in locations:
            row = NextRow(board, column)
            board_copy = board.copy()
            PlaceToken(board_copy, row, column, agent_token)
            new_score = MiniMax(board_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_column = column
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

def OptionalLocations(board):
    return [col for col in range(Column_number) if LocationValid(board, col)]

def VisualBoard(board):
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
                    return 5

# Game Initialization
pygame.init()
square_size = 100
Radius = int(square_size/2 - 8)
board_width = Column_number * square_size
board_height = Rows_number * square_size + square_size
size = (board_width, board_height)
screen = pygame.display.set_mode(size)

# Difficulty Selection
depth = DifficultySelection()

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
turn = random.randint(0, 1)
gameOver = False

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black, (0, 0, board_width, square_size))
            x_pos = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, Yellow, (x_pos, square_size//2), Radius)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == 0:
                x_pos = event.pos[0]
                column = x_pos // square_size
                if LocationValid(board, column):
                    row = NextRow(board, column)
                    PlaceToken(board, row, column, player_token)
                    if Win(board, player_token):
                        DisplayWinnerMessage("You Win. Nice!")
                        gameOver = True
                    turn = (turn + 1) % 2
                    VisualBoard(board)

    if turn == 1 and not gameOver:
        column, _ = MiniMax(board, depth, -math.inf, math.inf, True)
        if LocationValid(board, column):
            row = NextRow(board, column)
            PlaceToken(board, row, column, agent_token)
            if Win(board, agent_token):
                DisplayWinnerMessage("AI Agent wins!")
                gameOver = True
            turn = (turn + 1) % 2
            VisualBoard(board)

pygame.time.wait(3000)
