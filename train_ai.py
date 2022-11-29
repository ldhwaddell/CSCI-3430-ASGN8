import os
import pickle
import sys
import time

import neat
import pygame

from pong.game import Game


class PongGame():
    """
    Class to create an instance of a Pong Game for training the NEAT neural network. This
    clas is very similar to that in "game_modes.py", but it contains methods simply focused 
    on the training of the network. 

    :param window: The pygame window to draw the game in to
    :param fps: The rate at which pygame should refresh the game screens
    :param width: The width of the window in pixels
    :param height: The height of the window in pixels

    """

    def __init__(self, window, fps, width, height):
        self.game = Game(window, width, height)
        self.fps = fps
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle

    def train_ai(self, genome1, genome2, config, draw=False):
        """
        Train the neural network using the provided genomes. There is not cap on 
        the clock speed here as it was taking way too long to train if I set the 
        clock speed to 60 like the regular game. 

        :param genome1: The genome to use for the first neural network
        :param genome2: The genome to use for the second neural network
        :param config: The configuration of the neural network
        :param draw: Whether to draw the game total hits or not
        """
        # Create the networks
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        # Define the genomes for use in other methods
        self.genome1 = genome1
        self.genome2 = genome2

        max_hits = 50
        clock = pygame.time.Clock()
        run = True
        start_time = time.time()
        while run:
            clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            # Call the single loop of base game
            game_info = self.game.loop()

            self.move_ai_paddles(net1, net2)

            if draw:
                self.game.draw(draw_score=False, draw_hits=True)

            pygame.display.update()

            duration = time.time() - start_time

            # If either net gets a point or they reach a stalemate and the total hits reaches 100, quit current game
            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits > max_hits:
                self.calculate_fitness(game_info, duration)
                break

        # Return false while game loop running
        return False

    def move_ai_paddles(self, net1, net2):
        """
        Method to move the left and right paddles based o nthe output of their respective nets. 
        This function creates a list of tuples with the relevant information for the left and 
        right paddles. It then activates the respective net for each paddle and calls the games "move_paddles"
        function with whatever arguments necessary to meet the decision of the network. 

        :param net1: The first neural network
        :param net2: The second neural network
        """

        players = [(self.genome1, net1, self.left_paddle, True),
                   (self.genome2, net2, self.right_paddle, False)]
        # Iterate over each tuple
        for (genome, net, paddle, left) in players:
            output = net.activate(
                (paddle.y, abs(paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            valid = True
            if decision == 0:
                # Lower fitness to discourage doing nothing
                genome.fitness -= 0.01
            elif decision == 1:
                valid = self.game.move_paddles(left=left, up=True)
            else:
                valid = self.game.move_paddles(left=left, up=False)

            # If the AI wants to make an invalid move, massively discourage it
            # Invalid can be defined as moving off the screen
            if not valid:
                genome.fitness -= 1

    def calculate_fitness(self, game_info, duration):
        """
        Method to calculate the fitness of the neural network based on the game_info object. 

        :param game_info: The game_info object that contains information about the game
        :param duration: The duration of the game
        """
        self.genome1.fitness += game_info.left_hits + duration
        self.genome2.fitness += game_info.right_hits + duration


def get_config():
    """
    Gets the configuration for the neural network

    returns: 
        config: The neural network configuration
    """
    # Getting file
    dir = os.path.dirname(__file__)
    config_path = os.path.join(dir, "config.txt")

    # Creating config object
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    return config


def eval_genomes(genomes, config):
    """
    Evaluates the neural network for the given genomes. Pits each genome against
    each other genome to ensure the absolute best is found. This rapidly creates and stops
    unique pong games once one genome scores against the other. 

    genomes: The genomes to evaluate
    config: The neural network configuration
    """

    fps, width, height = 60, 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Training NEAT")

    for i, (genome_id1, genome1) in enumerate(genomes):
        # Print progress for each training round
        print(round(i/len(genomes) * 100), end=" ")
        # Stop loop if we reach end of genomes
        if i == len(genomes) - 1:
            break
        # Reset the genome fitness
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            # Create the game and exit once the train_ai method returns true
            game = PongGame(win, fps, width, height)
            force_quit = game.train_ai(genome1, genome2, config, draw=True)
            if force_quit:
                quit()


def run_neat(config):
    """
    Function to start the NEAT training and output the progress to 
    console. The neat algo is ran 50 times or until a fitness threshold of 400
    is met as defined in the config file. Once this is met, the file "net.pickle" 
    is created with the pickled object that is the "best" neural network for use 
    in the game

    :param config: the config file    
    """
    # Defining population and what/where to output
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    # Training network
    best_net = p.run(eval_genomes, 50)
    # Saving best neural network
    with open("net.pickle", "wb") as f:
        pickle.dump(best_net, f)


if __name__ == '__main__':
    config = get_config()
    run_neat(config)
