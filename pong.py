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

# Define the size of paddles
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100


# Define the game colours
RED = (255, 0, 0)
TURQUOISE = (0, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# In pygame, (0, 0) would be the top left corner


class Paddle:
    def __init__(self, colour, x, y, width, height):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.colour,
                         (self.x, self.y, self.width, self.height))


def draw(window, paddles):
    # Make the windows background black
    window.fill(BLACK)

    for paddle in paddles:
        # Call the paddles draw method on each paddle
        paddle.draw(WINDOW)

    # Refresh the display
    pygame.display.update()


def main():
    run = True
    # Create a clock to be able to cap the speed at which screen is refreshed
    clock = pygame.time.Clock()

    player_paddle = Paddle(RED, 10, HEIGHT//2 -
                           PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    bot_paddle = Paddle(TURQUOISE, WIDTH - 10 - PADDLE_WIDTH,
                        HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    while run:
        # Set the tick speed
        clock.tick(FPS)
        draw(WINDOW, [player_paddle, bot_paddle])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print("[+] User has exited game")
                break

    pygame.quit()


if __name__ == "__main__":
    main()
