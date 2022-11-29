import os
import pickle
import sys
import time

import neat
import pygame

from pong.game import Game


class PongGame():

    def __init__(self, window, fps, width, height):
        self.game = Game(window, width, height)
        self.fps = fps
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle

    def test_ai(self, net):
        # self._stop_music()
        # self.window.fill(colours["black"])
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.fps)
            game_info = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Empty screen
                    # self.game.window.fill(colours["black"])
                    run = False
                    print("[+] User has exited game")
                    pygame.quit(), sys.exit()

            keys = pygame.key.get_pressed()

            output = net.activate((self.right_paddle.y, abs(
                self.right_paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            if keys[pygame.K_q]:
                self.game.move_paddles(left=True, up=True)
            elif keys[pygame.K_a]:
                self.game.move_paddles(left=True, up=False)

            if decision == 0:
                pass
            if decision == 1:
                self.game.move_paddles(left=False, up=True)
            elif decision == 2:
                self.game.move_paddles(left=False, up=False)

            self.game.draw(draw_score=True)
            pygame.display.update()

    def train_ai(self, genome1, genome2, config, draw=False):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
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

            game_info = self.game.loop()

            self.move_ai_paddles(net1, net2)

            if draw:
                self.game.draw(draw_score=False, draw_hits=True)

            pygame.display.update()

            duration = time.time() - start_time

            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits > max_hits:
                self.calculate_fitness(game_info, duration)
                break

        return False

    def move_ai_paddles(self, net1, net2):
        """
        Determine where to move the left and the right paddle based on the two 
        neural networks that control them. 
        """
        players = [(self.genome1, net1, self.left_paddle, True),
                   (self.genome2, net2, self.right_paddle, False)]
        for (genome, net, paddle, left) in players:
            output = net.activate(
                (paddle.y, abs(paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            valid = True
            if decision == 0:  # Don't move
                genome.fitness -= 0.01  # we want to discourage this
            elif decision == 1:  # Move up
                valid = self.game.move_paddles(left=left, up=True)
            else:  # Move down
                valid = self.game.move_paddles(left=left, up=False)

            if not valid:  # If the movement makes the paddle go off the screen punish the AI
                genome.fitness -= 1

    def calculate_fitness(self, game_info, duration):
        self.genome1.fitness += game_info.left_hits + duration
        self.genome2.fitness += game_info.right_hits + duration


def get_config():
    dir = os.path.dirname(__file__)
    config_path = os.path.join(dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    return config


def eval_genomes(genomes, config):
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Training NEAT")

    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i/len(genomes) * 100), end=" ")
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGame(win, 60, width, height)

            force_quit = game.train_ai(genome1, genome2, config, draw=True)
            if force_quit:
                quit()


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("net.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best(config):
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    with open("net.pickle", "rb") as f:
        winner = pickle.load(f)

    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    game = PongGame(win, 60, width, height)
    game.test_ai(winner_net)


if __name__ == '__main__':
    config = get_config()
    #run_neat(config)
    test_best(config)
