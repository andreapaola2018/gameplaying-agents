class Node:
    def __init__(self, board, player, parent=None):
        self.board: list = board
        self.player = player
        self.parent = parent
        self.coordinates = [] # to store the coordinates of the current move made
        self.children = []  # List to store child nodes
        
    def setCoordinates(self, coordinates):
        self.coordinates = coordinates
        self.board[coordinates[0]][coordinates[1]] = self.player

    def generateChildren(self):
        for i in range(7): # check all 7 columns in board
            if not self.isColumnFull(i): # if column is not full, generate a child
                child = Node(self.board, self.player, parent=self)
                child.setCoordinates(self.getCoordinatesForColumn(i))
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
        pass
    
    def isColumnFull(self, index) -> bool:
        if self.board[0][index] == "O": # if it's an O, column is not full
            return False
        return True
    
    def getCoordinatesForColumn(self, colIndex):
        for i in range(5,0,-1):
            if self.board[i][colIndex] == "O": # empty spot
                return [i, colIndex]
        return [-1,-1] # column is full
        


# Example usage
current_board = [[0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

current_player = 1
root_node = Node(state=current_board, player=current_player)

# Implement a function to find legal moves
legal_moves = find_legal_moves(current_board)

root_node.expand(legal_moves)
