
# Game entities
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ghost:
    def __init__(self, x, y, color, speed):  # Default speed (lower than player)
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.move_counter = 0  # Counter to keep track of movement frequency
