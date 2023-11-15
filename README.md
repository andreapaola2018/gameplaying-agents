# gameplaying-agents - Connect Four
Programming Assignment 2: Game Playing Agents

created by Montserrat Molina & Andrea Ulloa

## Getting Started

To clone this repo, run `https://github.com/andreapaola2018/gameplaying-agents.git`

## Running our Project

In the project directory, you can run:

`python3 play.py <name of text file>.txt <print mode>`

### Print Modes Accepted: `None`, `Brief`, and `Verbose`, in this exact format

## Features

Given a text file which contains 3 lines at the top, the first one representing a game search algorith, the second one representing a parameter for game search, and the third one representing the next player's turn, followed by a 6 by 7 board representing a Connect 4 board, game play is simulated using different game search algorithms.

A win for "Red" is denoted by -1. A win for "Yellow" is denoted by 1. A draw is denoted by 0.

Game search algorithms supported are: Uniform Random (UR), Depth-Limited MinMax (DLMM), Pure Monte Carlo Game Search (PMCGS), and Upper Confidence bound for Trees (UCT).

### Uniform Random (UR)

The Uniform Random algorithm chooses a node or in this case a move in Connect 4, at random. This algorithm selects a legal move and each legal move is selected with the same probability. 

### Depth-Limited MinMax (DLMM)

Depth-Limited MinMax uses depth-first minimax search to a certain depth to select a next move. At the the nodes at the specified depth limit or the leaf nodes, a heuristic evaluation function is used to estimate value of the game state. The values calculated are then back propagated to the root of the tree. At each level of the tree the algorithm chooses the maximum or minimum value, depending on whether it is the player's or the opponent's turn. This continues until the root node is reached.

### Pure Monte Carlo Game Search (PMCGS)

This algorithm follows the simplest form of game tree search using monte carlo game search. It creates a tree based off of the given state of the game, and simulates n randomized rollouts (n is based on the parameter value passed in on the text file). Every move within the tree search and the rollout is made at random. Once n rollouts have been reached, it returns the best move (based on the number of wins over the number of simulations) for the next player. For "Red", this means choosing the move with the minimum value. For "Yellow", this means choosing the move with the maximum value. 

Ties are broken by choosing a move at random. Nodes that have not been explored in the tree yet are prioritized before attempting to find a leaf node from a node that has already been explored.

### Upper Confidence bound for Trees (UCT)

This algorithm is an extension of Pure Monte Carlo Game Tree Search adding the use of the Upper Confidence Bounds algorithm for selecting nodes within the existing search tree. Instead of selecting nodes at random, nodes are selected based on their UCB value (which again means minimizing the value for "Red" and maximizing the value for "Yellow").

Once again, ties are broken by choosing a move at random. Nodes that have not been explored in the tree yet are prioritized before attempting to find a leaf node from a node that has already been explored.

The final move selection is not based on the UCB value, but on the direct estimate of the node value (number of win / number of simulations).

### Print Modes

`None`: Will not output anything other than the move selected at the end.

`Brief`: Will output the value for each of the immediate next moves (with Null for illegal moves) and the move selected at the end

`Verbose`: Will output the same as `Brief` but additionally will output the current values of the number of wins (wi) and number of simulations (ni) for each node in the search tree. When a leaf in the current tree is reached and a new node is added, it outputs “NODE ADDED”. For the rollout it will print the moves selected, and when a terminal node is reached, it prints the value “TERMINAL NODE VALUE: X” where X is -1, 0, or 1. Then it prints the updated values.

## Enhancements

### Alpha-Beta Pruning in Depth-Limited MinMax

Depth-Limited Minimax with Alpha-Beta Pruning optimizes the minimax algorithm by evaluating a smaller number of nodes in a search tree through pruning. Alpha beta pruning allows for the pruning of branches in the tree that will not affect the final outcome of the game. This significantly improves the performance of the algorithm by reducing the number of nodes that need to be evaluated. 

### Playing Against a Human Player

A human player can play against a specified algorithm. Accepted algorithms to choose from are `DLMM`, `PMCGS`, and `UCT`.

In order to run this feature, run the following:

`python3 humanPlay.py <name of algorithm>`