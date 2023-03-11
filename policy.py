import copy
import random

from GameMap import Map
from GameSearch import REC_WIDTH, REC_HEIGHT

REWARD = -0.01  # constant reward for non-terminal states
DISCOUNT = 0.99
MAX_ERROR = 10 ** (-3)

# dx, dy
# Down, Left, Up, Right
ACTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]


# SAME
def get_utility(maze, x, y, action):
    dx, dy = ACTIONS[action]
    new_x, new_y = x + dx, y + dy
    if not maze.isValid(new_x, new_y) or not maze.isMovable(new_x, new_y):
        return maze.map[y][x]
    else:
        return maze.map[new_y][new_x]


# SAME
def calculate_utility(maze, x, y, action):
    u = REWARD
    u += 0.1 * DISCOUNT * get_utility(maze, x, y, (action - 1) % 4)
    u += 0.8 * DISCOUNT * get_utility(maze, x, y, action)
    u += 0.1 * DISCOUNT * get_utility(maze, x, y, (action + 1) % 4)
    return u


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


def policy_evaluation(policy, maze_origin: Map):
    maze = copy.deepcopy(maze_origin)
    while True:
        next_maze = copy.deepcopy(maze)
        error = 0
        for y in maze.height:
            for x in maze.width:
                if not maze.isValid(x, y) or not maze.isMovable(x, y):
                    continue
                next_maze.map[y][x] = calculate_utility(maze, x, y, policy[y][x])
                error = max(error, abs(next_maze.map[y][x] - maze.map[y][x]))
        maze = next_maze
        if error < MAX_ERROR * (1 - DISCOUNT) / DISCOUNT:
            break
    return maze


def policy_iteration(maze, dest):
    policy = [[random.randint(0, 3) for j in range(REC_WIDTH)] for i in range(REC_HEIGHT)]  # construct a random policy
    print("During the policy iteration:\n")
    while True:
        maze = policy_evaluation(policy, maze)
        unchanged = True
        for y in range(maze.height):
            for x in range(maze.width):
                if not maze.isValid(x, y) or not maze.isMovable(x, y):
                    continue
                max_action, max_utility = None, -float('inf')
                for action in range(len(ACTIONS)):
                    utility = calculate_utility(maze, x, y, action)
                    if utility > max_utility:
                        max_action, max_utility = action, utility
                if max_utility > calculate_utility(maze, x, y, policy[y][x]):
                    policy[y][x] = max_action
                    unchanged = False
        if unchanged:
            break
        print_policy(maze, policy, dest)
    return policy
