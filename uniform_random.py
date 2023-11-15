from node import Node
import random

def uniform_random(board: list, nextMovePlayer: str, printMode: str):
    prevMovePlayer = "Y" if nextMovePlayer == "R" else "R"
    root = Node(board, prevMovePlayer)
    root.generateChildren(nextMovePlayer)
    node = generate_random_child(root)
    # print("Move Selected", node)
    return node
    

# Function to generate a random child
def generate_random_child(root: Node) -> Node:

    legal_moves = [n for n in root.children]
    random_child = random.choice(legal_moves)
    return random_child