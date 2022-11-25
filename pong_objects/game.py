from .paddle import Paddle
from .ball import Ball

from .utils import colours

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
        self.left_hits = 0
        self.right_hits = 0
        self.left_score = 0
        self.right_score = 0

        # Instantiate paddles and ball
        self.left_paddle = Paddle(colours["red"], 10, self.height //
                                  2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(colours["turquoise"], self.width - 10 -
                                   Paddle.WIDTH, self.height // 2 - Paddle.HEIGHT // 2)

        self.ball = Ball(colours["gold"], self.width // 2, self.height // 2)

    def draw_dividers(self):
        separator = self.height // 20
        for i in range(10, self.height, separator):
            if i % 2 == 1:
                continue
            else:
                pygame.draw.rect(
                    self.window, colours["white"], (self.width // 2 - 5, i, 10, separator))

    def check_collision(self):
        # Pull in the ball and paddle objects for current game
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        # If the ball hits the bottom or top of the window, reverse its y direction
        if ball.y + ball.radius >= self.height:
            ball.y_velocity *= -1
        elif ball.y - ball.radius <= 0:
            ball.y_velocity *= -1

        # For player_paddle
        if ball.x_velocity < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                    # Send the ball towards the other paddle
                    ball.x_velocity = -ball.x_velocity
                    # Get the middle coord of the paddle to figure out where ball hit in relation to it
                    # For calculating what the output y angle should be
                    middle_y = left_paddle.y + left_paddle.height / 2
                    y_diff = middle_y - ball.y
                    # How much to reduce angle of bounce by
                    reduction_factor = (
                        left_paddle.height / 2) / ball.MAX_X_VELOCITY
                    y_velocity = y_diff / reduction_factor
                    ball.y_velocity = -y_velocity

        # For bot_paddle
        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                if ball.x + ball.radius >= right_paddle.x:
                    ball.x_velocity = -ball.x_velocity

                    middle_y = right_paddle.y + right_paddle.height / 2
                    y_diff = middle_y - ball.y
                    # How much to reduce angle of bounce by
                    reduction_factor = (right_paddle.height / 2) / \
                        ball.MAX_X_VELOCITY
                    y_velocity = y_diff / reduction_factor
                    ball.y_velocity = -y_velocity
