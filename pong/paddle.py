import pygame


class Paddle:
    """
    A class to represent the paddle object. 

    :param colour: The colour of the paddle
    :param x: The x position of the paddle
    :param y: The y position of the paddle
    
    """
    # Class attributes
    VELOCITY = 4  # Move 4 units at a time
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, colour, x, y):
        self.colour = colour
        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, win):
        """
        Draw the paddle on the given window.

        :param win: The window to draw on
        """
        pygame.draw.rect(win, self.colour,
                         (self.x, self.y, self.WIDTH, self.HEIGHT))

    def move(self, up=True):
        """
        Move the paddle up or down.

        :param up: True if moving up, False if moving down
        """
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        """
        Reset the paddle position to its original position.
        """
        self.x = self.original_x
        self.y = self.original_y
