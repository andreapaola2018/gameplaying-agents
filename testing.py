from uniform_random import *
from minimax import *
from monte_carlo import *

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
        
        winAlgo, winPlayer = playGame(algo1=algo1, param1=param1, player1=player1, algo2=algo2, param2=param2, player2=player2)
        print(winAlgo)
        print(winPlayer)
        
        if winAlgo == "Draw":
            item[9] += 1
        elif algo1 == algo2:
            if winPlayer == player1:
                item[4] += 1
            else:
                item[8] += 1
        else:
            if winAlgo == algo1:
                item[4] += 1
            else:
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
    board = [["O"]*7]*6
    printMode = "none"
    gameStatus = None

    while gameStatus is None:
        # Algorithm 1's turn
        if "PMCGS" in algo1:
            move = monteCarloTreeSearch(board, param1, player1, printMode)
            board = move.board
            gameStatus = move.checkGameStatus()
            if gameStatus == 0:  # draw
                return "Draw", None
            if wasWinningMove(gameStatus, player1):
                return algo1, player1

        elif "UCT" in algo1:
            move = monteCarloTreeSearch(board, param1, player1, printMode, True)
            board = move.board
            gameStatus = move.checkGameStatus()
            if gameStatus == 0:  # draw
                return "Draw", None
            if wasWinningMove(gameStatus, player1):
                return algo1, player1

        
        # Algorithm 2's turn
        if "PMCGS" in algo2:
            move = monteCarloTreeSearch(board, param2, player2, printMode)
            board = move.board
            gameStatus = move.checkGameStatus()
            if gameStatus == 0:  # draw
                return "Draw", None
            if wasWinningMove(gameStatus, player2):
                return algo2, player2

        elif "UCT" in algo2:
            move = monteCarloTreeSearch(board, param2, player2, printMode, True)
            board = move.board
            gameStatus = move.checkGameStatus()
            if gameStatus == 0:  # draw
                return "Draw", None
            if wasWinningMove(gameStatus, player2):
                return algo2, player2


def wasWinningMove(gameStatus, nextMovePlayer) -> bool:
    if (gameStatus == -1 and nextMovePlayer == "R") or (gameStatus == 1 and nextMovePlayer == "Y"):
        return True
    return False

def printBoard(board):
    for row in board:
        print(row)


if __name__ == "__main__":
    main()