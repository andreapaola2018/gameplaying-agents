import copy
# A class that represents the current state of the game
class gameState:
    simBoard: list # This is the board that will be used to simulate game play
    originalBoard: list # This is the original board from the original state
    # The next 3 attributes are to store the outcome of the game after simulating game play to the end
    gameOutcome = None 
    isWin: bool = False
    isDraw: bool = False
    
    def __init__(self, board) -> None:
        self.originalBoard = board
        self.simBoard = copy.deepcopy(board)
    
    # Returns a list of coordinates of all legal moves possible in the board
    def getLegalMoves(self):
        legalMoves = []
        
        for colIndex in range(7): # for all 7 columns
            if self.simBoard[0][colIndex] == "O": # the column is not full
                for rowIndex in range(5, -1, -1): # find the next empty spot
                    if self.simBoard[rowIndex][colIndex] == "O": # found next empty spot
                        legalMoves.append([rowIndex, colIndex])
                        break
        
        if legalMoves == []:
            return None
        return legalMoves
    
    # Given move coordinates and a player, makes a move for that player on the simulation board.
    # Caution: expects a legal move, will mess up game play if given an illegal move!
    def makeSimMove(self, moveCoordinates, player):
        row = moveCoordinates[0]
        col = moveCoordinates[1]
        self.simBoard[row][col] = player
     
    # Given move coordinates and a player, makes a move for that player on the actual game board.
    # Caution: expects a legal move, will mess up game play if given an illegal move!
    def makeMove(self, moveCoordinates, player):
        row = moveCoordinates[0]
        col = moveCoordinates[1]
        self.originalBoard[row][col] = player
        
    # Helper method to print out the board in a nice, readable format
    def printBoard(self):
        if self.simBoard is None:
            print("No board")
        b = ""
        for row in self.simBoard:
            b += "["
            for i in range(7):
                b += "'" + row[i] + ("', " if i < 6 else "'")
            b += "]\n"
        print(b)
        
    # This method resets the current game state to its original state before simulating game play to the end
    def resetToOriginalState(self):
        self.simBoard = copy.deepcopy(self.originalBoard)
        self.isWin = self.isDraw = False
        self.gameOutcome = None
    
    # Checks the current state of the board to see if the move made by the player is a win, draw, or neither
    def checkGameStatus(self, moveCoordinates, player):
        row = moveCoordinates[0]
        col = moveCoordinates[1]

        # check horizontal
        rightCount = 0
        leftCount = 0
        right = col+1
        left = col-1
        while right < 7 and self.simBoard[row][right] == player:  # count right
            rightCount += 1
            right += 1
        while left >= 0 and self.simBoard[row][left] == player:  # count left
            leftCount += 1
            left -= 1
        total = rightCount + leftCount + 1
        if total >= 4:
            # if Red won -> return -1, if Yellow won -> return 1
            self.isWin = True
            self.gameOutcome = -1 if player == "R" else 1
            return self.gameOutcome

        # check vertical
        upCount = 0
        downCount = 0
        up = row-1
        down = row+1
        while down < 6 and self.simBoard[down][col] == player:  # count down
            downCount += 1
            down += 1
        while up >= 0 and self.simBoard[up][col] == player:  # count up
            upCount += 1
            up -= 1
        total = downCount + upCount + 1
        if total >= 4:
            # if Red won -> return -1, if Yellow won -> return 1
            self.isWin = True
            self.gameOutcome = -1 if player == "R" else 1
            return self.gameOutcome

        # check top left to bottom right diagonal
        upLeftCount = 0
        downRightCount = 0
        up = row-1
        left = col-1
        down = row+1
        right = col+1
        # count upLeft
        while up >= 0 and left >= 0 and self.simBoard[up][left] == player:
            upLeftCount += 1
            left -= 1
            up -= 1
        # count downRight
        while down < 6 and right < 7 and self.simBoard[down][right] == player:
            downRightCount += 1
            right += 1
            down += 1
        total = upLeftCount + downRightCount + 1
        if total >= 4:
            # if Red won -> return -1, if Yellow won -> return 1
            self.isWin = True
            self.gameOutcome = -1 if player == "R" else 1
            return self.gameOutcome

        # check top right to bottom left diagonal
        upRightCount = 0
        downLeftCount = 0
        up = row-1
        right = col+1
        down = row+1
        left = col-1
        # count upRight
        while up >= 0 and right < 7 and self.simBoard[up][right] == player:
            upRightCount += 1
            right += 1
            up -= 1
        # count downLeft
        while down < 6 and left >= 0 and self.simBoard[down][left] == player:
            downLeftCount += 1
            left -= 1
            down += 1
        total = upRightCount + downLeftCount + 1
        if total >= 4:
            # if Red won -> return -1, if Yellow won -> return 1
            self.isWin = True
            self.gameOutcome = -1 if player == "R" else 1
            return self.gameOutcome

        # If we get to this point, it means one of 2 things:
        # (1) The move was a draw, which is true if the board is full now, or
        # (2) The move is neither a win nor a draw, and the board still has empty spaces for more moves

        # Check if board is full
        for row in self.simBoard:
            if "O" in row:  # Not full, therefore not a draw
                # return None, meaning there are still moves left that can be made
                return None

        # If board was full, then it was a draw since there were no winners
        self.isDraw = True
        self.gameOutcome = 0
        return 0
