from node import Node
import random

def uniform_random(board: list, nextMovePlayer: str, printMode: str):
    prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"
    root = Node(board, prevMovePlayer)
    root.generateChildren(nextMovePlayer)
    
    node = generate_random_child(root)
    print("Move Selected", node)
    return node
    

# Function to generate a random child
def generate_random_child(root: Node) -> Node:

    legal_moves = [n for n in root.children]
    for child in root.children:
            print("CHILD", child)
    random_child = random.choice(legal_moves)
    
    return random_child


# board = [
#     ["O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O"],    
#     ["O", "O", "O", "O", "O", "O", "O"],    
#     ["O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "Y", "O", "O", "O"],]

# nextMovePlayer = "R"
# printMode = "verbose"

# print("Move selected: ", uniform_random(board, nextMovePlayer, printMode))
