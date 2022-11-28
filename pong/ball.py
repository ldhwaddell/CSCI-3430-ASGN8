import pygame
import math
import random


class Ball:
    """
    
    
    """
    # Class attributes
    MAX_X_VELOCITY = 4
    RADIUS = 9

    def __init__(self, colour, x, y):
        self.colour = colour
        # Set coords
        self.x = self.original_x = x
        self.y = self.original_y = y
        # Set direction
        self.x_velocity, self.y_velocity = self.create_direction()

    def get_angle(self, min, max, exclude):
        return math.radians(random.choice([n for n in range(min, max) if n not in exclude]))

    def get_side(self):
        dir = random.random()
        # If return is -1, ball heads left
        if dir <= 0.5:
            return -1
        # Otherwise, ball heads right
        else:
            return 1

    def create_direction(self):
        # Get and angle and a side to head towards
        angle = self.get_angle(-30, 30, [0])
        side = self.get_side()
        # For the angle, cos(x) will be the rise and sin(x) will be the run
        x = side * abs(math.cos(angle) * self.MAX_X_VELOCITY)
        y = math.sin(angle) * self.MAX_X_VELOCITY
        return x, y

    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.RADIUS)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_velocity, self.y_velocity = self.create_direction()
        self.x_velocity *= -1
