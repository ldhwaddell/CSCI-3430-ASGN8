import pygame

# Object to hold all colours used in game
colours = {
    "turquoise": (0, 255, 255),
    "gold": (255, 215, 0),
    "red": (255, 0, 0),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
}


def create_font(font_path, text, size, colour):
    """
    Create a font with the given parameters. 

    Parameters: 
        text: The text to be displayed in the font
        size: The size of the font in pixels
        colour: The colour of the font
    """
    font = pygame.font.Font(font_path, size)
    return font.render(text, 1, colour)
