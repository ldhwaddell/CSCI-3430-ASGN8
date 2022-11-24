import sys

from ball import Ball
from paddle import Paddle

import pygame
pygame.init()

# Set constants for the size of the window
WIDTH = 700
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# Set refresh rate
FPS = 60
# Set winning score
WIN_SCORE = 5

# Define the size of paddles and board elements
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
SEPARATOR_HEIGHT = HEIGHT // 20
BALL_RADIUS = 9
WIN_SOUND = "resources/sounds/smb_stage_clear.wav"
LOSS_SOUND = "resources/sounds/smb_mariodie.wav"





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


def check_collision(ball, paddle1, paddle2):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_velocity *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_velocity *= -1

    # For player_paddle
    if ball.x_velocity < 0:
        if ball.y >= paddle1.y and ball.y <= paddle1.y + paddle1.height:
            if ball.x - ball.radius <= paddle1.x + paddle1.width:
                ball.x_velocity = -ball.x_velocity

                middle_y = paddle1.y + paddle1.height / 2
                y_diff = middle_y - ball.y
                # How much to reduce angle of bounce by
                reduction_factor = (paddle1.height /
                                    2) / ball.MAX_X_VELOCITY
                y_velocity = y_diff / reduction_factor
                ball.y_velocity = -y_velocity

    # For bot_paddle
    else:
        if ball.y >= paddle2.y and ball.y <= paddle2.y + paddle2.height:
            if ball.x + ball.radius >= paddle2.x:
                ball.x_velocity = -ball.x_velocity

                middle_y = paddle2.y + paddle2.height / 2
                y_diff = middle_y - ball.y
                # How much to reduce angle of bounce by
                reduction_factor = (paddle2.height / 2) / \
                    ball.MAX_X_VELOCITY
                y_velocity = y_diff / reduction_factor
                ball.y_velocity = -y_velocity


def two_player_paddle_movement(keys, paddle1, paddle2):
    # Player 1 movement
    if keys[pygame.K_q] and paddle1.y - paddle1.VELOCITY >= 0:
        paddle1.move()
    if keys[pygame.K_a] and paddle1.y + paddle1.VELOCITY + paddle1.height <= HEIGHT:
        paddle1.move(up=False)

    # Player 2 movement
    if keys[pygame.K_UP] and paddle2.y - paddle2.VELOCITY >= 0:
        paddle2.move()
    if keys[pygame.K_DOWN] and paddle2.y + paddle2.VELOCITY + paddle2.height <= HEIGHT:
        paddle2.move(up=False)


def hardcoded_bot_paddle_movement(keys, ball, paddle1, paddle2):
    # Player 1 movement
    if keys[pygame.K_q] and paddle1.y - paddle1.VELOCITY >= 0:
        paddle1.move()
    if keys[pygame.K_a] and paddle1.y + paddle1.VELOCITY + paddle1.height <= HEIGHT:
        paddle1.move(up=False)

    # Bot movememnt for paddle 2

    # If the paddle is already at top of bottom of screen, stay there
    if paddle2.y <= 0:
        paddle2.y = 0
    elif paddle2.y >= 400:
        paddle2.y = 400

    if ball.y <= paddle2.y + (PADDLE_HEIGHT // 2) and ball.y - paddle2.y - (PADDLE_HEIGHT // 2) < -4:
        paddle2.move(up=True)
    elif ball.y <= paddle2.y + (PADDLE_HEIGHT // 2):
        paddle2.y -= 1

    if ball.y >= paddle2.y + (PADDLE_HEIGHT // 2) and ball.y - paddle2.y - (PADDLE_HEIGHT // 2) > 4:
        paddle2.move(up=False)
    elif ball.y >= paddle2.y + (PADDLE_HEIGHT // 2):
        paddle2.y += 1


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

    paddle1 = Paddle(RED, 10, HEIGHT//2 -
                     PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    paddle2 = Paddle(TURQUOISE, WIDTH - 10 - PADDLE_WIDTH,
                     HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

                     
    ball = Ball(GOLD, WIDTH//2, HEIGHT//2, BALL_RADIUS)

    player_score = 0
    bot_score = 0

    while run:
        # Set the tick speed
        clock.tick(FPS)
        draw(WINDOW, [paddle1, paddle2],
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
            two_player_paddle_movement(keys, paddle1, paddle2)
        elif gamemode == "1_player_hardcoded_bot":
            hardcoded_bot_paddle_movement(keys, ball, paddle1, paddle2)

        ball.move()
        check_collision(ball, paddle1, paddle2)

        won = False

        player_score, bot_score = score_game(
            paddle1, paddle2, player_score, bot_score, ball)

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

    

if __name__ == "__main__":
    main_menu()
