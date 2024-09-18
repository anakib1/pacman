from const import ROWS, COLS


def is_available(x, y, maze):
    return 0 <= x < ROWS and 0 <= y < COLS and maze[x][y] == 0


def is_wall(x, y, maze):
    return 0 <= x < ROWS and 0 <= y < COLS and maze[x][y] == 1
