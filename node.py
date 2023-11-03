class Node:
    def __init__(self, board, player, parent=None):
        self.board: list = board
        self.player = player
        self.parent = parent
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

    # Generates up to 7 children nodes which represent possible moves for the next player
    def generateChildren(self):
        for i in range(7): # check all 7 columns in board
            coordinates = self.__getCoordinatesForColumn(i)
            if coordinates: # if column is not full, generate a child
                child = Node(self.board, self.player, parent=self)
                child.coordinates = self.__getCoordinatesForColumn(i)
                self.__generateBoardForChild(child)
                self.children.append(child)
                
        # for action in legal_moves:
        #     # Create a new state by applying the action to the current state
        #     new_state = apply_action(self.state, action, self.player)

        #     # Determine the next player's turn
        #     next_player = 1 if self.player == 2 else 2

        #     # Create a child node for the new state
        #     child_node = Node(state=new_state, player=next_player, parent=self)

        #     # Add the child node to the list of children
        #     self.children.append(child_node)

        # return self.children
        
    def isLegalMove(self) -> bool:
        # TODO
        pass
     
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
