import pygame

from pong.game_modes import PongGame

# Main access point to game. Run this file to play the game
if __name__ == '__main__':
    fps, width, height = 60, 700, 500
    window = pygame.display.set_mode((width, height))
    game = PongGame(window, fps, width, height)
    game.start_screen()
