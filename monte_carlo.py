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

def monte_carlo(board: list, param_value: str, next_move_player: str, printMode: str):
    # TODO
    pass
    

class Node:
    def __init__(self, state, player, parent=None):
        self.state = state
        self.player = player
        self.parent = parent
        self.children = []  # List to store child nodes

    def expand(self, legal_moves):
        for action in legal_moves:
            # Create a new state by applying the action to the current state
            new_state = apply_action(self.state, action, self.player)

            # Determine the next player's turn
            next_player = 1 if self.player == 2 else 2

            # Create a child node for the new state
            child_node = Node(state=new_state, player=next_player, parent=self)

            # Add the child node to the list of children
            self.children.append(child_node)

        return self.children


# Example usage
current_board = [[0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

current_player = 1
root_node = Node(state=current_board, player=current_player)

# Implement a function to find legal moves
legal_moves = find_legal_moves(current_board)

root_node.expand(legal_moves)
