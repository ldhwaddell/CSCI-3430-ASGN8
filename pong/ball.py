import pygame


class Ball:
    """"""
    # Class attributes
    MAX_X_VELOCITY = 4
    RADIUS = 9

    def __init__(self, colour, x, y):
        self.colour = colour
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.x_velocity = self.MAX_X_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.RADIUS)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0
        self.x_velocity *= -1
