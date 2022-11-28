import pygame

from .paddle import Paddle
from .ball import Ball
from .utils import colours, create_font

pygame.init()


class GameInfo:

    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score

    def __repr__(self):
        return f"GameInfo(left_hits={self.left_hits}, right_hits={self.right_hits}, left_score={self.left_score}, right_score={self.right_score})"


class Game:
    # Class Attributes
    font_path = "resources/fonts/ARCADECLASSIC.ttf"
    win_score = 2

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

    def draw_divider(self):
        separator = self.height // 20
        for i in range(10, self.height, separator):
            if i % 2 == 1:
                continue
            else:
                pygame.draw.rect(
                    self.window, colours["white"], (self.width // 2 - 5, i, 10, separator))

    def draw_score(self):
        left_score_text = create_font(
            self.font_path, f"{self.left_score}", 60, colours["red"])
        right_score_text = create_font(
            self.font_path, f"{self.right_score}", 60, colours["turquoise"])

        self.window.blit(left_score_text, ((self.width // 2 -
                         left_score_text.get_width() // 2) - 50, 1))
        self.window.blit(right_score_text, ((self.width // 2 -
                         right_score_text.get_width() // 2) + 50, 1))

    def draw_hits(self):
        hits_text = create_font(
            self.font_path, f"{self.left_hits + self.right_hits}", 60, colours["red"])

        self.window.blit(hits_text, ((self.width // 2 -
                         hits_text.get_width() // 2), 1))

    def draw(self, draw_score=True, draw_hits=False):
        self.window.fill(colours["black"])

        self.draw_divider()

        if draw_score:
            self.draw_score()

        if draw_hits:
            self.draw_hits()

        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(self.window)

        self.ball.draw(self.window)

    def check_collision(self):
        # Pull in the ball and paddle objects for current game
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        # If the ball hits the bottom or top of the window, reverse its y direction
        if ball.y + ball.RADIUS >= self.height:
            ball.y_velocity *= -1
        elif ball.y - ball.RADIUS <= 0:
            ball.y_velocity *= -1

        # For player_paddle
        if ball.x_velocity < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.HEIGHT:
                if ball.x - ball.RADIUS <= left_paddle.x + left_paddle.WIDTH:
                    # Send the ball towards the other paddle
                    ball.x_velocity = -ball.x_velocity
                    # Get the middle coord of the paddle to figure out where ball hit in relation to it
                    # For calculating what the output y angle should be
                    middle_y = left_paddle.y + left_paddle.HEIGHT / 2
                    y_diff = middle_y - ball.y
                    # How much to reduce angle of bounce by
                    reduction_factor = (
                        left_paddle.HEIGHT / 2) / ball.MAX_X_VELOCITY
                    y_velocity = y_diff / reduction_factor
                    ball.y_velocity = -y_velocity
                    self.left_hits += 1

        # For bot_paddle
        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_velocity = -ball.x_velocity

                    middle_y = right_paddle.y + right_paddle.HEIGHT / 2
                    y_diff = middle_y - ball.y
                    # How much to reduce angle of bounce by
                    reduction_factor = (right_paddle.HEIGHT / 2) / \
                        ball.MAX_X_VELOCITY
                    y_velocity = y_diff / reduction_factor
                    ball.y_velocity = -y_velocity
                    self.right_hits += 1

    def move_paddles(self, left=True, up=True):
        if left:
            if up and self.left_paddle.y - Paddle.VELOCITY < 0:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > self.height:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VELOCITY < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > self.height:
                return False
            self.right_paddle.move(up)

        return True

    def reset(self):
        """Reset game."""
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0

    def loop(self):
        """
        Executes a single game loop.
        :returns: GameInformation instance stating score 
                  and hits of each paddle.
        """
        self.ball.move()
        self.check_collision()

        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.width:
            self.ball.reset()
            self.left_score += 1

        game_info = GameInfo(
            self.left_hits, self.right_hits, self.left_score, self.right_score)

        return game_info
