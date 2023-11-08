import random
from node import Node

def select_random_move(board: list, nextMovePlayer: str, printMode: str):
    prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"
    root = Node(board, prevMovePlayer)
    root.generateChildren(nextMovePlayer)
    
    node = generate_random_child(root)

    return node
    

# Function to generate a random child
def generate_random_child(root: Node) -> Node:

    legal_moves = [n for n in root.children]
    for child in root.children:
            print("CHILD", child)
    random_child = random.choice(legal_moves)
    

    return random_child


# Example usage
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

print("Move selected: ", select_random_move(board, paramValue, nextMovePlayer, printMode))
