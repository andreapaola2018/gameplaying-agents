import math, random

class MiniMaxNode:
    def __init__(self, board, player, maximizingPlayer, depth, parent=None):
        self.board: list = board
        self.player = player
        self.parent = parent
        self.depth = depth
        self.maximizingPlayer = maximizingPlayer
        self.coordinates = [] # to store the coordinates of the current move made
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

    # Generates up to 7 children nodes which represent possible moves for the next player
    def generateChildren(self, nextMovePlayer: str, maximizingPlayer, depth):
        for i in range(7): # check all 7 columns in board
            if not self.__isColumnFull(i):
                coordinates = self.__getCoordinatesForColumn(i)
                if coordinates: # if column is not full, generate a child
                    child = MiniMaxNode(self.board, nextMovePlayer, maximizingPlayer, depth, parent=None)
                    child.coordinates = self.__getCoordinatesForColumn(i)
                    self.__generateBoardForChild(child)
                    self.children.append(child)
    # Checks the current state of the board to see if the move made is a win, loss, or neither move
    def checkGameStatus(self) -> str:
        row = self.coordinates[0]
        col = self.coordinates[1]
        playerTile = self.player
        
        # check horizontal
        rightCount = 0
        leftCount = 0
        right = col+1
        left = col-1
        while right < 7 and self.board[row][right] == playerTile: # count right
            rightCount += 1
            right += 1
        while left >= 0 and self.board[row][left] == playerTile: # count left
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
        while up >= 0 and left >= 0 and self.board[up][left] == playerTile: # count upLeft
            upLeftCount += 1
            left -= 1
            up -= 1
        while down < 6 and right < 7 and self.board[down][right] == playerTile: # count downRight
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
            if "O" in row: # Not full, therefore not a draw
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
        for i in range(5,0,-1):
            if self.board[i][colIndex] == "O": # empty spot
                return [i, colIndex]
        
    # Helper method that returns true if a column for a given index is full, false otherwise
    def __isColumnFull(self, colIndex) -> bool:
        if self.board[0][colIndex] == "O":  # if it's an O, column is not full
            return False
        return True

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        game_result = self.checkGameStatus()

        if depth == 0 or game_result is not None:

            ## game is not over
            if game_result is None:
                # Evaluate the board based on the number of lines with 2 or 3 pieces for each player
                max_lines = self.count_lines(self.board, 'R')
                min_lines = self.count_lines(self.board, 'Y')
                # Return a predicted value between -1 and 1
                return (max_lines - min_lines) / (max_lines + min_lines + 1e-5)
            ##return if game is over
            return game_result

        if maximizingPlayer:
            max_eval = float('-inf')
            for child in self.children:
                eval = child.minimax(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for child in self.children:
                eval = child.minimax(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def bestMove(self, depth):
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for child in self.children:
            eval = child.minimax(depth, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = child.coordinates
        
        return best_move
    

    def count_lines(self, board, player):
        lines = 0

        # Check rows
        for row in board:
            if row.count(player) == 2 or row.count(player) == 3:
                lines += 1

        # Check columns
        for col in range(3):
            if [board[row][col] for row in range(3)].count(player) == 2 or [board[row][col] for row in range(3)].count(player) == 3:
                lines += 1

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] == player:
            lines += 1
        if board[0][2] == board[1][1] == board[2][0] == player:
            lines += 1

        return lines
    
    def evaluate_immediate_moves(self, depth):

        ##set next move player depending on current player
        self.generateChildren('R' if self.player == 'Y' else 'Y', self.maximizingPlayer, depth)
        values_for_columns = {}

        ##iterate through children, if a child is found perform minimax and change to minimze player
        for child in self.children:
            if child.coordinates is not None:

                ##perform minimax on  that child 
                value = child.minimax(depth - 1, float('-inf'), float('inf'), not self.maximizingPlayer)
                col = child.coordinates[1] + 1  # Adjust to 1-based column indexing
                values_for_columns[f"Column {col}"] = value

        # Outputs the heuristic values for each immediate next move
        for key, value in values_for_columns.items():
            print(f"{key}: {value}")

        # Select the move with the highest value
        selected_move = max(values_for_columns, key=values_for_columns.get)
        print(f"FINAL Move selected: {selected_move}")

        return selected_move

# depth = 4
# best_move = root.bestMove(depth)
# print("Best Move:", best_move)
