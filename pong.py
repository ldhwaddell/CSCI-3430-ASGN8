import sys

import pygame
pygame.init()

# Set constants for the size of the window
WIDTH = 700
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# Set refresh rate
FPS = 60
# Set winning score
WIN_SCORE = 2

# Define the size of paddles and board elements
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
SEPARATOR_HEIGHT = HEIGHT // 20
BALL_RADIUS = 9
FONT = pygame.font.Font("resources/fonts/SuperMario256.ttf", 45)
TITLE_FONT = pygame.font.Font("resources/fonts/SuperMario256.ttf", 65)
WIN_FONT = pygame.font.Font("resources/fonts/SuperMario256.ttf", 60)
WIN_SOUND = "resources/sounds/smb_stage_clear.wav"
LOSS_SOUND = "resources/sounds/smb_mariodie.wav"


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


def check_collision(ball, player_paddle, bot_paddle):
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
                # How much to reduce angle of bounce by
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
                # How much to reduce angle of bounce by
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


def pong_game(gamemode):
    # Set the windows text to be Pong
    pygame.display.set_caption("Pong")
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
                # Empty screen
                WINDOW.fill((0, 0, 0))
                run = False
                print("[+] User has exited game")
                pygame.quit(), sys.exit()

        keys = pygame.key.get_pressed()

        if gamemode == "2_player":
            paddle_movement(keys, player_paddle, bot_paddle)

        ball.move()
        check_collision(ball, player_paddle, bot_paddle)

        won = False

        player_score, bot_score = score_game(
            player_paddle, bot_paddle, player_score, bot_score, ball)

        if player_score >= WIN_SCORE:
            won = True
            winner = "Player 1"
        elif bot_score >= WIN_SCORE:
            won = True
            winner = "Player 2"

        if won:
            # Play Sound
            pygame.mixer.init()
            pygame.mixer.music.load(WIN_SOUND)
            pygame.mixer.music.play(loops=1)
            game_over_menu(winner, gamemode)


def game_over_menu(winner, gamemode):
    WINDOW.fill((0, 0, 0))
    pygame.display.set_caption("Game Over")
    clock = pygame.time.Clock()
    game_over = True
    selected = "play_again"

    while game_over:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                print("[+] User has exited game")
                pygame.quit(), sys.exit()

            if event.type == pygame.KEYDOWN:
                # Logic for user pressing up arrow key
                if event.key == pygame.K_UP and selected == "play_again":
                    selected = "play_again"
                elif event.key == pygame.K_UP and selected == "diff_game_mode":
                    selected = "play_again"
                elif event.key == pygame.K_UP and selected == "quit":
                    selected = "diff_game_mode"

                # Logic for user pressing down arrow key
                if event.key == pygame.K_DOWN and selected == "play_again":
                    selected = "diff_game_mode"
                elif event.key == pygame.K_DOWN and selected == "diff_game_mode":
                    selected = "quit"
                elif event.key == pygame.K_DOWN and selected == "quit":
                    selected = "quit"

                # Logic for user pressing enter on selection
                if event.key == pygame.K_RETURN:
                    if selected == "play_again":
                        pong_game(gamemode)
                    elif selected == "diff_game_mode":
                        main_menu()
                    elif selected == "quit":
                        game_over = False
                        print("[+] User has exited the game")
                        pygame.quit(), sys.exit()

        # Main menu text
        title = WIN_FONT.render(f"{winner} has Won!", 1, WHITE)

        # Options text
        if selected == "play_again":
            text_play_again = FONT.render("Play Again", 1, RED)
        else:
            text_play_again = FONT.render("Play Again", 1, WHITE)

        if selected == "diff_game_mode":
            text_diff_game_mode = FONT.render(
                "Different Game Mode", 1, RED)
        else:
            text_diff_game_mode = FONT.render(
                "Different Game Mode", 1, WHITE)

        if selected == "quit":
            quit = FONT.render("Quit", 1, RED)
        else:
            quit = FONT.render("Quit", 1, WHITE)

        # The space between each game option (with 10 px buffer)
        vertical_offset = text_play_again.get_height() + 10

        # Draw the title and text options. The center of screen is found and then text is moved 40 pixels up to ensure spacing fits correctly
        WINDOW.blit(title, (WIDTH // 2 - title.get_width()//2, 30))
        WINDOW.blit(text_play_again, (WIDTH // 2 - text_play_again.get_width() //
                    2, HEIGHT//2 - text_play_again.get_height()//2))
        WINDOW.blit(text_diff_game_mode, (WIDTH // 2 - text_diff_game_mode.get_width() //
                    2, (HEIGHT//2 - text_diff_game_mode.get_height()//2) + vertical_offset))
        WINDOW.blit(quit, (WIDTH // 2 - quit.get_width()//2,
                    (HEIGHT//2 - quit.get_height()//2) + 2 * (vertical_offset)))

        # Refresh display to show selection
        pygame.display.update()


def main_menu():
    WINDOW.fill((0, 0, 0))
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()
    menu = True
    selected = "2_player"

    while menu:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                print("[+] User has exited game")
                pygame.quit(), sys.exit()
            if event.type == pygame.KEYDOWN:
                # Logic for user pressing up arrow key
                if event.key == pygame.K_UP and selected == "2_player":
                    selected = "2_player"
                elif event.key == pygame.K_UP and selected == "1_player_hardcoded_bot":
                    selected = "2_player"
                elif event.key == pygame.K_UP and selected == "1_player_trained_bot":
                    selected = "1_player_hardcoded_bot"
                elif event.key == pygame.K_UP and selected == "quit":
                    selected = "1_player_trained_bot"

                # Logic for user pressing down arrow key
                if event.key == pygame.K_DOWN and selected == "2_player":
                    selected = "1_player_hardcoded_bot"
                elif event.key == pygame.K_DOWN and selected == "1_player_hardcoded_bot":
                    selected = "1_player_trained_bot"
                elif event.key == pygame.K_DOWN and selected == "1_player_trained_bot":
                    selected = "quit"

                # Logic for user pressing enter on selection
                if event.key == pygame.K_RETURN:
                    if selected == "2_player":
                        pong_game("2_player")
                    elif selected == "1_player_hardcoded_bot":
                        print("1_player_hardcoded_bot")
                    elif selected == "1_player_trained_bot":
                        print("1_player_trained_bot")
                    elif selected == "quit":
                        menu = False
                        print("[+] User has exited game")
                        pygame.quit(), sys.exit()

        # Main menu text
        title = TITLE_FONT.render("PONG", 1, WHITE)

        # Options text
        if selected == "2_player":
            text_2_player = FONT.render("2 Player", 1, RED)
        else:
            text_2_player = FONT.render("2 Player", 1, WHITE)

        if selected == "1_player_hardcoded_bot":
            text_1_player_hardcoded_bot = FONT.render(
                "1 Player Hardcoded Bot", 1, RED)
        else:
            text_1_player_hardcoded_bot = FONT.render(
                "1 Player Hardcoded Bot", 1, WHITE)

        if selected == "1_player_trained_bot":
            text_1_player_trained_bot = FONT.render(
                "1 Player trained Bot", 1, RED)
        else:
            text_1_player_trained_bot = FONT.render(
                "1 Player trained Bot", 1, WHITE)

        if selected == "quit":
            quit = FONT.render("Quit", 1, RED)
        else:
            quit = FONT.render("Quit", 1, WHITE)

        # The space between each game option (with 10 px buffer)
        vertical_offset = text_2_player.get_height() + 10

        # Draw the title and text options. The center of screen is found and then text is moved 40 pixels up to ensure spacing fits correctly
        WINDOW.blit(title, (WIDTH // 2 - title.get_width()//2, 30))
        WINDOW.blit(text_2_player, (WIDTH // 2 - text_2_player.get_width() //
                    2, HEIGHT//2-text_2_player.get_height()//2 - 40))
        WINDOW.blit(text_1_player_hardcoded_bot, (WIDTH // 2 - text_1_player_hardcoded_bot.get_width() //
                    2, (HEIGHT//2-text_1_player_hardcoded_bot.get_height()//2 - 40) + vertical_offset))
        WINDOW.blit(text_1_player_trained_bot, (WIDTH // 2 - text_1_player_trained_bot.get_width() //
                    2, (HEIGHT//2-text_1_player_trained_bot.get_height()//2 - 40) + 2*(vertical_offset)))
        WINDOW.blit(quit, (WIDTH // 2 - quit.get_width()//2,
                    (HEIGHT//2-quit.get_height()//2 - 40) + 3*(vertical_offset)))

        # Refresh display to show selection
        pygame.display.update()


if __name__ == "__main__":
    main_menu()
