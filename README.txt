
#########
8-puzzle problem -

Overview:
The 8-puzzle is a sliding puzzle that is played on a 3-by-3 grid with 8 square tiles labeled 1 through 8, plus a blank square.
The goal is to rearrange the tiles so that they are in row-major order, using as few moves as possible.
You are permitted to slide tiles either horizontally or vertically into the blank square.(1)
In our case the end state will be when the grid is arranged so the empty tile (labeled as 0) is in the top-left corner and rest of the tiles
are arranged after it in ascending order in each row.we will do it by using BFS and A* (A star) algorithms.

1.Program structure by functions -

I. __init__:
    This is the constructor of the program , here we defined the start state (by the user input),the end state (as described on the overview)
    and the moves states (legal moves)

II. heuristic:
    Computes the heuristic estimate for a given state using the heuristic function.
    iterates over each tile and calculates the absolute differences between its current position and its goal position.
    if two following tiles are reversal compared to the end state, it will add a penalty cost by increasing the heuristic value.

III. BFS:
    Initializes a queue with the initial state and an empty path. using a visited of data structure set to track states and prevent revisiting them.
    iteratively dequeues a state and checks if its the end state and expands the current state by generating its successors and enqueues them if they haven’t been visited.
    finally, the algorithm returns the number of expanded nodes and the sequence of tile movements leading to the solution.

IV.expand_successors:
    Finds the index of the empty tile (0) in the current state.determines the possible moves based on the predefined moves_states dictionary(as described on the constructor).
    generates new states by swapping the empty tile with each valid neighbor(with a legal move).
    finally,the function returns a list of tuples, each containing a new state and the tile that was moved.

V.A* (A Star):
    Initializes a priority queue where states are ordered by their total estimated cost (cost so far + heuristic value).
    uses a visited set to track states and prevent revisiting them.
    iteratively pop the state with the lowest estimated cost.
    finally,the algorithm checks if the state is the goal if it is so returns the number of expanded nodes and the solution path.
    else,expands the state by generating successors and inserts them into the priority queue with their updated cost.

2.Definition of the representation that selected to the problem-

I.States representation:
    A state in our program is presented by a tuple.when the start state is inputted by a user and translated into a tuple,and the end state defined as
    a tuple by the programmer in the constructor.

II + III.Moves and Transition model -
    The transition model in the program is moving the empty tile (labeled as 0) by maximum into 4 directions(left,right,down,up)
    by swapping him with the tile that next to it on the given direction.(cannot be swapped out the board)
    the possible moves are mentioned on the moves_states as a dictionary and a list so every key (in his current position) has a list which tiles are his successors

3.Heuristics-
An Heuristic function constitutes an estimated cost(=estimation,inaccurate index) of getting from the state that in the node to the end state,and so it guides the search.(2)

I.Heuristics description:
    Manhattan Distance plus Reversal Penalty Search.
        The chosen heuristic is the Manhattan distance, calculated as the sum of the horizontal and vertical distances between each tile and its end position.
        plus a reversal penalty is applied to penalize cases where two numbers appear in the reverse order compared to the end state.(2.1)

II.Based Idea:
    The Heuristic is based on a Manhattan distance.
    "The Manhattan Distance of one tile is the number of moves that would be required to move that tile to its goal
    location if it could move over any of the other tiles."(2.2)

III.Consistent and admissible:
    Each move on the board between 2 tiles changes the heuristic estimate by at most the cost of the move - according to the moves states
    the cost of that move is 1.
    Therefore, the function is consistent so the function is admissible too.

IV.Example with the described start state:
    for the start state that described (1 4 0 5 8 2 3 6 7 )
    the algorithm using the given heuristic function will print:
        A*
        Nodes expanded: 13
        Path: [2, 8, 5, 3, 6, 7, 8, 5, 4, 1]

4.Optimally-
    A optimal solution is a solution with the minimal cost among the whole possibles solutions.(3)

I.BFS:
    Provides the optimal solution because it always finds the shortest solution since it explores all states at a given depth before proceeding to deeper levels.

II.A* (A Star):
    Since the algorithm is consistent so the algorithms finds the optimal solution(4)








