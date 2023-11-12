# Entry point for our program
import sys
from uniform_random import *
from minimax import *
from node import Node
from mcts_node import MonteCarloNode
from monte_carlo import *
from PrettyPrint import PrettyPrintTree

# This method starts the game play
def play(board: list, algorithm: str, paramValue: int, nextMovePlayer: str, printMode: str):
    print(algorithm)
    if algorithm == "UR":
        uniform_random(board, nextMovePlayer, printMode)
    elif algorithm == "PMCGS":
        monteCarloTreeSearch(board, paramValue, nextMovePlayer, printMode)
        # root = Node(board, "Y" if nextMovePlayer == "R" else "R")
        # root.generateChildren(nextMovePlayer)
        # print("Root's children:")
        # root.printChildrenNodes()
        # child = selectChildNode(root)
        # print("Selected child:")
        # print(child)
        # # print("Expanding child...")
        # expand(child)
        # # child.printChildrenNodes()
        # # print("Performing roll out...")
        # leaf, gameStatus = rollOut(child, nextMovePlayer)
        # print("Game status: ", gameStatus)
        # print(leaf)
        # backPropagate(leaf, gameStatus, nextMovePlayer)
        
        # child = selectChildNode(root)
        # expand(child)
        # leaf, gameStatus = rollOut(child, nextMovePlayer)
        # backPropagate(leaf, gameStatus, nextMovePlayer)
        # print("Game status: ", gameStatus)
        # print(leaf)
        
        # printTree(root)
    elif algorithm == "UCT":
        monteCarloTreeSearch(board, paramValue, nextMovePlayer, printMode, True)
    elif algorithm == "DLMM": 
        # root node with the initial game state
        root = MiniMaxNode(board, 'Y', True, paramValue)

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
    fileName = sys.argv[1]
    printMode = sys.argv[2]
    
    board, algorithm, param_value, next_move_player = readFromFile(fileName)
    
    play(board, algorithm, param_value, next_move_player, printMode)

if __name__ == "__main__":
    main()