import pygame
pygame.init()

# Set constants for the size of the window
WIDTH = 700
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# Set the windows text to be Pong
pygame.display.set_caption("Pong")
# Set refresh rate
FPS = 60

# Define the size of paddles and board elements
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
SEPARATOR_HEIGHT = HEIGHT // 20
BALL_RADIUS = 7


# Define the game colours
RED = (255, 0, 0)
TURQUOISE = (0, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)

# In pygame, (0, 0) is top left corner


class Paddle:
    # Class attributes
    VELOCITY = 4  # Move 4 units

    def __init__(self, colour, x, y, width, height):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.colour,
                         (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY


class Ball:
    # Class attributes
    MAX_X_VELOCITY = 5

    def __init__(self, colour, x, y, radius):
        self.colour = colour
        self.x = x
        self.y = y
        self.radius = radius
        self.x_velocity = self.MAX_X_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)

    def move(self):
        self.x = self.x_velocity
        self.y = self.y_velocity


def draw(window, paddles, ball):
    # Make the windows background black
    window.fill(BLACK)

    for paddle in paddles:
        # Call the paddles draw method on each paddle
        paddle.draw(WINDOW)

    # Create a checkered line down the middle of the game board
    for i in range(10, HEIGHT, SEPARATOR_HEIGHT):
        # Skip odd numbers so that there are blank spaces
        if i % 2 == 1:
            continue
        else:
            pygame.draw.rect(WINDOW, WHITE, (WIDTH//2 -
                             5, i, 10, SEPARATOR_HEIGHT))

    ball.draw(WINDOW)

    # Refresh the display
    pygame.display.update()


def paddle_movement(keys, player_paddle, bot_paddle):
    # Player movement
    if keys[pygame.K_q] and player_paddle.y - player_paddle.VELOCITY >= 0:
        player_paddle.move()
    if keys[pygame.K_a] and player_paddle.y + player_paddle.VELOCITY + player_paddle.height <= HEIGHT:
        player_paddle.move(up=False)

    # Bot movement
    if keys[pygame.K_UP] and bot_paddle.y - bot_paddle.VELOCITY >= 0:
        bot_paddle.move()
    if keys[pygame.K_DOWN] and bot_paddle.y + bot_paddle.VELOCITY + bot_paddle.height <= HEIGHT:
        bot_paddle.move(up=False)


def main():
    run = True
    # Create a clock to be able to cap the speed at which screen is refreshed
    clock = pygame.time.Clock()

    player_paddle = Paddle(RED, 10, HEIGHT//2 -
                           PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    bot_paddle = Paddle(TURQUOISE, WIDTH - 10 - PADDLE_WIDTH,
                        HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(GOLD, WIDTH//2, HEIGHT//2, BALL_RADIUS)

    while run:
        # Set the tick speed
        clock.tick(FPS)
        draw(WINDOW, [player_paddle, bot_paddle], ball)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print("[+] User has exited game")
                break

        keys = pygame.key.get_pressed()
        paddle_movement(keys, player_paddle, bot_paddle)

    pygame.quit()


if __name__ == "__main__":
    main()
