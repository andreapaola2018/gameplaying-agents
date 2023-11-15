from mcts_node import MonteCarloNode
import random
# from PrettyPrint import PrettyPrintTree

def monteCarloTreeSearch(board: list, paramValue: int, nextMovePlayer: str, printMode: str = "None", uct: bool = False):
    prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"
    root = MonteCarloNode(board, prevMovePlayer)
    root.generateChildren(nextMovePlayer)
    
    # Runs for paramValue times
    for _ in range(paramValue):
        if printMode == "verbose":
            print("Selecting child node...")
        node = selectChildNode(root, uct)
        if printMode == "verbose":
            print("wi: ", node.wins)
            print("ni: ", node.numSims)
        if printMode == "brief" or printMode == "verbose":
            print("Move selected: ", node.coordinates[1]+1) # represents the column of the move selected (since indexing is 0 based we add a 1 to it)
        
        if printMode == "verbose":
            print("Expanding the selected child node...")
        # if the selected node turns out to be a terminal move, we can't roll out any more moves
        # therefore, expand will return a boolean to let us know if we can or cannot expand on that node
        isExpandable = expand(node, printMode)
        if isExpandable: # if we can expand, we roll out simulations and back propagate from the returned leaf
            if printMode == "verbose":
                print("Rolling out simulations...")
            leaf = rollOut(node, printMode)
            if printMode == "verbose":
                print("Performing back propagate...")
            backPropagate(leaf, nextMovePlayer, printMode)
        else: # else, we back propagate from the selected node, which turned out to be a non-expandable leaf
            if printMode == "verbose":
                print("Performing back propagate...")
            backPropagate(node, nextMovePlayer, printMode)
        
    # if not uct:
    #     printTreeMcts(root)
    # else:
    #     printTreeMcts(root)
    #     print("\n")
    #     printTreeUct(root)
    if printMode == "brief" or printMode == "verbose":
        columns = [n.coordinates[1]+1 for n in root.children]
        c = 0
        for i in range(7):
            if (i+1) not in columns:
                print("Column ", i+1, ": Null")
            else:
                print("Column ", i+1, ": ", root.children[c].pureMctsValueInt())
                c += 1
        # for child in root.children:
        #     print("Column ", child.coordinates[1]+1, ": ", child.pureMctsValueInt())
    
    # once it is done running simulations, must choose the move with the max or min mcts value
    # regardless of whether it is with uct or not, the final move that is selected is the
    # one based on the direct estimate of the node value. The move is maximized or minimized
    # depending on whose turn it is.    
    if nextMovePlayer == "R": # means we want to minimize
        return min(root.children, key=lambda n: n.pureMctsValueInt())
    
    # else it is yellow's turn, so we want to maximize
    return max(root.children, key=lambda n: n.pureMctsValueInt())

# def printTreeMcts(root: MonteCarloNode):
#     pt = PrettyPrintTree(lambda x: x.children, lambda x: x.pureMctsValueStr())
#     pt(root)

# def printTreeUct(root: MonteCarloNode):
#     pt = PrettyPrintTree(lambda x: x.children, lambda x: x.uctValueInt(root.numSims))
#     pt(root)
    

def selectChildNode(root: MonteCarloNode, uct: bool = False) -> MonteCarloNode:
    selected = root
    while len(selected.children) != 0: # while we have not found a leaf node
        maxSims = max(selected.children, key=lambda n: n.numSims).numSims
        
        if maxSims == 0: # this means that none of the children have been explored (no simulations have been run in any!)
            # select an unexplored child at random
            return random.choice(selected.children)
        
        # we want to prioritize exploring children that have not been explored yet
        unexploredChildren = [n for n in selected.children if n.numSims == 0]
        if len(unexploredChildren) != 0: # this means that there exists at least 1 child that has not been explored yet
            # select an unexplored child at random
            return random.choice(unexploredChildren)
            
        # if we reach here, it means all children have been explored, therefore we want to traverse
        # the child with the highest mcts or uct (depending on algorithm) value to find a leaf node
        maxChildren = []
        if uct: # we will use uct value
            currentMovePlayer = root.children[0].player
            rootNumSims = root.numSims
            
            if currentMovePlayer == "R": # means we want to minimize
                minChildValue = min(selected.children, key=lambda n: n.uctValueInt(rootNumSims)).uctValueInt(rootNumSims)
                minChildren = [n for n in selected.children if n.uctValueInt(rootNumSims) == minChildValue]
                selected = random.choice(minChildren) # choose min child at random
            else: # means we want to maximize
                maxChildValue = max(selected.children, key=lambda n: n.uctValueInt(rootNumSims)).uctValueInt(rootNumSims)
                maxChildren = [n for n in selected.children if n.uctValueInt(rootNumSims) == maxChildValue]
                selected = random.choice(maxChildren) # choose max child at random
                
        else: # else pure monte carlo, choose next move at random
            selected = random.choice(selected.children)
            # maxChildValue = max(selected.children, key=lambda n: n.pureMctsValueInt()).pureMctsValueInt()
            # maxChildren = [n for n in selected.children if n.pureMctsValueInt() == maxChildValue]
        
        selected.generateChildren(flipPlayer(selected))
    
    # found leaf, return
    return selected

def expand(node: MonteCarloNode, printMode: str) -> bool:
    # first check if selected node to expand on is a winning or draw move
    # if so, cannot expand further, so return False
    gameStatus = node.checkGameStatus()
    # # if (gameStatus == -1 and node.player == "R") or (gameStatus == 1 and node.player == "Y"):
    if gameStatus == -1 or gameStatus == 0 or gameStatus == 1:   
        if printMode == "verbose":
            print("TERMINAL NODE VALUE: ", gameStatus, "\n")
        return False

    # if neither win nor draw, expand
    node.generateChildren(flipPlayer(node))
    if printMode == "verbose":
        print("NODE ADDED\n")
    return True
    
def rollOut(node: MonteCarloNode, printMode: str):
    nextMove = node
    
    while True:
        # choose a move at random from the children of the node
        if printMode == "verbose":
            print("wi: ", nextMove.wins)
            print("ni: ", nextMove.numSims)
        nextMove = random.choice(nextMove.children)
        if printMode == "brief" or printMode == "verbose":
            print("Move selected: ", nextMove.coordinates[1]+1, "\n")
        gameStatus = nextMove.checkGameStatus()
        
        if gameStatus != None: # if the game status is win or draw, we are done rolling out simulations
            # reached terminal node!
            if printMode == "verbose":
                print("TERMINAL NODE VALUE: ", gameStatus, "\n")
            break
        
        nextMove.generateChildren(flipPlayer(nextMove))
        if printMode == "verbose":
            print("NODE ADDED\n")
        
        if len(nextMove.children) == 0: # If we could not generate more children, it means a terminal state was reached
            # Note: This if statement is here as a precaution, given the if statement above, this should never happen
            print("Children empty, game status: ", gameStatus)
            print("current child: ", nextMove)
            break

    return nextMove # return the leaf node that we end up at

def backPropagate(leaf: MonteCarloNode, nextMovePlayer: str, printMode: str):
    numSims = 0
    gameOutcome = leaf.checkGameStatus()
    # Since this is a leaf node, the game outcome should be either a win or a draw
    # if this is not the case, clearly there was an error somewhere
    if gameOutcome is None: # this is here as a precaution and should never happen
        print("Error in leaf node")
        print("Leaf that has error: ", leaf)
        return
    
    while leaf:
        leaf.numSims += numSims + 1
        leaf.wins += gameOutcome
        # if the player we simulated the moves for won the game, increment number of wins
        # if ((gameOutcome == -1 and nextMovePlayer == "R") or (gameOutcome == 1 and nextMovePlayer == "Y")): 
        #     leaf.wins += 1
        if printMode == "verbose":
            print("Updated values:")
            print("wi: ", leaf.wins)
            print("ni: ", leaf.numSims, "\n")
        leaf = leaf.parent # go back up
        numSims += 1
        
def flipPlayer(node: MonteCarloNode) -> str:
    return "Y" if node.player == "R" else "R"