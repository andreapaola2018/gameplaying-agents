# Part 2 - Testing the algorithms against each other
from uniform_random import *
from minimax import *
from monte_carlo import *
from gameState import gameState

def main():
    statistics = getCombinations()

    for item in statistics:
        algo1 = item[1]
        param1 = item[2]
        player1 = item[3]

        algo2 = item[5]
        param2 = item[6]
        player2 = item[7]
        
        for _ in range(100):
            gameOutcome = playGame(algo1=algo1, param1=param1, player1=player1, algo2=algo2, param2=param2, player2=player2)            
            if gameOutcome == 0: # draw
                item[9] += 1
            elif gameOutcome == -1: # red won
                item[4] += 1
            else: # yellow won
                item[8] += 1

        print(item)

def getCombinations():
    #algorithms = [["UR", 0], ["DLMM", 5], ["PMCGS500", 500], ["PMCGS1000", 1000], ["UCT500", 500], ["UCT1000", 1000]]
    algorithms = [["UR", 0], ["PMCGS500", 500], ["PMCGS10000", 1000], ["UCT500", 500], ["UCT10000", 1000]]
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
    gameOutcome = None

    while gameOutcome is None:
        # Algorithm 1's turn
        if algo1 == "UR":
            node = uniform_random(board, player1, printMode)
            board = node.board
            gameOutcome = node.checkGameStatus()
            if gameOutcome is not None:
                return gameOutcome
        elif algo1 == "DLMM":
            _, move, board = DLMM(board, param1, player1, True)
            node = MiniMaxNode(board, player1, True, 5)
            node.coordinates = move
            gameOutcome = node.checkGameStatus()
            if gameOutcome is not None:
                return gameOutcome
            
        elif "PMCGS" in algo1:
            move = monteCarloTreeSearch(game, param1, player1, printMode)
            game.resetToOriginalState()
            game.checkGameStatus(move.coordinates, player1)
            if game.gameOutcome is not None:
                return game.gameOutcome
        elif "UCT" in algo1:
            move = monteCarloTreeSearch(game, param1, player1, printMode, True)
            game.resetToOriginalState()
            game.checkGameStatus(move.coordinates, player1)
            if game.gameOutcome is not None:
                return game.gameOutcome
        
        # Algorithm 2's turn
        if algo2 == "UR":
           node = uniform_random(board, player2, printMode)
           board = node.board
           gameOutcome = node.checkGameStatus()
           if gameOutcome is not None:
                return gameOutcome
        elif algo2 == "DLMM":
            _, move, board = DLMM(board, param2, player2, True)
            node = MiniMaxNode(board, player2, True, 5)
            node.coordinates = move
            gameOutcome = node.checkGameStatus()
            if gameOutcome is not None:
                return gameOutcome
        elif "PMCGS" in algo2:
            move = monteCarloTreeSearch(game, param2, player2, printMode)
            game.resetToOriginalState()
            gameOutcome = game.checkGameStatus(move.coordinates, player2)
        elif "UCT" in algo2:
            move = monteCarloTreeSearch(game, param2, player2, printMode, True)
            game.resetToOriginalState()
            gameOutcome = game.checkGameStatus(move.coordinates, player2)

        
    return gameOutcome

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

if __name__ == "__main__":
    main()