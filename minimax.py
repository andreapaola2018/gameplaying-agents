import math
import random
from gameState import gameState
class MiniMaxNode:
    def __init__(self, board, player, maximizingPlayer, depth, parent=None):
        self.board: list = board
        self.player = player
        self.parent = parent
        self.depth = depth
        self.maximizingPlayer = maximizingPlayer
        self.coordinates = []  # to store the coordinates of the current move made
        self.children: list[MiniMaxNode] = []  # List to store child nodes

    def __str__(self):
        return "Coordinates: " + ((str(self.coordinates[0]) + " " + str(self.coordinates[1])) if (len(self.coordinates) == 2) else "") + "\n" + self.__boardFormatted()

    def __boardFormatted(self) -> str:
        if self.board is None:
            return "No board!"
        b = ""
        for row in self.board:
            b += "["
            for i in range(7):
                b += "'" + row[i] + ("', " if i < 6 else "'")
            b += "]\n"
        return b

    #Generates up to 7 children nodes which represent possible moves for the next player
    def generateChildren(self, nextMovePlayer: str, maximizingPlayer, depth):
        for i in range(7):  # check all 7 columns in board
            if not self.__isColumnFull(i):
                coordinates = self.__getCoordinatesForColumn(i)
                if coordinates:  # if column is not full, generate a child
                    maximizingPlayer_for_opponent = not self.maximizingPlayer  # Opponent's turn
                    child = MiniMaxNode(
                        self.board, nextMovePlayer, maximizingPlayer_for_opponent, depth, parent=None)
                    child.coordinates = self.__getCoordinatesForColumn(i)
                    self.__generateBoardForChild(child)
                    self.children.append(child)
                    # Generate children for the opponent's subsequent moves
                    if depth > 1:  # Considering the depth limit
                        child.generateChildren(
                            "R" if nextMovePlayer == "Y" else "Y", maximizingPlayer_for_opponent, depth - 1)
                            
    # Checks the current state of the board to see if the move made is a win, loss, or neither move
    def checkGameStatus(self) -> str:

        if len(self.coordinates) < 2:
            return None  # Coordinates are not available, can't determine game status
        row = self.coordinates[0]
        col = self.coordinates[1]
        playerTile = self.player

        # check horizontal
        rightCount = 0
        leftCount = 0
        right = col+1
        left = col-1
        while right < 7 and self.board[row][right] == playerTile:  # count right
            rightCount += 1
            right += 1
        while left >= 0 and self.board[row][left] == playerTile:  # count left
            leftCount += 1
            left -= 1
        total = rightCount + leftCount + 1
        if total >= 4:
            # if Red won -> return -1, if Yellow won -> return 1
            return -1 if self.player == "R" else 1

        # check vertical
        upCount = 0
        downCount = 0
        up = row-1
        down = row+1
        while down < 6 and self.board[down][col] == playerTile:  # count down
            downCount += 1
            down += 1
        while up >= 0 and self.board[up][col] == playerTile:  # count up
            upCount += 1
            up -= 1
        total = downCount + upCount + 1
        if total >= 4:
            # if Red won -> return -1, if Yellow won -> return 1
            return -1 if self.player == "R" else 1

        # check top left to bottom right diagonal
        upLeftCount = 0
        downRightCount = 0
        up = row-1
        left = col-1
        down = row+1
        right = col+1
        # count upLeft
        while up >= 0 and left >= 0 and self.board[up][left] == playerTile:
            upLeftCount += 1
            left -= 1
            up -= 1
        # count downRight
        while down < 6 and right < 7 and self.board[down][right] == playerTile:
            downRightCount += 1
            right += 1
            down += 1
        total = upLeftCount + downRightCount + 1
        if total >= 4:
            # if Red won -> return -1, if Yellow won -> return 1
            return -1 if self.player == "R" else 1

        # check top right to bottom left diagonal
        upRightCount = 0
        downLeftCount = 0
        up = row-1
        right = col+1
        down = row+1
        left = col-1
        # count upRight
        while up >= 0 and right < 7 and self.board[up][right] == playerTile:
            upRightCount += 1
            right += 1
            up -= 1
        # count downLeft
        while down < 6 and left >= 0 and self.board[down][left] == playerTile:
            downLeftCount += 1
            left -= 1
            down += 1
        total = upRightCount + downLeftCount + 1
        if total >= 4:
            # if Red won -> return -1, if Yellow won -> return 1
            return -1 if self.player == "R" else 1

        # Check if board is full
        for row in self.board:
            if "O" in row:  # Not full, therefore not a draw
                # return None, meaning there are still moves left that can be made
                return None

        # If board was full, then it was a draw since there were no winners
        return 0

    # Will generate a new, updated board for the child, with the tile played by the player in the appropriate coordinates
    def __generateBoardForChild(self, child):
        childBoard = []
        for row in self.board:
            letters = []
            for l in row:
                letters.append(l)
            childBoard.append(letters)
        childBoard[child.coordinates[0]][child.coordinates[1]] = child.player
        child.board = childBoard

    # Given a column index, will first check if that column is full (as in no more tiles can be put in that column)
    # If full, returns None. If not full, will return the coordinates of the next position in which a tile fits.
    def __getCoordinatesForColumn(self, colIndex):
        if self.__isColumnFull(colIndex):
            return None
        for i in range(5, 0, -1):
            if self.board[i][colIndex] == "O":  # empty spot
                return [i, colIndex]

    # Helper method that returns true if a column for a given index is full, false otherwise
    def __isColumnFull(self, colIndex) -> bool:
        if self.board[0][colIndex] == "O":  # if it's an O, column is not full
            return False
        return True

    def minimax(self, depth):
        game_result = self.checkGameStatus()
        if depth == 0 or game_result is not None:
            # game is not over
            if game_result is None:
                # return heuristic and no selected move for non-terminal states
                return self.heuristic_evaluation(), None
            return game_result, None

        if self.maximizingPlayer:
            max_eval = float('-inf')
            selected_move = None
            for child in self.children:
                eval, _ = child.minimax(depth - 1)
                if eval > max_eval:
                    max_eval = eval
                    selected_move = child.coordinates[1]
            return max_eval, selected_move + 1 if selected_move is not None else None
        else:
            min_eval = float('inf')
            selected_move = None
            for child in self.children:
                eval, _ = child.minimax(depth - 1)
                if eval < min_eval:
                    min_eval = eval
                    selected_move = child.coordinates[1]
            return min_eval, selected_move + 1 if selected_move is not None else None

    def minimax_alpha_beta(self, depth, alpha, beta):   
        game_result = self.checkGameStatus()
        
        if depth == 0 or game_result is not None:
            # game is not over
            if game_result is None:
                ##return heuristic and no selected move for non-terminal states
                return self.heuristic_evaluation(), None
            return game_result, None 

        if self.maximizingPlayer:
            max_eval = float('-inf')
            selected_move = None 
            for child in self.children:
                eval, _ = child.minimax_alpha_beta(depth - 1, alpha, beta)
                if eval > max_eval: 
                    max_eval = eval
                    selected_move = child.coordinates[1]
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, selected_move + 1 if selected_move is not None else None
        else:
            min_eval = float('inf')
            selected_move = None
            for child in self.children:
                eval, _ = child.minimax_alpha_beta(depth - 1, alpha, beta)
                if eval < min_eval: 
                    min_eval = eval
                    selected_move = child.coordinates[1]
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, selected_move + 1 if selected_move is not None else None

    def heuristic_evaluation(self):
        player = self.player
        opponent = "Y" if player == "R" else "R"

        # Check lines of 2 and 3 pieces for the current player
        player_lines_2 = self.count_lines_of_length(2, player)
        player_lines_3 = self.count_lines_of_length(3, player)

        # Check lines for the opponent
        opponent_lines_2 = self.count_lines_of_length(2, opponent)
        opponent_lines_3 = self.count_lines_of_length(3, opponent)

        # Calculate heuristic
        player_score = player_lines_2 + 2 * player_lines_3
        opponent_score = opponent_lines_2 + 2 * opponent_lines_3

        # Normalize scores and return a value between -1 and 1
        total_score = player_score - opponent_score
        max_possible_score = 2 * (self.count_lines_of_length(3, "R") +
             self.count_lines_of_length(3, "Y"))
        heuristic_value = (
            total_score / max_possible_score) if max_possible_score != 0 else 0
        return heuristic_value

    def count_lines_of_length(self, length, player):
        lines = 0

        # Check rows
        for row in range(6):
            for col in range(4):
                line = self.board[row][col:col + length]
                # Check if the line contains the player's pieces
                if all(tile == player for tile in line):
                    lines += 1

        # Check columns
        for col in range(7):
            for row in range(3):
                line = [self.board[row + i][col] for i in range(length)]
                if all(tile == player for tile in line):
                    lines += 1

        # Check diagonals (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                line = [self.board[row + i][col + i] for i in range(length)]
                if all(tile == player for tile in line):
                    lines += 1

        # Check diagonals (top-right to bottom-left)
        for row in range(3):
            for col in range(3, 7):
                line = [self.board[row + i][col - i] for i in range(length)]
                if all(tile == player for tile in line):
                    lines += 1
        return lines
    
    
    def output(self): 

        for child in self.children:
            eval = child.heuristic_evaluation()
            print(f"Column {child.coordinates[1] + 1}: {eval}" if eval is not None else f"Column {child.coordinates[1] + 1}: Null")

def DLMM(board, depth, nextMovePlayer, isAlphaBeta): 
    prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"

    root_node = MiniMaxNode(board, prevMovePlayer, True, depth)

    # Generate children nodes (possible moves)
    root_node.generateChildren(nextMovePlayer, not root_node.maximizingPlayer, depth)

    # Run Minimax algorithm with a specified depth
    if isAlphaBeta: 

        result, selected_move = root_node.minimax_alpha_beta(depth, -math.inf, math.inf)
    else: 
        result, selected_move = root_node.minimax(depth)


    if selected_move == None: 
        print("No valid moves")

    print("Minimax result:", result)

    print("Output: ")
    root_node.output()

    print("FINAL Move selected: ", selected_move)

    return result, selected_move
