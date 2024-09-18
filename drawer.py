import pygame
from const import TILE_SIZE, WHITE, BLACK


# Function to draw a ghost with a rounded top and wavy bottom
def draw_ghost(surface, x, y, color):
    # Draw the ghost's head (rounded dome)
    pygame.draw.circle(surface, color, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), TILE_SIZE // 2)

    # Draw the ghost's body (rectangle)
    pygame.draw.rect(surface, color, (x, y + TILE_SIZE // 4, TILE_SIZE, TILE_SIZE // 2))

    # Draw the wavy bottom (legs)
    wave_radius = TILE_SIZE // 6
    for i in range(3):
        pygame.draw.circle(surface, color,
                           (x + i * (TILE_SIZE // 3) + wave_radius, y + TILE_SIZE // 2 + wave_radius),
                           wave_radius)

    # Draw eyes
    eye_radius = TILE_SIZE // 8
    pupil_radius = TILE_SIZE // 16
    eye_offset_x = TILE_SIZE // 4
    eye_offset_y = TILE_SIZE // 4

    # Left eye
    pygame.draw.circle(surface, WHITE, (x + eye_offset_x, y + eye_offset_y), eye_radius)
    pygame.draw.circle(surface, BLACK, (x + eye_offset_x, y + eye_offset_y), pupil_radius)

    # Right eye
    pygame.draw.circle(surface, WHITE, (x + TILE_SIZE - eye_offset_x, y + eye_offset_y), eye_radius)
    pygame.draw.circle(surface, BLACK, (x + TILE_SIZE - eye_offset_x, y + eye_offset_y), pupil_radius)
