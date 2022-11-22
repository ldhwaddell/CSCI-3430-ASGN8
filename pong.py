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
# Set winning score
WIN_SCORE = 5

# Define the size of paddles and board elements
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
SEPARATOR_HEIGHT = HEIGHT // 20
BALL_RADIUS = 9
FONT = pygame.font.SysFont("calibri", 50)


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
        self.x = self.original_x = x
        self.y = self.original_y = y
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

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    # Class attributes
    MAX_X_VELOCITY = 5

    def __init__(self, colour, x, y, radius):
        self.colour = colour
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.MAX_X_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0
        self.x_velocity *= -1


def draw(window, paddles, ball, player_score, bot_score):
    # Make the windows background black
    window.fill(BLACK)

    # Draw the scores
    player_score_text = FONT.render(f"{player_score}", 1, RED)
    bot_score_text = FONT.render(f"{bot_score}", 1, TURQUOISE)
    # blit = "draw"
    WINDOW.blit(player_score_text,
                ((WIDTH//2 - player_score_text.get_width()//2) - 50, 1))
    WINDOW.blit(bot_score_text,
                ((WIDTH//2 - bot_score_text.get_width()//2) + 50, 1))

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


def collision(ball, player_paddle, bot_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_velocity *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_velocity *= -1

    # For player_paddle
    if ball.x_velocity < 0:
        if ball.y >= player_paddle.y and ball.y <= player_paddle.y + player_paddle.height:
            if ball.x - ball.radius <= player_paddle.x + player_paddle.width:
                ball.x_velocity = -ball.x_velocity

                middle_y = player_paddle.y + player_paddle.height / 2
                y_diff = middle_y - ball.y
                # How much to reduce angle of output by
                reduction_factor = (player_paddle.height /
                                    2) / ball.MAX_X_VELOCITY
                y_velocity = y_diff / reduction_factor
                ball.y_velocity = -y_velocity

    # For bot_paddle
    else:
        if ball.y >= bot_paddle.y and ball.y <= bot_paddle.y + bot_paddle.height:
            if ball.x + ball.radius >= bot_paddle.x:
                ball.x_velocity = -ball.x_velocity

                middle_y = bot_paddle.y + bot_paddle.height / 2
                y_diff = middle_y - ball.y
                # How much to reduce angle of output by
                reduction_factor = (bot_paddle.height / 2) / \
                    ball.MAX_X_VELOCITY
                y_velocity = y_diff / reduction_factor
                ball.y_velocity = -y_velocity


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


def score_game(paddle1, paddle2, paddle1_score, paddle2_score, ball):
    if ball.x < 0:
        paddle2_score += 1
        ball.reset()
        paddle1.reset()
        paddle2.reset()
    elif ball.x >= WIDTH:
        paddle1_score += 1
        ball.reset()
        paddle1.reset()
        paddle2.reset()

    return paddle1_score, paddle2_score


def pong_game():
    run = True
    # Create a clock to be able to cap the speed at which screen is refreshed
    clock = pygame.time.Clock()

    player_paddle = Paddle(RED, 10, HEIGHT//2 -
                           PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    bot_paddle = Paddle(TURQUOISE, WIDTH - 10 - PADDLE_WIDTH,
                        HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(GOLD, WIDTH//2, HEIGHT//2, BALL_RADIUS)

    player_score = 0
    bot_score = 0

    while run:
        # Set the tick speed
        clock.tick(FPS)
        draw(WINDOW, [player_paddle, bot_paddle],
             ball, player_score, bot_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print("[+] User has exited game")
                break

        keys = pygame.key.get_pressed()
        paddle_movement(keys, player_paddle, bot_paddle)
        ball.move()
        collision(ball, player_paddle, bot_paddle)

        won = False

        player_score, bot_score = score_game(
            player_paddle, bot_paddle, player_score, bot_score, ball)

        if player_score >= WIN_SCORE:
            won = True
        elif bot_score >= WIN_SCORE:
            won = True

        if won:
            pygame.time.delay(1000)
            ball.reset()
            player_paddle.reset()
            bot_paddle.reset()
            player_score = 0
            bot_score = 0

    pygame.quit()

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText

def main_menu():
    clock = pygame.time.Clock()
    menu = True
    selected = "2_player"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                print("[+] User has exited game")
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.KEYUP:
                    selected = "2_player"
                elif event.key == pygame.KEYDOWN:
                    selected = "quit"
                if event.key==pygame.K_RETURN:
                    if selected=="2_player":
                        print("2_player")
                    if selected=="quit":
                        menu = False
                        print("[+] User has exited game")
                        pygame.quit()
                        break
        # Main menu text
        title = text_format("PONG", "Retro.ttf", 90, WHITE)
        if selected == "2_player":
            text_2_player = text_format("2 Player", "Retro.ttf",75, RED)
        else:
            text_2_player = text_format("2 Player", "Retro.ttf",75, WHITE)
        if selected == "2_player":
            quit = text_format("Quit", "Retro.ttf",75, RED)
        else:
            quit = text_format("Quit", "Retro.ttf",75, WHITE)

        title_rect = title.get_rect()
        text_2_player_rect = text_2_player.get_rect()
        quit_rect = quit.get_rect()

        WINDOW.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        WINDOW.blit(text_2_player, (WIDTH/2 - (text_2_player_rect[2]/2), 300))
        WINDOW.blit(quit, (WIDTH/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()




if __name__ == "__main__":
    #pong_game()
    main_menu()
    
