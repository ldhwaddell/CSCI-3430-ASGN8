import pygame
import sys
from .utils import colours
from .game import Game
from .menus import Menus


class PongGame():
    win_sound_path = "resources/sounds/smb_stage_clear.wav"
    win_score = 2

    def __init__(self, window, fps, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.game = Game(window, width, height)
        self.fps = fps
        self.menu = Menus(window, fps, width, height)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        # Create sound object and initialize it
        self.sound = pygame.mixer
        self.sound.init()

    def _stop_music(self):
        # Check if game over sound is playing and stop if it is
        if self.sound.music.get_busy():
            self.sound.music.stop()

    def start_screen(self, game_mode=None):
        self._stop_music()
        if game_mode is None:
            game_mode = self.menu.draw_main()
        if game_mode == "2_player":
            self.two_player()
        elif game_mode == "1_player_hardcoded_bot":
            self.one_player_hardcoded_bot()
        elif game_mode == "1_player_trained_bot":
            self.test_ai()

    def _game_over_screen(self, game_mode, winner):
        status = self.menu.draw_game_over(game_mode, winner)
        if status == "diff_game_mode":
            self.start_screen(game_mode=None)
        else:
            self.start_screen(game_mode=game_mode)

    def _game_over(self, game_mode, winner):
        self.sound.music.load(self.win_sound_path)
        self.sound.music.play(loops=1)
        self.game.reset()
        self._game_over_screen(game_mode=game_mode, winner=winner)
        return False

    def two_player(self):
        """
        Start a pong game with two players.
        """
        self._stop_music()
        self.window.fill(colours["black"])
        pygame.display.set_caption("2 Player Pong")
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.fps)
            game_info = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Empty screen
                    self.game.window.fill(colours["black"])
                    run = False
                    print("[+] User has exited game")
                    pygame.quit(), sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_q]:
                self.game.move_paddles(left=True, up=True)
            elif keys[pygame.K_a]:
                self.game.move_paddles(left=True, up=False)

            if keys[pygame.K_UP]:
                self.game.move_paddles(left=False, up=True)
            elif keys[pygame.K_DOWN]:
                self.game.move_paddles(left=False, up=False)

            self.game.draw(draw_score=True)
            # print(repr(game_info))

            won = False

            if game_info.left_score >= self.win_score:
                won = True
                winner = "Player 1"
            elif game_info.right_score >= self.win_score:
                won = True
                winner = "Player 2"

            if won:
                run = self._game_over(game_mode="2_player", winner=winner)

            pygame.display.update()

    def one_player_hardcoded_bot(self):
        """
        Start a pong game with one player against an impossible to beat
        hardcoded bot.
        """
        self._stop_music()
        self.window.fill(colours["black"])
        pygame.display.set_caption("1 Player Pong")
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.fps)
            game_info = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Empty screen
                    self.game.window.fill(colours["black"])
                    run = False
                    print("[+] User has exited game")
                    pygame.quit(), sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_q]:
                self.game.move_paddles(left=True, up=True)
            elif keys[pygame.K_a]:
                self.game.move_paddles(left=True, up=False)

            self._hardcoded_bot_movement()

            self.game.draw(draw_score=True)

            won = False

            if game_info.left_score >= self.win_score:
                won = True
                winner = "Player"
            elif game_info.right_score >= self.win_score:
                won = True
                winner = "Bot"

            if won:
                run = self._game_over(
                    game_mode="1_player_hardcoded_bot", winner=winner)

            pygame.display.update()

    def _hardcoded_bot_movement(self):
        paddle = self.right_paddle
        ball = self.ball
        if paddle.y <= 0:
            paddle.y = 0
        elif paddle.y >= 400:
            paddle.y = 400

        if ball.y <= paddle.y + (paddle.HEIGHT // 2) and ball.y - paddle.y - (paddle.HEIGHT // 2) < -4:
            paddle.move(up=True)
        elif ball.y <= paddle.y + (paddle.HEIGHT // 2):
            paddle.y -= 1

        if ball.y >= paddle.y + (paddle.HEIGHT // 2) and ball.y - paddle.y - (paddle.HEIGHT // 2) > 4:
            paddle.move(up=False)
        elif ball.y >= paddle.y + (paddle.HEIGHT // 2):
            paddle.y += 1

    def test_ai(self):
        ...
