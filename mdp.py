import copy
import random

from memory_profiler import profile

from GameMap import Map, MAP_ENTRY_TYPE

REWARD_VALUE = -0.01  # constant reward for non-terminal states
DISCOUNT_VALUE = 0.99
MAX_ERROR_VALUE = 10 ** (-3)

REWARD_POLICY = -0.01  # constant reward for non-terminal states
DISCOUNT_POLICY = 0.99
MAX_ERROR_POLICY = 10 ** (-3)

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


def calculate_utility(maze, x, y, action, reward, discount):
    u = reward
    u += 0.1 * discount * get_utility(maze, x, y, (action - 1) % 4)
    u += 0.8 * discount * get_utility(maze, x, y, action)
    u += 0.1 * discount * get_utility(maze, x, y, (action + 1) % 4)
    return u


def value_iteration(maze_origin: Map, dest):
    maze = copy.deepcopy(maze_origin)
    print('During the value iteration: \n')
    maze.showNumericMap(dest)
    counter = 0
    loop_counter = 0
    while True:
        next_maze = copy.deepcopy(maze_origin)
        error = 0
        for y in range(maze.height):
            for x in range(maze.width):
                loop_counter += 4
                # if () this is the wall/goal
                if not maze.isValid(x, y) or not maze.isMovable(x, y) or (x, y) == dest:
                    continue
                # Bellman update
                next_maze.map[y][x] = max(
                    [calculate_utility(maze, x, y, action, REWARD_VALUE, DISCOUNT_VALUE) for action in
                     range(len(ACTIONS))])
                # next_maze.setMap(x, y, max([calculate_utility(maze, x, y, action) for action in range(len(ACTIONS))]))
                error = max(error, abs(next_maze.map[y][x] - maze.map[y][x]))
        maze = next_maze
        maze.showNumericMap(dest)
        counter += 1
        print('Iteration count: ', counter)
        if error < MAX_ERROR_VALUE * (1 - DISCOUNT_VALUE) / DISCOUNT_VALUE:
            break
    print('Loop count: ', loop_counter)
    return maze


def get_optimal_policy(maze: Map, dest):
    policy = [[-1] * maze.width for _ in range(maze.height)]
    for y in range(maze.height):
        for x in range(maze.width):
            if not maze.isValid(x, y) or not maze.isMovable(x, y) or (x, y) == dest:
                continue
            max_action, max_utility = None, -float('inf')
            for action in range(len(ACTIONS)):
                utility = calculate_utility(maze, x, y, action, REWARD_VALUE, DISCOUNT_VALUE)
                if utility > max_utility:
                    max_action, max_utility = action, utility
            policy[y][x] = max_action
    return policy


def print_policy(maze: Map, policy: list, dest):
    res = ''
    for y in range(len(policy)):
        res += '|'
        for x in range(len(policy[0])):
            if not maze.isValid(x, y) or not maze.isMovable(x, y):
                val = '#'
            elif (x, y) == dest:
                val = 'GOAL'
            else:
                val = ["v", "<", "^", ">"][policy[y][x]]
            res += " " + val[:5].ljust(5) + " |"  # format
        res += '\n'
    print(res)


def draw_policy_on_maze(maze: Map, policy: list, source, dest):
    x = source[0]
    y = source[1]
    while (x, y) != dest:
        x, y = x + ACTIONS[policy[y][x]][0], y + ACTIONS[policy[y][x]][1]
        maze.setMap(x, y, MAP_ENTRY_TYPE.MAP_PATH)
    print('Draw path finished')


def policy_evaluation(policy, maze_origin: Map, dest, loop_counter):
    maze = copy.deepcopy(maze_origin)
    while True:
        next_maze = copy.deepcopy(maze_origin)
        error = 0
        for y in range(maze.height):
            for x in range(maze.width):
                loop_counter += 1
                if not maze_origin.isValid(x, y) or not maze_origin.isMovable(x, y) or (x, y) == dest:
                    continue
                next_maze.map[y][x] = calculate_utility(maze, x, y, policy[y][x], REWARD_POLICY, DISCOUNT_POLICY)
                error = max(error, abs(next_maze.map[y][x] - maze.map[y][x]))
        maze = next_maze
        if error < MAX_ERROR_POLICY * (1 - DISCOUNT_VALUE) / DISCOUNT_VALUE:
            break
    return maze, loop_counter


def policy_iteration(maze: Map, dest):
    policy = [[random.randint(0, 3) for _ in range(maze.width)] for _ in
              range(maze.height)]  # construct a random policy
    print("During the policy iteration:\n")
    counter = 0
    loop_counter = 0
    while True:
        counter += 1
        maze, loop_counter = policy_evaluation(policy, maze, dest, loop_counter)
        unchanged = True
        for y in range(maze.height):
            for x in range(maze.width):
                if not maze.isValid(x, y) or not maze.isMovable(x, y) or (x, y) == dest:
                    continue
                max_action, max_utility = None, -float('inf')
                for action in range(len(ACTIONS)):
                    loop_counter += 1
                    utility = calculate_utility(maze, x, y, action, REWARD_POLICY, DISCOUNT_POLICY)
                    if utility > max_utility:
                        max_action, max_utility = action, utility
                if max_utility > calculate_utility(maze, x, y, policy[y][x], REWARD_POLICY, DISCOUNT_POLICY):
                    policy[y][x] = max_action
                    unchanged = False
        if unchanged:
            break
        print_policy(maze, policy, dest)
        print('Iteration times: ', counter)
    print('Loop count: ', loop_counter)
    return policy
