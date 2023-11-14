# Entry point for our program
import sys
from gameState import gameState
from uniform_random import *
from minimax import *
from node import Node
from monte_carlo import *
from mcts_node import *
from PrettyPrint import PrettyPrintTree

# This method starts the game play
def play(game: gameState, algorithm: str, paramValue: int, nextMovePlayer: str, printMode: str):
    print(algorithm)
    if algorithm == "UR":
        uniform_random(game, nextMovePlayer, printMode)
    elif algorithm == "PMCGS":
        move = monteCarloTreeSearch(game, paramValue, nextMovePlayer, printMode)
        print("FINAL Move selected: ", move.coordinates[1]+1)
    elif algorithm == "UCT":
        move = monteCarloTreeSearch(game, paramValue, nextMovePlayer, printMode, True)
        print("FINAL Move selected: ", move.coordinates[1]+1)
    elif algorithm == "DLMM": 
        print("****Depth-Limited Minimax with Alpha-Beta Pruning****")
        DLMM(board, paramValue, nextMovePlayer, True)

        print("\n****Depth-Limited Minimax****")
        DLMM(board, paramValue, nextMovePlayer, False)


        
# def printTreeMcts(root: MonteCarloNode):

#         monteCarloTreeSearch(board, paramValue, nextMovePlayer, printMode, True)
    
                
# def printTree(root: Node):

#     pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val())
#     pt(root)
        # root node with the initial game state
        root = MiniMaxNode(game, 'Y', True, paramValue)

        # Evaluate immediate moves and select the final move
        final_move = root.evaluate_immediate_moves(1)  # Assuming depth 1 for immediate moves
        
def printTree(root: Node):
    pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val())
    pt(root)

def printBoard(board: list):
    for row in board:
        print(row)

def readFromFile(fileName: str) -> (list, str, int, str):
    algorithm = ""
    param_value = 0
    board = []

   # reading the file
    with open(fileName, 'r') as f:
        algorithm = f.readline().strip()  # algorithm name
        param_value = int(f.readline().strip()) # parameter value
        next_move_player = f.readline().strip()  # player who will make the next move

        # reading through all the map coordinates and saving as a 2D list
        for _, line in enumerate(f):
            letters = [l for l in line.strip()]
            board.append(letters)
            
    return board, algorithm, param_value, next_move_player

# main method
def main():
    # PART 1: Please comment this section out in order to run PART 2
    fileName = sys.argv[1]
    printMode = sys.argv[2]
    
    board, algorithm, paramValue, nextMovePlayer = readFromFile(fileName)
    game = gameState(board)
    
    play(game, algorithm, paramValue, nextMovePlayer, printMode.lower())

if __name__ == "__main__":
    main()