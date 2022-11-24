import pygame
from pong_objects.menus import Menus
pygame.init()

win = pygame.display.set_mode((700, 500))
test = Menus(win, 60, 700, 600)

test.main_menu()