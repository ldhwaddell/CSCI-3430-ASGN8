import math
import random

import pygame


class Ball:
    """
    A class to represent the ball object. 

    :param colour: The colour of the ball
    :param x: The x position of the ball
    :param y: The y position of the ball
    """
    # Class attributes
    MAX_X_VELOCITY = 5
    RADIUS = 9

    def __init__(self, colour, x, y):
        self.colour = colour
        # Set coords
        self.x = self.original_x = x
        self.y = self.original_y = y
        # Set direction
        self.x_velocity, self.y_velocity = self.create_direction()

    def get_angle(self, min, max, exclude):
        """
        Picks a random angle in radians to send the ball on that is not in the list
        of excluded angles.

        :param min: The minimum value of the angle
        :param max: The maximum value of the angle
        :param exclude: Points to exclude from the angle picking
        """
        return math.radians(random.choice([i for i in range(min, max) if i not in exclude]))

    def get_side(self):
        """
        Returns a direction to send the ball on, whether it is -1 or 1
        """
        dir = random.random()
        # If return is -1, ball heads left
        if dir <= 0.5:
            return -1
        # Otherwise, ball heads right
        else:
            return 1

    def create_direction(self):
        """
        Generates the x and y coordinates that the ball will start our on.

        After getting an angle and a side to point towards, the cos of that angle is the 
        change in x that the ball should move each game loop. 

        The sin of this angle is the change in y that the ball should move each game loop
        """
        # Get and angle and a side to head towards
        angle = self.get_angle(-30, 30, [0])
        side = self.get_side()
        # For the angle, cos(x) will be the run and sin(x) will be the rise
        x = side * abs(math.cos(angle) * self.MAX_X_VELOCITY)
        y = math.sin(angle) * self.MAX_X_VELOCITY
        return x, y

    def draw(self, win):
        """
        Draws the ball on the screen

        :param win: The pygame window object
        """
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.RADIUS)

    def move(self):
        """
        Moves the ball by the given amount
        """

        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        """
        Resets the ball to original position
        """
        self.x = self.original_x
        self.y = self.original_y
        self.x_velocity, self.y_velocity = self.create_direction()
        self.x_velocity *= -1
