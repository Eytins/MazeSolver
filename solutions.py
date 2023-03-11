from GameMap import MAP_ENTRY_TYPE
from collections import deque


class SearchEntry:
    def __init__(self, x, y, g_cost, f_cost=0, pre_entry=None):
        self.x = x
        self.y = y
        # cost move form start entry to this entry
        self.g_cost = g_cost
        self.f_cost = f_cost
        self.pre_entry = pre_entry

    def get_pos(self):
        return self.x, self.y


def a_star_search(maze, source, dest):
    def get_fast_position(open_list):
        fast = None
        for entry in open_list.values():
            if fast is None:
                fast = entry
            elif fast.f_cost > entry.f_cost:
                fast = entry
        return fast

    def get_positions(maze, location):
        offsets = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        pos_list = []
        for offset in offsets:
            x, y = (location.x + offset[0], location.y + offset[1])
            if maze.isValid(x, y) and maze.isMovable(x, y):
                pos_list.append((x, y))
        return pos_list

    # check if the position is in list
    def is_in_list(list, pos):
        if pos in list:
            return list[pos]
        return None

    def cal_heuristic(pos, dest):
        return abs(dest.x - pos[0]) + abs(dest.y - pos[1])

    def get_move_cost(location, pos):
        if location.x != pos[0] and location.y != pos[1]:
            return 1.4
        else:
            return 1

    def add_adjacent_positions(maze, cur_loc, dest, open_list, closed_list):
        pos_list = get_positions(maze, cur_loc)
        for pos in pos_list:
            # if position is already in closed_list, do nothing
            if is_in_list(closed_list, pos) is None:
                find_entry = is_in_list(open_list, pos)
                h_cost = cal_heuristic(pos, dest)
                g_cost = cur_loc.g_cost + get_move_cost(cur_loc, pos)
                if find_entry is None:
                    # if position is not in open_list, add it to open_list
                    open_list[pos] = SearchEntry(pos[0], pos[1], g_cost, g_cost + h_cost, cur_loc)
                elif find_entry.g_cost > g_cost:
                    find_entry.g_cost = g_cost
                    find_entry.f_cost = g_cost + h_cost
                    find_entry.pre_entry = cur_loc

    open_list = {}
    closed_list = {}
    location = SearchEntry(source[0], source[1], 0.0)
    dest = SearchEntry(dest[0], dest[1], 0.0)
    open_list[source] = location
    counter = 0
    while True:
        counter += 1
        location = get_fast_position(open_list)
        if location is None:
            print("can't find valid path")
            break
        if location.x == dest.x and location.y == dest.y:
            break
        closed_list[location.get_pos()] = location
        open_list.pop(location.get_pos())
        add_adjacent_positions(maze, location, dest, open_list, closed_list)
    while location is not None:
        maze.setMap(location.x, location.y, MAP_ENTRY_TYPE.MAP_PATH)
        location = location.pre_entry
    print('loop times: ', counter)


def bfs_search(maze, source, dest):
    # Define directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Create a queue and add the source location
    queue = deque()
    queue.append(source)

    # Create a dictionary to store predecessors and mark source as visited
    predecessors = {}
    predecessors[source] = None
    visited = set()
    visited.add(source)

    counter = 0
    # Keep searching until the queue is empty or the destination is found
    while queue:
        counter += 1
        # Dequeue next position from the queue
        curr_pos = queue.popleft()

        # If destination is found, break
        if curr_pos == dest:
            break

        # Explore all neighboring positions
        for direction in directions:
            x, y = curr_pos[0] + direction[0], curr_pos[1] + direction[1]
            new_pos = x, y

            # Check if position is valid and not visited
            if maze.isValid(x, y) and maze.isMovable(x, y) and new_pos not in visited:
                predecessors[new_pos] = curr_pos
                visited.add(new_pos)
                queue.append(new_pos)

    # If destination was not found, return None
    if dest not in predecessors:
        print("Can't find valid path.")
        return None

    # Mark the path from destination to source on the maze
    curr_pos = dest
    print('loop times: ', counter)
    while curr_pos is not None:
        maze.setMap(curr_pos[0], curr_pos[1], MAP_ENTRY_TYPE.MAP_PATH)
        curr_pos = predecessors[curr_pos]

    return maze


def dfs_search(maze, source, dest):
    # Define directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Create a stack and add the source location
    stack = [source]

    # Create a dictionary to store predecessors and mark source as visited
    predecessors = {}
    predecessors[source] = None
    visited = set()
    visited.add(source)

    counter = 0
    # Keep searching until the stack is empty or the destination is found
    while stack:
        counter += 1
        # Pop the top position from the stack
        curr_pos = stack.pop()

        # If destination is found, break
        if curr_pos == dest:
            break

        # Explore all neighboring positions in reverse order
        for direction in directions[::-1]:
            x, y = curr_pos[0] + direction[0], curr_pos[1] + direction[1]
            new_pos = x, y

            # Check if position is valid and not visited
            if maze.isValid(x, y) and maze.isMovable(x, y) and new_pos not in visited:
                predecessors[new_pos] = curr_pos
                visited.add(new_pos)
                stack.append(new_pos)

    # If destination was not found, return None
    if dest not in predecessors:
        print("Can't find valid path.")
        return None

    print('loop times: ', counter)

    # Mark the path from destination to source on the maze
    curr_pos = dest
    while curr_pos is not None:
        maze.setMap(curr_pos[0], curr_pos[1], MAP_ENTRY_TYPE.MAP_PATH)
        curr_pos = predecessors[curr_pos]

    return maze
