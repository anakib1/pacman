from const import ROWS, COLS
from collections import deque
import random
from utils import is_available, is_wall


# DFS pathfinding for ghosts
def dfs(maze, start, goal):
    stack = [start]
    visited = set()
    parent = {}
    while stack:
        current = stack.pop()
        if current == goal:
            # Reconstruct path
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path
        visited.add(current)
        x, y = current
        # Check neighbors (Up, Down, Left, Right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if is_available(nx, ny, maze) and (nx, ny) not in visited:
                stack.append((nx, ny))
                parent[(nx, ny)] = current
    return []


def bfs(maze, start, goal):
    queue = deque([start])
    visited = set()
    parent = {}
    visited.add(start)

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if is_available(nx, ny, maze) and (nx, ny) not in visited:
                queue.append((nx, ny))
                parent[(nx, ny)] = current
                visited.add((nx, ny))

    return []  # No path found


def random_move(x, y, maze):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    random.shuffle(directions)  # Randomize movement
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if is_available(new_x, new_y, maze):
            return new_x, new_y
