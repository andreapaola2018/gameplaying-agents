import math
from gameState import gameState

# The UCT constant parameter.
# Can be modified to any other constant. We chose square root of 2 as our constant.
EXPLORATION_PARAMETER: int = math.sqrt(2)

# A Monte Carlo Tree Node class that keeps track of the current player, the number of wins,
# the total number of simulations, the coordinates of the move that the node represents, and 
# a list of child nodes for the next moves possible from this node
class MonteCarloNode:
    def __init__(self, player, coordinates=[], parent=None):
        self.player = player # player the node represents making a move for
        self.parent = parent
        self.wins = 0
        self.numSims = 0
        self.coordinates = coordinates # to store the coordinates of the current move made
        self.children: list[MonteCarloNode] = []  # List to store child nodes
        
    def __str__(self):
        return "Coordinates: " + ((str(self.coordinates[0]) + " " + str(self.coordinates[1])) if (len(self.coordinates) == 2) else "") + " MCTS value: " + str(self.pureMctsValueInt()) + "\n"
    
    # Helper method that prints out all children nodes of a node
    def printChildrenNodes(self):
        for child in self.children:
            print(child.coordinates)
        
    # TO DELETE    
    def pureMctsValueStr(self) -> str:
        return str(self.wins) + "/" + str(self.numSims)
    
    # Represents the pure MCST value (num of wins / num of simulations)
    def pureMctsValueInt(self) -> int:
        return 0 if self.numSims == 0 else self.wins/self.numSims
    
    # Represents the UCT value
    def uctValueInt(self, rootNumSims):
        if self.numSims == 0:
            return self.pureMctsValueStr()
        return (self.wins / self.numSims) + (EXPLORATION_PARAMETER * math.sqrt(math.log(rootNumSims) / self.numSims))

    # Given the player and the game state, generates up to 7 children nodes which represent all the legal possible moves for the player
    def generateChildren(self, nextMovePlayer: str, gameState: gameState):
        legalMoves = gameState.getLegalMoves()
        for move in legalMoves:
            child = MonteCarloNode(nextMovePlayer, move, self)
            self.children.append(child)
                    