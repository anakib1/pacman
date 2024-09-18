import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 20
ROWS = HEIGHT // TILE_SIZE
COLS = WIDTH // TILE_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLORS = [(255, 0, 0), (255, 128, 0), (0, 255, 255), (255, 192, 203)]  # Red, Orange, Cyan, Pink
WALL_COLOR = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman with Random Maze and DFS Ghosts")
clock = pygame.time.Clock()

# Maze generation using recursive backtracking with more open spaces
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = []

    # Starting cell
    current_cell = (random.randint(0, rows-1), random.randint(0, cols-1))
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
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
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
    wall_removal_probability = 0.2  # Adjust this value between 0 and 1
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:
                if random.random() < wall_removal_probability:
                    maze[i][j] = 0

    return maze

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
            if (0 <= nx < ROWS and 0 <= ny < COLS and
                maze[nx][ny] == 0 and (nx, ny) not in visited):
                stack.append((nx, ny))
                parent[(nx, ny)] = current
    return []

# Game entities
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# Main game function
def main():
    maze = generate_maze(ROWS, COLS)

    # Find a starting position for Pacman (player)
    while True:
        player_pos = (random.randint(0, ROWS -1), random.randint(0, COLS -1))
        if maze[player_pos[0]][player_pos[1]] == 0:
            break
    player = Player(*player_pos)

    # Initialize ghosts
    NUM_GHOSTS = 4
    ghosts = []
    for i in range(NUM_GHOSTS):
        while True:
            ghost_pos = (random.randint(0, ROWS -1), random.randint(0, COLS -1))
            if maze[ghost_pos[0]][ghost_pos[1]] == 0 and ghost_pos != player_pos:
                # Ensure ghosts don't start at the same position
                if all(ghost_pos != (g.x, g.y) for g in ghosts):
                    break
        ghost = Ghost(ghost_pos[0], ghost_pos[1], GHOST_COLORS[i % len(GHOST_COLORS)])
        ghosts.append(ghost)

    # Game loop
    running = True
    while running:
        clock.tick(10)  # FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx, dy = 0, -1
        elif keys[pygame.K_RIGHT]:
            dx, dy = 0, 1
        elif keys[pygame.K_UP]:
            dx, dy = -1, 0
        elif keys[pygame.K_DOWN]:
            dx, dy = 1, 0

        new_x, new_y = player.x + dx, player.y + dy
        if 0 <= new_x < ROWS and 0 <= new_y < COLS and maze[new_x][new_y] == 0:
            player.x, player.y = new_x, new_y

        # Ghost movement using DFS
        for ghost in ghosts:
            path = dfs(maze, (ghost.x, ghost.y), (player.x, player.y))
            if path:
                next_move = path[0]
                ghost.x, ghost.y = next_move

        # Check collision
        for ghost in ghosts:
            if (player.x, player.y) == (ghost.x, ghost.y):
                print("Game Over")
                running = False

        # Drawing
        screen.fill(BLACK)
        for i in range(ROWS):
            for j in range(COLS):
                if maze[i][j] == 1:
                    pygame.draw.rect(screen, WALL_COLOR,
                                     (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        # Draw player
        pygame.draw.circle(screen, PACMAN_COLOR,
                           (player.y*TILE_SIZE + TILE_SIZE//2,
                            player.x*TILE_SIZE + TILE_SIZE//2),
                           TILE_SIZE//2)
        # Draw ghosts
        for ghost in ghosts:
            pygame.draw.circle(screen, ghost.color,
                               (ghost.y*TILE_SIZE + TILE_SIZE//2,
                                ghost.x*TILE_SIZE + TILE_SIZE//2),
                               TILE_SIZE//2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
