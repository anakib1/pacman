from typing import Union, Literal


class Settings:
    # Higher value - less spaces
    wall_difficulty = 0.2
    # Higher value - more ghosts
    ghost_count = 3
    # Lower value - higher speed
    ghost_speed = 2
    # increasing difficulty left to right
    ghost_algo: Union[Literal["random"], Literal["dfs"], Literal["bfs"], Literal["group"]] = 'group'
    # settings level
    level = 1

    def __init__(self, level: int):
        self.level = level
        # Define the order of increasing difficulty
        ghost_algos = ["random", "dfs", "bfs", "group"]
        max_wall_difficulty = 0.5  # Maximum wall difficulty
        max_ghost_count = 10  # Maximum number of ghosts
        min_ghost_speed = 1  # Minimum ghost speed (higher speed)
        max_ghost_speed = 5  # Maximum ghost speed (slower speed)

        # Level thresholds (Adjusted to update algorithms earlier)
        wall_levels = 10  # Wall difficulty increases over 10 levels (was 20)
        algo_levels = len(ghost_algos) * 5  # Each algorithm changes every 5 levels (was 10)
        ghost_count_levels = 10  # Ghost count increases over 10 levels
        ghost_speed_levels = 10  # Ghost speed increases over 10 levels

        # Adjust wall difficulty
        if self.level <= wall_levels:
            wall_level = min(self.level, wall_levels)
            self.wall_difficulty = 0.2 + (wall_level / wall_levels) * (max_wall_difficulty - 0.2)
        else:
            self.wall_difficulty = max_wall_difficulty

        # Adjust ghost algorithm after wall difficulty reached max
        if self.level > wall_levels and self.level <= wall_levels + algo_levels:
            # Algorithm changes every 5 levels
            algo_index = (self.level - wall_levels - 1) // 5
            self.ghost_algo = ghost_algos[algo_index]
        elif self.level > wall_levels + algo_levels:
            self.ghost_algo = ghost_algos[-1]
        else:
            self.ghost_algo = "random"

        # Adjust ghost count after ghost algorithm reached max
        if self.level > wall_levels + algo_levels and self.level <= wall_levels + algo_levels + ghost_count_levels:
            ghost_count_level = self.level - wall_levels - algo_levels
            self.ghost_count = 3 + int((ghost_count_level / ghost_count_levels) * (max_ghost_count - 3))
        elif self.level > wall_levels + algo_levels + ghost_count_levels:
            self.ghost_count = max_ghost_count
        else:
            self.ghost_count = 3

        # Adjust ghost speed after ghost count reached max
        if self.level > wall_levels + algo_levels + ghost_count_levels:
            ghost_speed_level = self.level - (wall_levels + algo_levels + ghost_count_levels)
            ghost_speed_level = min(ghost_speed_level, ghost_speed_levels)
            self.ghost_speed = max_ghost_speed - int(
                (ghost_speed_level / ghost_speed_levels) * (max_ghost_speed - min_ghost_speed))
        else:
            self.ghost_speed = max_ghost_speed

        # Ensure values are within bounds
        self.wall_difficulty = min(max(self.wall_difficulty, 0.2), max_wall_difficulty)
        self.ghost_count = min(max(self.ghost_count, 3), max_ghost_count)
        self.ghost_speed = min(max(self.ghost_speed, min_ghost_speed), max_ghost_speed)

    def __str__(self):
        """Return a string representation of the current settings."""
        return (
            f"Level: {self.level}\n"
            f"Ghost Algorithm: {self.ghost_algo}\n"
            f"Wall Difficulty: {self.wall_difficulty:.2f}\n"
            f"Ghost Count: {self.ghost_count}\n"
            f"Ghost Speed: {self.ghost_speed}"
        )
