import heapq
from collections import deque

class Tiles:
    def __init__(self, start_state):
        self.start_state = tuple(start_state)
        self.end_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        self.moves_states = {
            0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
            3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
            6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
        }

    def heuristic(self, state):
        distance = 0
        for i, val in enumerate(state):
            if val != 0:
                end_state = self.end_state.index(val)
                distance += abs(end_state // 3 - i // 3) + abs(end_state % 3 - i % 3)  # Manhattan distance

                if i > 0 and state[i - 1] != 0:  # Reversal!
                    if (state[i] > state[i - 1] and self.end_state.index(state[i]) < self.end_state.index(
                            state[i - 1])) or \
                            (state[i] < state[i - 1] and self.end_state.index(state[i]) > self.end_state.index(
                                state[i - 1])):
                        distance += 1  # The reversal penalty
        return distance

    def bfs(self):
        queue = deque([(self.start_state, [])])
        visited = set()
        nodes_expanded = 0

        while queue:
            state, path = queue.popleft()

            if state in visited:
                continue

            visited.add(state)
            nodes_expanded += 1

            if state == self.end_state:
                return nodes_expanded, path

            for new_state, tile_moved in self.expand_successors(state):
                if new_state not in visited:
                    queue.append((new_state, path + [tile_moved]))

        return -1, []

    def expand_successors(self, state):
        successors = []
        empty_index = state.index(0)  # Find the index of the empty tile (labeled as 0)

        for move in self.moves_states[empty_index]:
            new_state = list(state)  # Convert tuple to a mutable list
            new_state[empty_index], new_state[move] = new_state[move], new_state[empty_index]  # Swap tiles
            successors.append((tuple(new_state), state[move]))

        return successors

    def a_star(self):
        priority_queue = [(self.heuristic(self.start_state), 0, self.start_state, [])]
        visited = set()
        nodes_expanded = 0

        while priority_queue:
            estimated_value, cost, state, path = heapq.heappop(priority_queue)

            if state in visited:
                continue

            visited.add(state)
            nodes_expanded += 1

            if state == self.end_state:
                return nodes_expanded, path

            for new_state, tile_moved in self.expand_successors(state):
                if new_state not in visited:
                    new_cost = cost + 1
                    heapq.heappush(priority_queue,
                                   (new_cost + self.heuristic(new_state), new_cost, new_state, path + [tile_moved]))

        return -1, []

if __name__ == "__main__":
    input_state = list(map(int, input("Enter the initial state (space-separated numbers): ").strip().split()))
    puzzle = Tiles(input_state)

    print("BFS")
    nodes_expanded, path = puzzle.bfs()
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Path: {path}")


    print("\nA*")
    nodes_expanded, path = puzzle.a_star()
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Path: {path}")
