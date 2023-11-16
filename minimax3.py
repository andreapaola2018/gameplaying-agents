import math
import random

class Connect4Node:
    def __init__(self, board, maximizing_player, depth, move=None):
        self.board = board
        self.maximizing_player = maximizing_player
        self.depth = depth
        self.move = move
        self.children = []
        self.coordinates = []

    def is_terminal(self):
        # Check for a win or draw
        if self.check_winner("R"):
            return True, 1  # Player 'R' wins
        elif self.check_winner("Y"):
            return True, -1  # Player 'Y' wins
        elif self.is_board_full():
            return True, 0  # Draw
        return False, None

    def check_winner(self, player):
        # Check for a win in rows, columns, and diagonals
        for row in range(6):
            for col in range(4):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True
        for col in range(7):
            for row in range(3):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True
        for row in range(3):
            for col in range(4):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True
                if all(self.board[row + i][col + 3 - i] == player for i in range(4)):
                    return True
        return False

    def is_board_full(self):
        # Check if the board is full
        return all(cell != ' ' for row in self.board for cell in row)

    def generate_children(self):
        for col in range(7):
            if self.is_valid_move(col):
                child_board = [row.copy() for row in self.board]
                row = self.get_empty_row(col)
                child_board[row][col] = 'R' if self.maximizing_player else 'Y'
                child = Connect4Node(child_board, not self.maximizing_player, self.depth - 1, move=col + 1)
                self.children.append(child)

    def is_valid_move(self, col):
        # Check if a move is valid in the given column
        return self.board[0][col] == ' ' if col < 7 else False

    def get_empty_row(self, col):
        # Find the first empty row in a column
        for row in range(5, -1, -1):
            if self.board[row][col] == ' ':
                return row

    def heuristic_evaluation(self):
        # Basic heuristic: count lines of length 2 and 3 for each player
        player = 'R' if self.maximizing_player else 'Y'
        opponent = 'Y' if player == 'R' else 'R'

        player_lines_2 = self.count_lines_of_length(2, player)
        player_lines_3 = self.count_lines_of_length(3, player)

        opponent_lines_2 = self.count_lines_of_length(2, opponent)
        opponent_lines_3 = self.count_lines_of_length(3, opponent)

        player_score = player_lines_2 + 2 * player_lines_3
        opponent_score = opponent_lines_2 + 2 * opponent_lines_3

        total_score = player_score - opponent_score
        max_possible_score = 2 * (self.count_lines_of_length(3, 'R') + self.count_lines_of_length(3, 'Y'))

        if max_possible_score != 0:
            heuristic_value = total_score / max_possible_score
        else:
            heuristic_value = 0

        return heuristic_value

    def count_lines_of_length(self, length, player):
        lines = 0

        for row in range(6):
            for col in range(4):
                line = self.board[row][col:col + length]
                if all(tile == player for tile in line):
                    lines += 1

        for col in range(7):
            for row in range(3):
                line = [self.board[row + i][col] for i in range(length)]
                if all(tile == player for tile in line):
                    lines += 1

        for row in range(3):
            for col in range(4):
                line = [self.board[row + i][col + i] for i in range(length)]
                if all(tile == player for tile in line):
                    lines += 1

            for col in range(3, 7):
                line = [self.board[row + i][col - i] for i in range(length)]
                if all(tile == player for tile in line):
                    lines += 1

        return lines

    def minimax(self):
        is_terminal, value = self.is_terminal()

        if is_terminal:
            return value, None

        if self.depth == 0:
            return self.heuristic_evaluation(), None

        if self.maximizing_player:
            max_eval = float('-inf')
            selected_move = None
            for child in self.children:
                eval, _ = child.minimax()
                if eval > max_eval:
                    max_eval = eval
                    selected_move = child.move
            return max_eval, selected_move
        else:
            min_eval = float('inf')
            selected_move = None
            for child in self.children:
                eval, _ = child.minimax()
                if eval < min_eval:
                    min_eval = eval
                    selected_move = child.move
            return min_eval, selected_move

def print_moves(node):
    for child in node.children:
        print(f"Column {child.move}: {child.minimax()[0]}" if child.move is not None else f"Column Null")

if __name__ == "__main__":
    initial_board = [['O'] * 7 for _ in range(6)]

    root_node = Connect4Node(initial_board, maximizing_player=True, depth=3)
    root_node.generate_children()

    print_moves(root_node)

    final_move = root_node.minimax()[1]
    print(f"FINAL Move selected: {final_move}")
