import pygame
from pong_objects.menus import Menus


if __name__ == '__main__':
    window = pygame.display.set_mode((700, 500))
    main = Menus(window, 60, 700, 500)
    main.main_menu()
