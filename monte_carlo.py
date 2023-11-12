from mcts_node import MonteCarloNode
import random
from PrettyPrint import PrettyPrintTree

def monteCarloTreeSearch(board: list, paramValue: int, nextMovePlayer: str, printMode: str, uct: bool = False):
    prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"
    root = MonteCarloNode(board, prevMovePlayer)
    root.generateChildren(nextMovePlayer)
    
    # Runs for paramValue times
    for _ in range(paramValue):
        node = selectChildNode(root, uct)
        print("selected node: ", node)
        # if the selected node turns out to be a terminal move, we can't roll out any more moves
        # therefore, expand will return a boolean to let us know if we can or cannot expand on that node
        isExpandable = expand(node)
        if isExpandable: # if we can expand, we roll out simulations and back propagate from the returned leaf
            leaf = rollOut(node)
            backPropagate(leaf, nextMovePlayer)
        else: # else, we back propagate from the selected node, which turned out to be a non-expandable leaf
            backPropagate(node, nextMovePlayer)
        
    # once it is done running simulations, must choose the move with the max mcts value
    # root.printChildrenNodes()
    if not uct:
        printTreeMcts(root)
    else:
        printTreeMcts(root)
        print("\n")
        printTreeUct(root)
    
    return max(root.children, key=lambda n: n.pureMctsValueInt())
  

def printTreeMcts(root: MonteCarloNode):
    pt = PrettyPrintTree(lambda x: x.children, lambda x: x.pureMctsValueStr())
    pt(root)

def printTreeUct(root: MonteCarloNode):
    pt = PrettyPrintTree(lambda x: x.children, lambda x: x.uctValueInt(root.numSims))
    pt(root)
    
def selectChildNode(root: MonteCarloNode, uct: bool = False) -> MonteCarloNode:
    selected = root
    while len(selected.children) != 0: # while we have not found a leaf node
        maxSims = max(selected.children, key=lambda n: n.numSims).numSims
        
        if maxSims == 0: # this means that none of the children have been explored (no simulations have been run in any!)
            # select one at random
            return random.choice(selected.children)
        
        # we want to prioritize exploring children that have not been explored yet
        unexploredChildren = [n for n in selected.children if n.numSims == 0]
        if len(unexploredChildren) != 0: # this means that there exists at least 1 child that has not been explored yet
            return random.choice(unexploredChildren)
            
        # if we reach here, it means all children have been explored, therefore we want to traverse
        # the child with the highest mcts or uct (depending on algorithm) value to find a leaf node
        maxChildren = []
        if uct: # we will use uct value
            rootNumSims = root.numSims
            maxChildValue = max(selected.children, key=lambda n: n.uctValueInt(rootNumSims)).uctValueInt(rootNumSims)
            maxChildren = [n for n in selected.children if n.uctValueInt(rootNumSims) == maxChildValue]
        else: # else pure monte carlo
            maxChildValue = max(selected.children, key=lambda n: n.pureMctsValueInt()).pureMctsValueInt()
            maxChildren = [n for n in selected.children if n.pureMctsValueInt() == maxChildValue]
        
        # if there are ties for the highest mcts value, choose one at random
        selected = random.choice(maxChildren)
        selected.generateChildren(flipPlayer(selected))
    
    # found leaf, return
    return selected

def expand(node: MonteCarloNode) -> bool:
    # first check if selected node to expand on is a winning move
    # if so, cannot expand further, so just return
    gameStatus = node.checkGameStatus()
    if (gameStatus == -1 and node.player == "R") or (gameStatus == 1 and node.player == "Y"):
        print("Win!")
        return False
    
    # second, check if the selected node to expand on is a draw move (meaning the board is now full!)
    # if so, cannot expand further, so just return
    if gameStatus == 0:
        print("draw!")
        return False

    # if neither win nor draw, expand
    node.generateChildren(flipPlayer(node))
    return True
    
def rollOut(node: MonteCarloNode):
    nextMove = node
    
    while True:
        # choose a move at random from the children of the node
        nextMove = random.choice(nextMove.children)
        gameStatus = nextMove.checkGameStatus()
        
        if gameStatus != None: # if the game status is win or draw, we are done rolling out simulations
            # reached terminal node!
            break
        
        nextMove.generateChildren(flipPlayer(nextMove))
        
        if len(nextMove.children) == 0: # If we could not generate more children, it means a terminal state was reached
            # Note: This if statement is here as a precaution, given the if statement above, this should never happen
            print("Children empty, game status: ", gameStatus)
            print("current child: ", nextMove)
            break

    return nextMove # return the leaf node that we end up at

def backPropagate(leaf: MonteCarloNode, nextMovePlayer: str):
    #numSims = 0
    gameOutcome = leaf.checkGameStatus()
    # Since this is a leaf node, the game outcome should be either a win or a draw
    # if this is not the case, clearly there was an error somewhere
    if gameOutcome is None:
        print("Error in leaf node")
        print("Leaf that has error: ", leaf)
        return
    
    print("Leaf in back propagate: ", leaf)
    print("Game outcome: ", gameOutcome)
    
    while leaf:
        leaf.numSims += 1
        # if the player we simulated the moves for won the game, increment number of wins
        if ((gameOutcome == -1 and nextMovePlayer == "R") or (gameOutcome == 1 and nextMovePlayer == "Y")): 
            leaf.wins += 1
        leaf = leaf.parent # go back up
        # numSims += 1
        
def flipPlayer(node: MonteCarloNode) -> str:
    return "Y" if node.player == "R" else "R"
