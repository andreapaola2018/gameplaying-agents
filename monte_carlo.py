from node import Node
import random
# from PrettyPrint import PrettyPrintTree

def monteCarloTreeSearch(board: list, paramValue: int, nextMovePlayer: str, printMode: str, uct: bool = False):
    prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"
    root = Node(board, prevMovePlayer)
    root.generateChildren(nextMovePlayer)
    
    # Runs for paramValue times
    for _ in range(paramValue):
        node = selectChildNode(root)
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
    printTree(root)
    
    return max(root.children, key=lambda n: n.mctsValueInt())
  

# def printTree(root: Node):
#     pt = PrettyPrintTree(lambda x: x.children, lambda x: x.mctsValueStr())
#     pt(root)
    
def selectChildNode(root: Node) -> Node:
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
        # the child with the highest mcts value to find a leaf node
        maxChildValue = max(selected.children, key=lambda n: n.mctsValueInt()).mctsValueInt()
        maxChildren = [n for n in selected.children if n.mctsValueInt() == maxChildValue]
        
        # if there are ties for the highest mcts value, choose one at random
        selected = random.choice(maxChildren)
        selected.generateChildren(flipPlayer(selected))
    
    # found leaf, return
    return selected

def expand(node: Node) -> bool:
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
    
def rollOut(node: Node):
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

def backPropagate(leaf: Node, nextMovePlayer: str):
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
        
def flipPlayer(node: Node) -> str:
    return "Y" if node.player == "R" else "R"