import pygame

from pong.game_modes import PongGame

# Main access point to game. Run this file to play the game
if __name__ == '__main__':
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))
    game = PongGame(window, 60, 700, 500)
    game.start_screen()
