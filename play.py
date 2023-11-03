# Entry point for our program
import sys
from node import Node

# This method starts the game play
def play(board: list, algorithm: str, param_value: str, next_move_player: str, printMode: str):
    if algorithm == "UR":
        print("in UR")
    return algorithm

def printBoard(board: list):
    for row in board:
        print(row)

def readFromFile(fileName: str) -> (list, str, int, str):
    algorithm = ""
    param_value = 0
    board = []

   # reading the file
    with open(fileName, 'r') as f:
        algorithm = f.readline()  # algorithm name
        param_value = f.readline()  # parameter value
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
    print("Original Board:")
    printBoard(board)
    print("\n\n")
    
    # test Node class:
    root = Node(board, next_move_player)
    root.generateChildren()
    root.printChildrenNodes()
    
    print("\nOriginal Board Again:")
    printBoard(root.board)
    
    play(board, algorithm, param_value, next_move_player, printMode)



if __name__ == "__main__":
    main()
