import pygame
import sys
import random

##=== DECLARATIONS AND INITILZATIONS ===##

pygame.init()

# setting up screen
WIDTH = 900
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Unbeatable TTT | The Second Edition")

BG_COLOR = (214, 201, 227)

# assets
boardImg = pygame.image.load("assets/Board.png")
Ximg = pygame.image.load("assets/X.png")
Oimg = pygame.image.load("assets/O.png")

Xturn = pygame.image.load("assets/X.png")
Xturn = pygame.transform.scale(Xturn, (50, 50))

Oturn = pygame.image.load("assets/O.png")
Oturn = pygame.transform.scale(Oturn, (50, 50))

# brd stuffz
board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
graphical_board = [[[None, None], [None, None], [None, None]],
                   [[None, None], [None, None], [None, None]],
                   [[None, None], [None, None], [None, None]]]

# player in this case is the computer, while opponent is the person playing against computer
player = 'X'
opponent = 'O'

#== INITIAL SETTUP ==#

screen.fill(BG_COLOR)
screen.blit(boardImg, (64, 64))

# starting player
if random.randint(0, 1):
    activePlayer = 'O'
else:
    activePlayer = 'X'
print(activePlayer)
# tell person who starts
if activePlayer == 'X':
    print("X's Turn")
    screen.blit(Xturn, Xturn.get_rect(center=(450, 865)))
if activePlayer == 'O':
    print("O's Turn")
    screen.blit(Oturn, Oturn.get_rect(center=(450, 865)))

pygame.display.update()

game_finished = False

##=== GAME FUNCTION FUNCTIONS ===##

def renderBoard(board, Ximg, Oimg):
    print("rendering this brd:")
    print(board)

    global graphical_board
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                graphical_board[i][j][0]  = Ximg
                graphical_board[i][j][1]  = Ximg.get_rect(center = (j * 300 + 150, i * 300 + 150))
            elif board[i][j] == 'O':
                graphical_board[i][j][0]  = Oimg
                graphical_board[i][j][1]  = Oimg.get_rect(center = (j * 300 + 150, i * 300 + 150))

    for i in range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                screen.blit(graphical_board[i][j][0], graphical_board[i][j][1])

def newSymbol(board, graphical_board, activePlayer):
    print("New Symbol Time")
    current_pos = pygame.mouse.get_pos()
    scaledX = (current_pos[0]-65) / 835 * 2
    scaledY = current_pos[1] / 835 * 2
    if board[round(scaledY)][round(scaledX)] != 'O' and board[round(scaledY)][round(scaledX)] != 'X':
        board[round(scaledY)][round(scaledX)] = activePlayer
        activePlayer = 'X'

    print("calling render")
    renderBoard(board, Ximg, Oimg)

    return board, activePlayer

def checkWin(board):
    winner = None
    for row in range(0, 3):
        if ((board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None)):
            winner = board[row][0]
            for i in range(0, 3):
                graphical_board[row][i][0] = pygame.image.load(f"assets/Winning {winner}.png")
                screen.blit(graphical_board[row][i][0], graphical_board[row][i][1])
            pygame.display.update()
            return winner

    for col in range(0, 3):
        if ((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)):
            winner = board[0][col]
            for i in range(0, 3):
                graphical_board[i][col][0] = pygame.image.load(f"assets/Winning {winner}.png")
                screen.blit(graphical_board[i][col][0], graphical_board[i][col][1])
            pygame.display.update()
            return winner

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        graphical_board[0][0][0] = pygame.image.load(f"assets/Winning {winner}.png")
        screen.blit(graphical_board[0][0][0], graphical_board[0][0][1])
        graphical_board[1][1][0] = pygame.image.load(f"assets/Winning {winner}.png")
        screen.blit(graphical_board[1][1][0], graphical_board[1][1][1])
        graphical_board[2][2][0] = pygame.image.load(f"assets/Winning {winner}.png")
        screen.blit(graphical_board[2][2][0], graphical_board[2][2][1])
        pygame.display.update()
        return winner

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner = board[0][2]
        graphical_board[0][2][0] = pygame.image.load(f"assets/Winning {winner}.png")
        screen.blit(graphical_board[0][2][0], graphical_board[0][2][1])
        graphical_board[1][1][0] = pygame.image.load(f"assets/Winning {winner}.png")
        screen.blit(graphical_board[1][1][0], graphical_board[1][1][1])
        graphical_board[2][0][0] = pygame.image.load(f"assets/Winning {winner}.png")
        screen.blit(graphical_board[2][0][0], graphical_board[2][0][1])
        pygame.display.update()
        return winner

    if winner is None:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    return None
        return "DRAW"

##=== COMPUTER ALGORITHIM (MINIMAX) ===##

emptyBoard = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

def isNotFull(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == emptyBoard[i][j]:
                return True
    return False

def scoreBoard(brd):
    # win on row
    for i in range(3):
        if brd[i][0] == brd[i][1] and brd[i][1] == brd[i][2]:
            if brd[i][0] == player:
                return 10
            elif brd[i][0] == opponent:
                return -10
    # win on col
    for i in range(3):
        if brd[0][i] == brd[1][i] and brd[1][i] == brd[2][i]:
            if brd[0][i] == player:
                return 10
            elif brd[0][i] == opponent:
                return -10
    # win on diagnoals
    if brd[0][0] == brd[1][1] and brd[1][1] == brd[2][2]:
        if brd[0][0] == player:
            return 10
        elif brd[0][0] == opponent:
            return -10
    if brd[0][2] == brd[1][1] and brd[1][1] == brd[2][0]:
        if brd[0][2] == player:
            return 10
        elif brd[0][2] == opponent:
            return -10
    # if no one wins than be sad
    return 0

def minimax(board, depth, isMax):
    # print("Calculating")

    score = scoreBoard(board)

    if score == 10 or score == -10:
        return score
    if not isNotFull(board):
        return 0

    if isMax:
        best = -1000

        for i in range(3):
            for j in range(3):
                if board[i][j] == emptyBoard[i][j]:
                    board[i][j] = player
                    best = max(best, minimax(board, depth+1, not isMax))

                    board[i][j] = emptyBoard[i][j]
        return best

    else:
        best = 1000

        for i in range(3):
            for j in range(3):
                if board[i][j] == emptyBoard[i][j]:
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, not isMax))

                    board[i][j] = emptyBoard[i][j]
        return best

def bestMove(board):
    best = -1000
    pos = [-1, -1]

    for i in range(3):
        for j in range(3):
            if board[i][j] == emptyBoard[i][j]:
                board[i][j] = player

                move = minimax(board, 0, False)

                board[i][j] = emptyBoard[i][j]

                if move > best:
                    pos = [i, j]
                    best = move

    return pos

##=== IN GAME CODE ===#

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # print(activePlayer)

        if activePlayer == 'X':
            print()
            print("X is going to choose at this brd state")
            print(board)
            bestPos = bestMove(board)
            if board[bestPos[0]][bestPos[1]] != 'O' and board[bestPos[0]][bestPos[1]] != 'X':
                board[bestPos[0]][bestPos[1]] = activePlayer
                activePlayer = 'O'

                renderBoard(board, Ximg, Oimg)

            if game_finished and pygame.MOUSEBUTTONDOWN:
                board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                graphical_board = [[[None, None], [None, None], [None, None]],
                                   [[None, None], [None, None], [None, None]],
                                   [[None, None], [None, None], [None, None]]]

                if random.randint(0, 1):
                    activePlayer = 'O'
                else:
                    activePlayer = 'X'
                print(activePlayer)

                screen.fill(BG_COLOR)
                screen.blit(boardImg, (64, 64))

                game_finished = False

                pygame.display.update()

            if checkWin(board) is not None:
                game_finished = True

            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and activePlayer == 'O':
            print()
            print("O chose something")
            board, activePlayer = newSymbol(board, graphical_board, activePlayer)

            if game_finished:
                board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                graphical_board = [[[None, None], [None, None], [None, None]],
                                   [[None, None], [None, None], [None, None]],
                                   [[None, None], [None, None], [None, None]]]

                screen.fill(BG_COLOR)
                screen.blit(boardImg, (64, 64))

                # starting player
                if random.randint(0, 1):
                    activePlayer = 'O'
                else:
                    activePlayer = 'X'
                print(activePlayer)
                # tell person who starts
                if activePlayer == 'X':
                    print("X's Turn")
                    screen.blit(Xturn, Xturn.get_rect(center=(450, 865)))
                if activePlayer == 'O':
                    print("O's Turn")
                    screen.blit(Oturn, Oturn.get_rect(center=(450, 865)))

                pygame.display.update()

                game_finished = False

            if checkWin(board) is not None:
                game_finished = True

            pygame.display.update()