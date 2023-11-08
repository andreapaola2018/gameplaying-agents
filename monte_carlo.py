from node import Node
import random
# This algorithm is the simplest form of game tree search based on 
# randomized rollouts. It is essentially the UCT algorithm without a 
# sophisticated tree search policy. Please refer to https: 
# // en.wikipedia.org/wiki/Monte_Carlo_tree_search for detailed descriptions
# and examples for both PMCGS and UCT(of course you can also use the course 
# slides, textbook, and other references as needed). The main steps in this 
# algorithm are the same as in UCT, but every move both within the tree 
# search and the rollout is made at random. Output the value for each of 
# the immediate next moves(with Null for illegal moves) and the move 
# selected at the end. Only if the “Verbose” mode is selected you should 
# also print out additional information during each simulation trace, as 
# shown below. For each node in the search tree output the current values 
# of wi and ni, and the move selected. When you reach a leaf in the current 
# tree and add a new node print “NODE ADDED”. For the rollout print only 
# the moves selected, and when you reach a terminal node print the value as 
# “TERMINAL NODE VALUE: X” where X is -1, 0, or 1. Then print the updated 
# values.

# UR
# 0
# R 
# OOOOOOO 
# OOOOOOO 
# OOYOOOY 
# OOROOOY 
# OYRYOYR 
# YRRYORR

def monte_carlo(board: list, paramValue: str, nextMovePlayer: str, printMode: str, uct: bool = False):
    prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"
    root = Node(board, prevMovePlayer)
    root.generateChildren(nextMovePlayer)
    
    node = selectChildNode(root)
    expand(node)
    rollOut(node, nextMovePlayer)
    
    pass
    
def selectChildNode(root: Node) -> Node:
    selected = root
    while len(selected.children) != 0: # while we have not found a lead node
        max_child_value = max(root.children, key=lambda n: n.mcts_value()).mcts_value()
        # select all children with the highest win/numSims ratio
        max_children = [n for n in root.children if n.mcts_value() == max_child_value]
        
        # choose one at random
        selected = random.choice(max_children)
        
        # if the randomly selected child has not yet been explored, return that one
        if selected.numSims == 0:
            return selected
    
    # found leaf, return
    return selected

def expand(node: Node):
    # first check if selected node to expand on is a winning/losing move
    # if so, cannot expand further, so just return
    gameStatus = node.checkGameStatus()
    if gameStatus == "Win" or gameStatus == "Loss":
        return

    # if neither win nor loss, expand
    node.generateChildren("Y" if node.player == "R" else "R")
    
def rollOut(node: Node, nextMovePlayer: str):
    nextMove = node
    gameStatus = "Neither"
    
    while True:
        # choose a move at random from the children of the node
        nextMove = random.choice(nextMove.children)
        gameStatus = nextMove.checkGameStatus()
        
        if gameStatus != "Neither":
            break
        
        nextMove.generateChildren("Y" if nextMove.player == "R" else "R")
        
        if len(nextMove.children) == 0:
            print("Children empty, game status: ", gameStatus)
            break

    gameStatus = "Win" if nextMove.player == nextMovePlayer else "Loss"
    return nextMove, gameStatus # return the leaf node that we end up at and the game outcome

def backPropagate(leaf: Node, gameOutcome: str, nextMovePlayer: str):
    numSims = 0
    numWins = 0
    while leaf:
        leaf.numSims += + numSims + 1
        leaf.wins = (numWins + 1) if (gameOutcome == "Win") else 0
        leaf = leaf.parent # go back up
        numSims += 1
        