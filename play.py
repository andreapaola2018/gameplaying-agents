# Entry point for our program
import sys

# This method starts the game play
def play(board: list, algorithm: str, param_value: str, next_move_player: str, printMode: str):
    print("in play", algorithm)
    if algorithm == "UR":
        print("in UR")
    return algorithm



def readFromFile(fileName: str) -> (list, str, int, str):
    algorithm = ""
    param_value = 0
    board = []

   # reading the file
    with open(fileName, 'r') as f:
        algorithm = f.readline()  # algorithm name
        print("algirthm", algorithm)
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
    
    print(play(board, algorithm, param_value, next_move_player, printMode))



if __name__ == "__main__":
    main()
