import pygame
import random
import sys
from utils import is_available
from const import *
from algo import dfs, bfs, random_move
from drawer import draw_ghost
from models import Player, Ghost
from generate import generate_maze
from settings import Settings
from scoreboard import load_high_score, dump_high_score

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman with Random Maze and DFS Ghosts")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", FONT_SIZE)

# Initialize High Score
LEVEL = 27
high_score = load_high_score(LEVEL)
settings = Settings(LEVEL)
print(f'Using settings: {settings}')


# Main game function
def main():
    global high_score
    maze = generate_maze(ROWS, COLS, settings)

    # Find a starting position for Pacman (player)
    while True:
        player_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if maze[player_pos[0]][player_pos[1]] == 0:
            break
    player = Player(*player_pos)

    # Initialize pellets (points)
    pellets = [(i, j) for i in range(ROWS) for j in range(COLS) if maze[i][j] == 0]

    # Initialize score
    score = 0

    # Initialize ghosts
    num_ghosts = settings.ghost_count
    ghosts = []
    for i in range(num_ghosts):
        while True:
            ghost_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
            if maze[ghost_pos[0]][ghost_pos[1]] == 0 and ghost_pos != player_pos:
                if all(ghost_pos != (g.x, g.y) for g in ghosts):
                    break
        ghost = Ghost(ghost_pos[0], ghost_pos[1], GHOST_COLORS[i % len(GHOST_COLORS)], speed=settings.ghost_speed)
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
        if is_available(new_x, new_y, maze):
            player.x, player.y = new_x, new_y

        # Collect pellets
        if (player.x, player.y) in pellets:
            pellets.remove((player.x, player.y))
            score += 10  # Add points for each pellet collected

        # Ghost movement using BFS
        for i, ghost in enumerate(ghosts):
            if ghost.move_counter >= ghost.speed:
                next_move = None
                if settings.ghost_algo == 'random':
                    next_move = random_move(ghost.x, ghost.y, maze)
                elif settings.ghost_algo == 'bfs':
                    path = bfs(maze, (ghost.x, ghost.y), (player.x, player.y))
                    if path:
                        next_move = path[0]
                elif settings.ghost_algo == 'dfs':
                    path = dfs(maze, (ghost.x, ghost.y), (player.x, player.y))
                    if path:
                        next_move = path[0]
                elif settings.ghost_algo == 'group':
                    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
                    direction = directions[i % 4]
                    target = (player.x + direction[0], player.y + direction[1])
                    if not is_available(*target, maze):
                        target = (player.x, player.y)
                    path = bfs(maze, (ghost.x, ghost.y), target)
                    if path:
                        next_move = path[0]

                if next_move is not None:
                    ghost.x, ghost.y = next_move
                ghost.move_counter = 0
            else:
                ghost.move_counter += 1

        # Check collision
        for ghost in ghosts:
            if (player.x, player.y) == (ghost.x, ghost.y):
                print(f"Game Over. Score: {score}")
                dump_high_score(LEVEL, score)
                running = False

        # Drawing
        screen.fill(BLACK)

        # Draw maze
        for i in range(ROWS):
            for j in range(COLS):
                if maze[i][j] == 1:
                    pygame.draw.rect(screen, WALL_COLOR, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw pellets
        for pellet in pellets:
            pygame.draw.circle(screen, PELLET_COLOR,
                               (pellet[1] * TILE_SIZE + TILE_SIZE // 2, pellet[0] * TILE_SIZE + TILE_SIZE // 2),
                               TILE_SIZE // 4)

        # Draw player
        pygame.draw.circle(screen, PACMAN_COLOR,
                           (player.y * TILE_SIZE + TILE_SIZE // 2, player.x * TILE_SIZE + TILE_SIZE // 2),
                           TILE_SIZE // 2)

        # Draw ghosts using the new ghost shape
        for ghost in ghosts:
            draw_ghost(screen, ghost.y * TILE_SIZE, ghost.x * TILE_SIZE, ghost.color)

        # Update high score
        if score > high_score:
            high_score = score

        # Display score and high score
        score_text = font.render(f"Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        level_text = font.render(f"Level: {LEVEL}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (WIDTH - 200, 10))
        screen.blit(level_text, (WIDTH // 2, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)
