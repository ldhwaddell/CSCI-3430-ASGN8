import sys

import pygame


class Menus:
    """
    A class to contain the two different menu options, the main menu
    and the game over menu. When the user runs the game, they will be 
    presented with the main menu. When the user wins a game, or loses to either type of bot, 
    they will be presented with the game over menu. 

    Parameters:
        window: The pygame window to draw the menu in to
        fps: The rate at which pygame should refresh the menu screens
        width: The width of the window in pixels
        height: The height of the window in pixels
    """
    # Class attributes
    font_path = "resources/fonts/ARCADECLASSIC.ttf"
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, window, fps, width, height):
        self.window = window
        self.fps = fps
        self.width = width
        self.height = height

    def create_font(self, text, size, colour):
        """
        Create a font with the given parameters. 

        Parameters: 
            text: The text to be displayed in the font
            size: The size of the font in pixels
            colour: The colour of the font
        """
        font = pygame.font.Font(self.font_path, size)
        return font.render(text, 1, colour)

    def main_menu(self):
        """
        Present the main menu to the user.
        """
        # Remove all existing objects from the window by filling it with black
        self.window.fill(self.BLACK)
        pygame.display.set_caption("Main Menu")
        clock = pygame.time.Clock()
        menu = True
        selected = "2_player"

        # Run while the user has not clicked out of the menu
        while menu:
            clock.tick(self.fps)

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
                            # pong_game("2_player")
                            print("2 play")
                        elif selected == "1_player_hardcoded_bot":
                            # pong_game("1_player_hardcoded_bot")
                            print("1 play bot ")
                        elif selected == "1_player_trained_bot":
                            print("1_player_trained_bot")
                        elif selected == "quit":
                            menu = False
                            print("[+] User has exited game")
                            pygame.quit(), sys.exit()

            # Main menu text
            title = self.create_font("PONG", 85, self.WHITE)

            # Options text
            if selected == "2_player":
                text_2_player = self.create_font("2 Player", 60, self.RED)
            else:
                text_2_player = self.create_font("2 Player", 60, self.WHITE)

            if selected == "1_player_hardcoded_bot":
                text_1_player_hardcoded_bot = self.create_font(
                    "1 Player Hardcoded Bot", 60, self.RED)
            else:
                text_1_player_hardcoded_bot = self.create_font(
                    "1 Player Hardcoded Bot", 60, self.WHITE)

            if selected == "1_player_trained_bot":
                text_1_player_trained_bot = self.create_font(
                    "1 Player trained Bot", 60, self.RED)
            else:
                text_1_player_trained_bot = self.create_font(
                    "1 Player trained Bot", 60, self.WHITE)

            if selected == "quit":
                quit = self.create_font("Quit", 60, self.RED)
            else:
                quit = self.create_font("Quit", 60, self.WHITE)

            # The space between each game option (with 10 px buffer)
            vertical_offset = text_2_player.get_height() + 10

            # Draw the title and text options. The center of screen is found and then
            # text is moved 40 pixels up to ensure spacing fits correctly
            self.window.blit(
                title, (self.width // 2 - title.get_width()//2, 30))
            self.window.blit(text_2_player, (self.width // 2 - text_2_player.get_width() //
                                             2, self.height//2-text_2_player.get_height()//2 - 40))
            self.window.blit(text_1_player_hardcoded_bot, (self.width // 2 - text_1_player_hardcoded_bot.get_width() //
                                                           2, (self.height//2-text_1_player_hardcoded_bot.get_height()//2 - 40) + vertical_offset))
            self.window.blit(text_1_player_trained_bot, (self.width // 2 - text_1_player_trained_bot.get_width() //
                                                         2, (self.height//2-text_1_player_trained_bot.get_height()//2 - 40) + 2*(vertical_offset)))
            self.window.blit(quit, (self.width // 2 - quit.get_width()//2,
                                    (self.height//2-quit.get_height()//2 - 40) + 3*(vertical_offset)))

            # Refresh display to show selection
            pygame.display.update()

    def game_over_menu(self, gamemode, winner):
        """
        Draws the game over menu

        Params: 
            gamemode: Game mode
            winner: Winner of the game
        """
        # Remove all existing objects from the window by filling it with black
        self.window.fill(self.BLACK)
        pygame.display.set_caption("Game Over")
        clock = pygame.time.Clock()
        game_over = True
        selected = "play_again"

        while game_over:
            clock.tick(self.fps)

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
                            # pong_game(gamemode)
                            print("here")
                        elif selected == "diff_game_mode":
                            self.main_menu()
                        elif selected == "quit":
                            game_over = False
                            print("[+] User has exited the game")
                            pygame.quit(), sys.exit()

            # Main menu text
            title = self.create_font(f"{winner} has Won!", 60, self.WHITE)

            # Options text
            if selected == "play_again":
                text_play_again = self.create_font("Play Again", 60, self.RED)
            else:
                text_play_again = self.create_font(
                    "Play Again", 60, self.WHITE)

            if selected == "diff_game_mode":
                text_diff_game_mode = self.create_font(
                    "Different Game Mode", 60, self.RED)
            else:
                text_diff_game_mode = self.create_font(
                    "Different Game Mode", 60, self.WHITE)

            if selected == "quit":
                quit = self.create_font("Quit", 60, self.RED)
            else:
                quit = self.create_font("Quit", 60, self.WHITE)

            # The space between each game option (with 10 px buffer)
            vertical_offset = text_play_again.get_height() + 10

            # Draw the title and text options. The center of screen is found and then text is moved 40 pixels up to ensure spacing fits correctly
            self.window.blit(
                title, (self.width // 2 - title.get_width()//2, 30))
            self.window.blit(text_play_again, (self.width // 2 - text_play_again.get_width() //
                                               2, self.height // 2 - text_play_again.get_height() // 2))
            self.window.blit(text_diff_game_mode, (self.width // 2 - text_diff_game_mode.get_width() //
                                                   2, (self.height//2 - text_diff_game_mode.get_height() // 2) + vertical_offset))
            self.window.blit(quit, (self.width // 2 - quit.get_width() // 2,
                                    (self.height // 2 - quit.get_height() // 2) + 2 * (vertical_offset)))

            # Refresh display to show selection
            pygame.display.update()
