import pygame

from pong.game_modes import PongGame


if __name__ == '__main__':
    window = pygame.display.set_mode((700, 500))
    game = PongGame(window, 60, 700, 500)
    game.start_screen()
