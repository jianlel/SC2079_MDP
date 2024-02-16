import numpy as np
import heapq

# Define constants
ACTION_COST = 1  # Cost of taking an action (e.g., moving forward)
OBS_COST = 1000  # Cost of colliding with an obstacle
RS_COST_SCALE = 10  # Scale factor for Reed-Shepp path length

# Define actions (moving forward, turning left, turning right)
ACTIONS = [(1, 0), (0, -1), (0, 1)]  # Move forward, turn left, turn right

# Define grid size and obstacle locations (0 = free, 1 = obstacle)
GRID_SIZE = (10, 10)
OBSTACLES = {(3, 3), (3, 4), (4, 3)}

# Define start and goal positions
START = (0, 0)
GOAL = (9, 9)

# Reed-Shepp path generation function (simplified)
def reeds_shepp_path_cost(start, end):
    # Calculate Reed-Shepp path length (simplified, not the exact algorithm)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    return np.sqrt(dx**2 + dy**2) * RS_COST_SCALE

# A* search algorithm
def astar_search(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))  # (cost, state)
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current_state = heapq.heappop(frontier)

        if current_state == goal:
            break

        for action in ACTIONS:
            next_state = (current_state[0] + action[0], current_state[1] + action[1])

            # Check if next state is within bounds and not colliding with an obstacle
            if 0 <= next_state[0] < GRID_SIZE[0] and 0 <= next_state[1] < GRID_SIZE[1] and next_state not in OBSTACLES:
                new_cost = cost_so_far[current_state] + ACTION_COST

                # Reed-Shepp path cost
                rs_cost = reeds_shepp_path_cost(current_state, next_state)
                new_cost += rs_cost

                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    cost_so_far[next_state] = new_cost
                    priority = new_cost + reeds_shepp_path_cost(next_state, goal)  # A* heuristic
                    heapq.heappush(frontier, (priority, next_state))
                    came_from[next_state] = current_state

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path

# Main function
def main():
    path = astar_search(START, GOAL)
    print("Optimal Path:", path)

if __name__ == "__main__":
    main()
