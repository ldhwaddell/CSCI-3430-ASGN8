import pygame
import sys
from .utils import colours
from .game import Game

class PongGame():
    win_sound_path = "resources/sounds/smb_stage_clear.wav"
    win_score = 2
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.game = Game(window, width, height)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle

    def two_player(self):
        """
        Start a pong game with two players.
        """
        pygame.display.set_caption("2 Player Pong")
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
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
            #print(repr(game_info))

            won = False

            if game_info.left_score >= self.win_score:
                won = True
            elif game_info.right_score >= self.win_score:
                won = True

            if won:
                # Play Sound
                pygame.mixer.init()
                pygame.mixer.music.load(self.win_sound_path)
                pygame.mixer.music.play(loops=1)
                run = False
            pygame.display.update()
        return run
