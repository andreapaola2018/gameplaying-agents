# Part 2 - Testing the algorithms against each other
from uniform_random import *
from minimax import *
from monte_carlo import *
from gameState import gameState

def main():
    statistics = getCombinations()

    for item in statistics:
        print(item)
    
        algo1 = item[1]
        param1 = item[2]
        player1 = item[3]
        
        algo2 = item[5]
        param2 = item[6]
        player2= item[7]
        
        gameOutcome = playGame(algo1=algo1, param1=param1, player1=player1, algo2=algo2, param2=param2, player2=player2)
        print(gameOutcome)
        
        if gameOutcome == 0: # draw
            item[9] += 1
        elif gameOutcome == -1: # red won
            item[4] += 1
        else: # yellow won
            item[8] += 1
        
        print(item)
        break

def getCombinations():
    # algorithms = [["UR", 0], ["DLMM", 5], ["PMCGS500", 500], ["PMCGS10000", 10000], ["UCT500", 500], ["UCT10000", 10000]]
    algorithms = [["PMCGS500", 500], ["PMCGS10000", 10000], ["UCT500", 500], ["UCT10000", 10000]]
    # algorithms = ["UR", "DLMM", "PMCGS500", "PMCGS10000", "UCT500", "UCT10000"]
    statistics = []
    # make all 36 combinations of algorithms that we want to test
    for i in range(len(algorithms)):
        for j in range(len(algorithms)):
            algo1 = algorithms[i][0]
            algo2 = algorithms[j][0]
            param1 = algorithms[i][1]
            param2 = algorithms[j][1]
            test = [algo1 + " vs " + algo2, algo1, param1, "R", 0, algo2, param2, "Y", 0, 0]
            statistics.append(test)
    
    return statistics


def playGame(algo1, param1, player1, algo2, param2,  player2) -> str:
    board = getEmptyBoard()
    game = gameState(board)
    printMode = "none"

    while game.gameOutcome is None:
        # Algorithm 1's turn
        if "PMCGS" in algo1:
            move = monteCarloTreeSearch(game, param1, player1, printMode)
            print("Before reset:")
            game.printBoard()
            game.resetToOriginalState()
            print("After reset:")
            game.printBoard()
            
            game.checkGameStatus(move.coordinates, player1)
            if game.gameOutcome == -1:
                print("Winning move: ", move.coordinates)
            # if game.gameOutcome == 0:  # draw
            #     return "Draw", None
            # if wasWinningMove(game.gameOutcome, player1):
            #     return algo1, player1

        elif "UCT" in algo1:
            move = monteCarloTreeSearch(game, param1, player1, printMode, True)
            # if game.gameOutcome == 0:  # draw
            #     return "Draw", None
            # if wasWinningMove(game.gameOutcome, player1):
            #     return algo1, player1

        if game.gameOutcome is not None:
            return game.gameOutcome
        
        # Algorithm 2's turn
        if "PMCGS" in algo2:
            move = monteCarloTreeSearch(game, param2, player2, printMode)
            print("Before reset:")
            game.printBoard()
            game.resetToOriginalState()
            print("After reset:")
            game.printBoard()
            game.checkGameStatus(move.coordinates, player2)
            if game.gameOutcome == 1:
                print("Winning move: ", move.coordinates)
            # if game.gameOutcome == 0:  # draw
            #     return "Draw", None
            # if wasWinningMove(gameStatus, player2):
            #     return algo2, player2

        elif "UCT" in algo2:
            move = monteCarloTreeSearch(game, param2, player2, printMode, True)
            # if gameStatus == 0:  # draw
            #     return "Draw", None
            # if wasWinningMove(gameStatus, player2):
            #     return algo2, player2
        
    
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

def wasWinningMove(gameStatus, nextMovePlayer) -> bool:
    if (gameStatus == -1 and nextMovePlayer == "R") or (gameStatus == 1 and nextMovePlayer == "Y"):
        return True
    return False

def printBoard(board):
    for row in board:
        print(row)


if __name__ == "__main__":
    main()