from node_dlmm import Node
import math, random

def is_terminal(node: Node) -> bool:

    gameStatus = node.checkGameStatus()
    if (gameStatus == -1 and node.player == "R") or (gameStatus == 1 and node.player == "Y"):
        print("win!")
        return True

    # game is a draw
    if gameStatus == 0:
        return True
    
    return False
        
def minimax_alpha_beta(board, root: Node, depth, alpha, beta, maximizing_player, nextMovePlayer: str):
    # print("is maximizing player: ", maximizing_player, "depth: ", depth)
    # print("root", root)

    ##flip maximizing player since its children will have to be minimized or maximized depending on what is coming in 
    if maximizing_player == True: 
        root.generateChildren(nextMovePlayer, False, depth)
    else: 
        root.generateChildren(nextMovePlayer, True, depth)

    ##select random node, check it its terminal, if not, check if its max or min and continue
    ##select random child 
    current_node = select_random_child(root)
    print("random child", current_node)
    for child in root.children: 
        print(child)

    # root = current_node
   
    if depth == 0 or is_terminal(current_node):
        
        # Check for a win or loss
        gameStatus = current_node.checkGameStatus()
        print("game status", gameStatus)
        if gameStatus == 1 and current_node.player == "Y":
            return 1  # Maximizer wins
        elif gameStatus == -1 and current_node.player == "R":
            return -1  # Minimizer wins
        elif gameStatus == 0:
            return 0  # It's a draw

        # Evaluate the board based on the number of lines with 2 or 3 pieces for each player
        max_lines = count_lines(current_node.board, 'R')
        min_lines = count_lines(current_node.board, 'Y')
        # Return a predicted value between -1 and 1
        return (max_lines - min_lines) / (max_lines + min_lines + 1e-5)
    

    if maximizing_player:
        max_eval = -math.inf
        for child in root.children:
            print(child)
            eval_score = minimax_alpha_beta(board, child, depth-1, alpha, beta, False, nextMovePlayer)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = math.inf
        for child in root.children:
            print(child)
            eval_score = minimax_alpha_beta(board, child, depth-1, alpha, beta, True, nextMovePlayer)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

def count_lines(board, player):
    lines = 0

    # Check rows
    for row in board:
        if row.count(player) == 2 or row.count(player) == 3:
            lines += 1

    # Check columns
    for col in range(3):
        if [board[row][col] for row in range(3)].count(player) == 2 or [board[row][col] for row in range(3)].count(player) == 3:
            lines += 1

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        lines += 1
    if board[0][2] == board[1][1] == board[2][0] == player:
        lines += 1

    return lines

def select_random_child(root: Node) -> Node: 
    
    random_child_node = random.choice(root.children)
    return random_child_node


# Example usage:
board = [
    ["O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O"],    
    ["O", "O", "O", "O", "O", "O", "O"],    
    ["O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "Y", "O", "O", "R"],
]

nextMovePlayer = "Y"
depth = 5 ##depth is our parameter  value
maximizing_player = True
alpha = -math.inf
beta = math.inf


prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"
root = Node(board, prevMovePlayer, maximizing_player, depth)
print("output of minimax", minimax_alpha_beta(board, root, depth, alpha, beta, maximizing_player, nextMovePlayer))