import pygame


class Paddle:
    # Class attributes
    VELOCITY = 4  # Move 4 units at a time
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, colour, x, y):
        self.colour = colour
        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, win):
        pygame.draw.rect(win, self.colour,
                         (self.x, self.y, self.WIDTH, self.HEIGHT))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
