from paddle import Paddle
from ball import Ball

import pygame
pygame.init()


class gameInfo:
    # Class Attributes
    TURQUOISE = (0, 255, 255)
    GOLD = (255, 215, 0)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score


class Game:
    def __init__(self, window, width, height):
        self.width = width
        self.height = height
        self.window = window

        # Instantiate paddles and ball
        self.left_paddle = Paddle(self.RED, 10, self.height //
                             2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(self.TURQUOISE, self.width - 10 -
                              Paddle.WIDTH, self.height // 2 - Paddle.HEIGHT // 2)

        self.ball

        
