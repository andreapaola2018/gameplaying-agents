# PART 2: ENHANCEMENT #1
from uniform_random import *
from minimax import *
from monte_carlo import *
from gameState import gameState
import sys

def main():
    print("Setting up your game...")
    algorithm = sys.argv[1]
    
    outcome = playGame(algorithm)
    if outcome == -1:
        print("You won!")
    elif outcome == 1:
        print("Game over! You lost!")
    else:
        print("It's a tie!")

def playGame(algorithm) -> str:
    board = getEmptyBoard()
    game = gameState(board)
    print("Game ready! You are player 'Red'!")
    game.printBoard()

    while game.gameOutcome is None:
        # Player's turn
        validMove = False
        legalMoves = game.getLegalMoves()
        playerMove = []
        while not validMove:
            col = int(input("Input a column number (1-7) to place your tile in: "))
            col -= 1
            for move in legalMoves:
                if col == move[1]:
                    validMove = True
                    playerMove = move
            print("Invalid column. Please try again.")
        
        print("Great move! Here is the current board:")
        game.makeMove(playerMove, "R")
        game.resetToOriginalState()
        game.printBoard()
        
        game.checkGameStatus(playerMove, "R")
        
        if game.gameOutcome is not None:
            return game.gameOutcome
        
        print("It is now player 2's turn.")
        print("Player 2 is thinking...")
        
        # AI's turn
        AImove = None
        if algorithm == "DLMM":
            # TODO
            pass
        elif algorithm == "PMCGS":
            AImove = monteCarloTreeSearch(game, 10000, "Y", "none")
        elif algorithm == "UCT":
            AImove = monteCarloTreeSearch(game, 10000, "Y", "none", True)

        print("Player 2 made their move, here is the updated board:")
        game.resetToOriginalState()
        game.printBoard()
        
        game.checkGameStatus(AImove.coordinates, "Y")

    return game.gameOutcome

def getEmptyBoard():
    fileName = "emptyBoard.txt"
    board = []

   # reading the file
    with open(fileName, 'r') as f:
        # reading through all the map coordinates and saving as a 2D list
        for _, line in enumerate(f):
            letters = [l for l in line.strip()]
            board.append(letters)

    return board


if __name__ == "__main__":
    main()
