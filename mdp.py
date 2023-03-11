from GameMap import Map

REWARD = -0.01  # constant reward for non-terminal states
DISCOUNT = 0.99
MAX_ERROR = 10 ** (0)

# dx, dy
# Down, Left, Up, Right
ACTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]


# Get the utility of the state reached by performing the given action from the given state
def get_utility(maze, x, y, action):
    dx, dy = ACTIONS[action]
    new_x, new_y = x + dx, y + dy
    if not maze.isValid(new_x, new_y) or not maze.isMovable(new_x, new_y):
        return maze.map[y][x]
    else:
        return maze.map[new_y][new_x]


def calculate_utility(maze, x, y, action):
    u = REWARD
    u += 0.1 * DISCOUNT * get_utility(maze, x, y, (action - 1) % 4)
    u += 0.8 * DISCOUNT * get_utility(maze, x, y, action)
    u += 0.1 * DISCOUNT * get_utility(maze, x, y, (action + 1) % 4)
    return u


def value_iteration(maze_origin: Map, source, dest):
    maze = maze_origin
    print('During the value iteration: \n')
    maze.showNumericMap()
    counter = 0
    while True:
        next_maze = maze
        error = 0
        for y in range(maze.height):
            for x in range(maze.width):
                # if () this is the wall/goal
                if not maze.isValid(x, y) or not maze.isMovable(x, y) or (x, y) == dest:
                    continue
                # Bellman update
                next_maze.map[y][x] = max([calculate_utility(maze, x, y, action) for action in range(len(ACTIONS))])
                # next_maze.setMap(x, y, max([calculate_utility(maze, x, y, action) for action in range(len(ACTIONS))]))
                error = max(error, abs(next_maze.map[y][x] - maze.map[y][x]))
        maze = next_maze
        maze.showNumericMap()
        counter += 1
        print('Iteration times: ', counter)
        if error < MAX_ERROR * (1 - DISCOUNT) / DISCOUNT:
            break
    return maze
