import math
from gameState import gameState
from dlmm_node import MiniMaxNode

def minimax_alpha_beta(gameState: gameState, root: MiniMaxNode, depth, alpha, beta):   
        game_result = None
        if root.parent != None: 
            game_result = gameState.checkGameStatus(root.coordinates, root.player)

        if depth == 0 or game_result is not None:
            # game is not over
            if game_result is None:
                ##return heuristic and no selected move for non-terminal states
                return heuristic_evaluation(root, gameState), None
            return game_result, None 

        if root.maximizingPlayer:
            max_eval = float('-inf')
            selected_move = None 
            for child in root.children:
                eval, _ = minimax_alpha_beta(gameState, child, depth - 1, alpha, beta)
                if eval > max_eval: 
                    max_eval = eval
                    selected_move = child.coordinates[1]
                    gameState.makeMove(child.coordinates, child.player)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, selected_move + 1 if selected_move is not None else None
        else:
            min_eval = float('inf')
            selected_move = None
            for child in root.children:
                eval, _ = minimax_alpha_beta(gameState, child, depth - 1, alpha, beta)
                if eval < min_eval: 
                    min_eval = eval
                    selected_move = child.coordinates[1]
                    gameState.makeMove(child.coordinates, child.player)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, selected_move + 1 if selected_move is not None else None

def heuristic_evaluation(node: MiniMaxNode, gameState: gameState):
        player = node.player
        opponent = "Y" if player == "R" else "R"

        # Check lines of 2 and 3 pieces for the current player
        player_lines_2 = count_lines_of_length(node, 2, player, gameState)
        player_lines_3 = count_lines_of_length(node, 3, player, gameState)

        # Check lines for the opponent
        opponent_lines_2 = count_lines_of_length(node, 2, opponent, gameState)
        opponent_lines_3 = count_lines_of_length(node, 3, opponent, gameState)

        # Calculate heuristic
        player_score = player_lines_2 + 2 * player_lines_3
        opponent_score = opponent_lines_2 + 2 * opponent_lines_3

        # Normalize scores and return a value between -1 and 1
        total_score = player_score - opponent_score
        max_possible_score = 2 * \
            (count_lines_of_length(node, 3, "R", gameState) + count_lines_of_length(node, 3, "Y", gameState))
        heuristic_value = (
            total_score / max_possible_score) if max_possible_score != 0 else 0
        return heuristic_value

def count_lines_of_length(node, length, player, gameState: gameState):
        lines = 0

        # Check rows
        for row in range(6):
            for col in range(4):
                line = gameState.originalBoard[row][col:col + length]
                # Check if the line contains the player's pieces
                if all(tile == player for tile in line):
                    lines += 1

        # Check columns
        for col in range(7):
            for row in range(3):
                line = [gameState.originalBoard[row + i][col] for i in range(length)]
                if all(tile == player for tile in line):
                    lines += 1

        # Check diagonals (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                line = [gameState.originalBoard[row + i][col + i] for i in range(length)]
                if all(tile == player for tile in line):
                    lines += 1

        # Check diagonals (top-right to bottom-left)
        for row in range(3):
            for col in range(3, 7):
                line = [gameState.originalBoard[row + i][col - i] for i in range(length)]
                if all(tile == player for tile in line):
                    lines += 1

        return lines
    
def output(root: MiniMaxNode, gameState: gameState): 
    for child in root.children:
        eval = heuristic_evaluation(child, gameState)
        print(f"Column {child.coordinates[1] + 1}: {eval}" if eval is not None else f"Column {child.coordinates[1] + 1}: Null")


sample_board = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'Y', 'O'],
    ['O', 'O', 'R', 'Y', 'O', 'R', 'Y'],
    ['O', 'Y', 'R', 'Y', 'O', 'Y', 'R'],
    ['Y', 'R', 'R', 'Y', 'R', 'R', 'R']
]

def DLMM(gameState: gameState, depth, nextMovePlayer): 
    prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"

    root_node = MiniMaxNode(gameState.originalBoard, prevMovePlayer, depth)

    # Generate children nodes (possible moves)
    root_node.generateChildren(nextMovePlayer, not root_node.maximizingPlayer, depth, gameState)

    # Run Minimax algorithm with a specified depth
    result, selected_move = minimax_alpha_beta(gameState, root_node, depth, -math.inf, math.inf)

    if selected_move == None: 
        print("No valid moves")

    print("Minimax result:", result)

    print("Output: ")
    output(root_node, gameState)

    print("FINAL Move selected: ", selected_move)

game = gameState(sample_board)

DLMM(game, 5, "R")
