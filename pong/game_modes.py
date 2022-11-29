import os
import pickle
import sys

import neat
import pygame

from .utils import colours
from .game import Game
from .menus import Menus


class PongGame():
    """
    Class to create instances of a game of pong with the users deried gamemode. 
    Instantiateing the pong game and calling the startscreen function presents the main menu and 
    gives the user a choice of three different game modes to play from. 

    2 Player:
        A 2 player pong game where player 1 uses the Q and A keys and player 2 uses the UP and DOWN
        arrow keys. 

    1 Player Hardcoded Bot:
        A 1 player pong game where the human uses the Q and A keys and the bot follows the ball. 
        The bot will always track the ball and make contact with the ball in the exact center of its paddle. 
        it is not possible to beat this bot as it is programmatically "perfect". 

    1 Player Trained Bot: 
       A 1 player pong game where the human uses the Q and A keys and plays against a bot with a 
       trained neural network. The bot was trained over the course of several hours by leaving it to run overnight. 
       It should not be possible to beat this bot as it "should" have been trained to perfection. It's movement is extremely jittery.
       This is likely causes by the fact this it can only move +/- 4 pixels at a time, as a result, when it is moving up and down 
       extremely fast, it appears to be glitching or jittering


    :param window: The pygame window to draw the game in to
    :param fps: The rate at which pygame should refresh the game screens
    :param width: The width of the window in pixels
    :param height: The height of the window in pixels
    """
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
        """Checks if music is currently being played and stops it if it is"""
        if self.sound.music.get_busy():
            self.sound.music.stop()

    def start_screen(self, game_mode=None):
        """
        Starts the main menu and starts the gamemode
        the user selects.  

        :param game_mode: The game mode to start the game with
        """

        self._stop_music()
        # If there is no selected game mode, display the main menu
        if game_mode is None:
            game_mode = self.menu.draw_main()

        # Otherwise if there is a selected game mode, start that type of game
        if game_mode == "2_player":
            self._two_player()
        elif game_mode == "1_player_hardcoded_bot":
            self._one_player_hardcoded_bot()
        elif game_mode == "1_player_trained_bot":
            self._one_player_trained_bot()

    def _game_over_screen(self, game_mode, winner):
        """
        Draws the game over screen

        :param game_mode: The game mode to start the game with
        :param winner: The winner of the game
        """
        # Draw the game mover screen displaying whoever won
        status = self.menu.draw_game_over(winner)
        # If the user wants to play a new game mode, display main menu again
        if status == "diff_game_mode":
            self.start_screen(game_mode=None)

        # Otherwise, play the users selected game mode
        else:
            self.start_screen(game_mode=game_mode)

    def _game_over(self, game_mode, winner):
        """
        Called when the game finishes. Plays the game over sound, 
        resets the game score and object positions, and displays the game over screen
        """
        self.sound.music.load(self.win_sound_path)
        self.sound.music.play(loops=1)
        self.game.reset()
        self._game_over_screen(game_mode=game_mode, winner=winner)
        return False

    def _two_player(self):
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

            # Move the left paddle
            if keys[pygame.K_q]:
                self.game.move_paddles(left=True, up=True)
            elif keys[pygame.K_a]:
                self.game.move_paddles(left=True, up=False)

            # Move the right paddle
            if keys[pygame.K_UP]:
                self.game.move_paddles(left=False, up=True)
            elif keys[pygame.K_DOWN]:
                self.game.move_paddles(left=False, up=False)

            # Draw objects on screen
            self.game.draw(draw_score=True)

            won = False
            # Check for game finishing
            if game_info.left_score >= self.win_score:
                won = True
                winner = "Player 1"
            elif game_info.right_score >= self.win_score:
                won = True
                winner = "Player 2"

            if won:
                run = self._game_over(game_mode="2_player", winner=winner)

            pygame.display.update()

    def _one_player_hardcoded_bot(self):
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

            # Allow player to move paddle
            if keys[pygame.K_q]:
                self.game.move_paddles(left=True, up=True)
            elif keys[pygame.K_a]:
                self.game.move_paddles(left=True, up=False)

            # Move bot paddle
            self._hardcoded_bot_movement()

            # Draw objects on screen
            self.game.draw(draw_score=True)

            won = False

            # Check for game finishing
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
        """
        Controls the hardcoded bot movement. 

        If the bot paddle is at the top or bottom of the screen, make it stay there so it does not move
        off screen. Other, if the difference in y values between the ball and the paddle is greater than the 
        4 pixels that the paddle moves at a time, allow it to move 4 pixels towards the ball. If the space is 
        less than 4 pixels, make it move 1 pixel per clock cycle to ensure that the paddle does not flicker on screen.
        """
        # Create variable to minimize typing
        paddle = self.right_paddle
        ball = self.ball

        # If the ball is at the top or bottom of the screen, leave it
        if paddle.y <= 0:
            paddle.y = 0
        elif paddle.y >= 400:
            paddle.y = 400

        # Check space between ball and paddle and move as defined above
        if ball.y <= paddle.y + (paddle.HEIGHT // 2) and ball.y - paddle.y - (paddle.HEIGHT // 2) < -4:
            paddle.move(up=True)
        elif ball.y <= paddle.y + (paddle.HEIGHT // 2):
            paddle.y -= 1

        if ball.y >= paddle.y + (paddle.HEIGHT // 2) and ball.y - paddle.y - (paddle.HEIGHT // 2) > 4:
            paddle.move(up=False)
        elif ball.y >= paddle.y + (paddle.HEIGHT // 2):
            paddle.y += 1

    def _get_net(self):
        """
        Gets the best neural network for the player to play against

        returns: 
            net: The best net to play against
        """
        with open("net.pickle", "rb") as f:
            net = pickle.load(f)
        return net

    def _get_config(self):
        """
        Gets the configuration for the neural network

        returns: 
            config: The neural network configuration
        """
        # Get root directory
        dir = os.path.dirname(os.path.dirname(__file__))
        # Find config file
        config_path = os.path.join(dir, "config.txt")
        # Create config object
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)
        return config

    def _one_player_trained_bot(self):
        """
        Start a pong game with one player against a NEAT neural network
        """
        # Get config file
        config = self._get_config()
        # Get the best neural network configuration
        net_obj = self._get_net()
        net = neat.nn.FeedForwardNetwork.create(net_obj, config)
        self._stop_music()
        self.window.fill(colours["black"])
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

            # Activate the neural network to get decisions from it
            output = net.activate((self.right_paddle.y, abs(
                self.right_paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            # Allow th eplayer to move
            if keys[pygame.K_q]:
                self.game.move_paddles(left=True, up=True)
            elif keys[pygame.K_a]:
                self.game.move_paddles(left=True, up=False)

            # Control the paddle based on the neural networks decision
            if decision == 0:
                pass
            if decision == 1:
                self.game.move_paddles(left=False, up=True)
            elif decision == 2:
                self.game.move_paddles(left=False, up=False)

            self.game.draw(draw_score=True)

            won = False
            # Check for game finishing
            if game_info.left_score >= self.win_score:
                won = True
                winner = "Player"
            elif game_info.right_score >= self.win_score:
                won = True
                winner = "Bot"

            if won:
                run = self._game_over(
                    game_mode="1_player_trained_bot", winner=winner)
            pygame.display.update()
