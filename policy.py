import copy

from GameMap import Map, MAP_ENTRY_TYPE

REWARD = -0.01  # constant reward for non-terminal states
DISCOUNT = 0.99
MAX_ERROR = 10 ** (-2)

# dx, dy
# Down, Left, Up, Right
ACTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]


# Get current state reward + DISCOUNT * (next state reward)
def get_state_utility(maze, x, y, dx, dy):
    if not maze.isValid(x + dx, y + dy) or not maze.isMovable(x + dx, y + dy):
        return maze.map[y][x]
    else:
        return DISCOUNT * maze.map[y + dy][x + dx] + REWARD


def calculate_utility(maze, x, y, policy):
    return sum([get_state_utility(maze, x, y, ACTIONS[p][0], ACTIONS[p][1]) for p in policy])


def policy_iteration(maze_origin: Map, dest):
    maze = copy.deepcopy(maze_origin)
    print('During the policy iteration: \n')
    maze.showNumericMap(dest)
    counter = 0
    policy = [[0] * maze.width for _ in range(maze.height)]
    while True:
        # policy Evaluation
        while True:
            next_maze = copy.deepcopy(maze)
            error = 0
            for y in range(maze.height):
                for x in range(maze.width):
                    if not maze.isValid(x, y) or not maze.isMovable(x, y) or (x, y) == dest:
                        continue
                    next_maze.map[y][x] = calculate_utility(maze, x, y, [policy[y][x]])
                    error = max(error, abs(next_maze.map[y][x] - maze.map[y][x]))

            maze = next_maze

            if error < MAX_ERROR * (1 - DISCOUNT) / DISCOUNT:
                break

        # policy improvement
        unchanged = True
        for y in range(maze.height):
            for x in range(maze.width):
                if not maze.isValid(x, y) or not maze.isMovable(x, y) or (x, y) == dest:
                    continue

                old_action = policy[y][x]
                best_action, best_utility = None, -float('inf')
                for action in range(len(ACTIONS)):
                    utility = calculate_utility(maze, x, y, [action])
                    if utility > best_utility:
                        best_action, best_utility = action, utility

                if best_action != old_action:
                    policy[y][x] = best_action
                    unchanged = False

        maze.showNumericMap(dest)
        counter += 1
        print('Iteration times: ', counter)

        if unchanged:
            break
    return maze, policy
