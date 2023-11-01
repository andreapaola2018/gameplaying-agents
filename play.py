# Entry point for our program
import sys

# This method starts the game play
def play(board: list, algorithm: str, param_value: str, next_move_player: str, printMode: str):
    if algorithm == "UR":
        # TODO
        pass
    elif algorithm == "DLMM":
        # TODO
        pass
    elif algorithm == "PMCGS":
        # TODO
        pass
    elif algorithm == "UCT":
        # TODO
        pass


def readFromFile(fileName: str) -> (list, str, str, str):
    algorithm = ""
    param_value = 0
    board = []

   # reading the file
    with open('board.txt', 'r') as f:
        algorithm = f.readline()  # algorithm name
        param_value = f.readline()  # parameter value
        next_move_player = f.readline()  # player who will make the next move

        # reading through all the map coordinates and saving as a 2D list
        for _, line in enumerate(f):
            strLine = line.split(' ')
            board.append(strLine)

    return board, algorithm, param_value, next_move_player


# main method
def main():
    fileName = sys.argv[1]
    printMode = sys.argv[2]
    
    board, algorithm, param_value, next_move_player = readFromFile(fileName)
    
    play(board, algorithm, param_value, next_move_player, printMode)
