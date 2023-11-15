from gameState import gameState
class MiniMaxNode:
    def __init__(self, player, maximizingPlayer, depth,  coordinates=[],  parent=None):
        # self.board: list = board
        self.player = player
        self.parent = parent
        self.depth = depth
        self.maximizingPlayer = maximizingPlayer
        self.coordinates = coordinates  # to store the coordinates of the current move made
        self.children: list[MiniMaxNode] = []  # List to store child nodes

    def __str__(self):
        return "Coordinates: " + ((str(self.coordinates[0]) + " " + str(self.coordinates[1])) if (len(self.coordinates) == 2) else "")

     # Given the player and the game state, generates up to 7 children nodes which represent all the legal possible moves for the player
    def generateChildren(self, nextMovePlayer: str, maximizingPlayer, depth, gameState: gameState):
        legalMoves = gameState.getLegalMoves()
        if legalMoves is not None: 
            for move in legalMoves:
                maximizingPlayer_for_child = not self.maximizingPlayer
                child = MiniMaxNode(nextMovePlayer, maximizingPlayer_for_child, depth-1, move, self)
                self.children.append(child)
                if depth > 1:  # Considering the depth limit
                    child.generateChildren("R" if nextMovePlayer == "Y" else "Y", maximizingPlayer_for_child, depth - 1, gameState)
