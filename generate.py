from typing import Literal, Union
from utils import is_wall
import random


# Maze generation using recursive backtracking with more open spaces
def generate_maze(rows, cols, settings):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = []

    # Starting cell
    current_cell = (random.randint(0, rows - 1), random.randint(0, cols - 1))
    maze[current_cell[0]][current_cell[1]] = 0
    stack.append(current_cell)

    while stack:
        current_cell = stack[-1]
        neighbors = []

        # Check unvisited neighbors
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Up, Down, Left, Right
        random.shuffle(directions)  # Randomize directions
        for dx, dy in directions:
            nx, ny = current_cell[0] + dx, current_cell[1] + dy
            if is_wall(nx, ny, maze):
                neighbors.append((nx, ny))

        if neighbors:
            next_cell = random.choice(neighbors)
            maze[next_cell[0]][next_cell[1]] = 0
            wall_x = current_cell[0] + (next_cell[0] - current_cell[0]) // 2
            wall_y = current_cell[1] + (next_cell[1] - current_cell[1]) // 2
            maze[wall_x][wall_y] = 0
            stack.append(next_cell)
        else:
            stack.pop()

    # Remove additional walls to create more open space
    wall_removal_probability = 1 - settings.wall_difficulty  # Adjust this value between 0 and 1
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:
                if random.random() < wall_removal_probability:
                    maze[i][j] = 0

    return maze
