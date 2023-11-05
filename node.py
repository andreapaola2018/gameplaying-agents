class Node:
    def __init__(self, board, player, parent=None):
        self.board: list = board
        self.player = player
        self.parent = parent
        self.wins = 0
        self.numSims = 0
        self.coordinates = [] # to store the coordinates of the current move made
        self.children: list[Node] = []  # List to store child nodes
        
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
    
    def printChildrenNodes(self):
        for child in self.children:
            print(child)
            
    def val(self):
        return str(self.wins) + "/" + str(self.numSims)

    # Generates up to 7 children nodes which represent possible moves for the next player
    def generateChildren(self, nextMovePlayer: str):
        for i in range(7): # check all 7 columns in board
            if not self.__isColumnFull(i):
                coordinates = self.__getCoordinatesForColumn(i)
                if coordinates: # if column is not full, generate a child
                    child = Node(self.board, nextMovePlayer, parent=self)
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
            return "Win"
        
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
            return "Win"

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
            return "Win"
        
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
            return "Win"
        
        # If we get to this point, it means one of 2 things:
        # (1) The move was a loss, which is true if the board is full now, or
        # (2) The move is neither a win nor a loss
        
        # Check if board is full
        for row in self.board:
            if "O" in row: # Not full, therefore not a loss
                return "Neither"
        
        # If board was full, then it was a loss
        return "Loss"
    
    def mcts_value(self) -> int:
        return 0 if self.numSims == 0 else self.wins/self.numSims

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
        if self.__isColumnFull(colIndex): # technically should not happen since is checked before this method is called
            return None
        for i in range(5,0,-1):
            if self.board[i][colIndex] == "O": # empty spot
                return [i, colIndex]
        
    # Helper method that returns true if a column for a given index is full, false otherwise
    def __isColumnFull(self, colIndex) -> bool:
        if self.board[0][colIndex] == "O":  # if it's an O, column is not full
            return False
        return True
