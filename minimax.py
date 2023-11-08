from node import Node
import math, random
import copy

def minimax(board, depth, alpha, beta, maximizing_player, nextMovePlayer: str, printMode: str):
    prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"
    root = Node(board, prevMovePlayer)
    ##generating possible moves 
    root.generateChildren(nextMovePlayer)

    minimax_alpha_beta(root, board, depth, alpha, beta, maximizing_player)



def minimax_alpha_beta(root: Node, board, depth, alpha, beta, maximizing_player): 
    if depth == 0: 
        return 0 ## return heuristic value 
    
    if maximizing_player:
        value = -math.inf
        ##random column to check 
        column = random.choice(root.children)
        for child in root.children: 
            ## get next open row 

            ## copy board 
            board_copy = board.copy() 

            ##place piece in board copy 

            ## calculate new score 
            new_score = minimax_alpha_beta(board_copy, depth-1, alpha, beta, False)[1]



            



board = [
    ["O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O"],    
    ["O", "O", "O", "O", "O", "O", "O"],    
    ["O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "Y", "O", "O", "O"],]

paramValue = 0
nextMovePlayer = "R"
printMode = "verbose"
depth = 5
maximizing_player = True
alpha = -math.inf
beta = math.inf
print("output", minimax(board, depth, alpha, beta, maximizing_player, nextMovePlayer, printMode))
    