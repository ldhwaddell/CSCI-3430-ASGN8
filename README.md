## Pong With 3 Different Game Modes

- 2 Player
    -  A 2 player pong game where player 1 uses the Q and A keys and player 2 uses the UP and DOWN
        arrow keys. 
- 1 Player against a hardcoded, impossible to beat bot
    -  A 1 player pong game where the human uses the Q and A keys and the bot follows the ball. 
        The bot will always track the ball and make contact with the ball in the exact center of its paddle. 
        it is not possible to beat this bot as it is programmatically "perfect". 
- 1 player against a bot trained with the NEAT algorithm
    -  A 1 player pong game where the human uses the Q and A keys and plays against a bot with a 
       NEAT neural network. The bot was trained over the course of several hours by leaving it to run overnight. 
       It should not be possible to beat this bot as it should have been trained to perfection but I guess it might 
       be possible to beat it. The code for training this bot can be found in train_ai.py. 

Requirements:
- pygame
- neat-python

Both can be found in the requirements.txt file. 

Sources: 

    Some Pong Game Logic: https://www.youtube.com/watch?v=vVGTZlnnX3U&t=2s&ab_channel=TechWithTim

    Implementing the AI: https://www.youtube.com/watch?v=2f6TmKm7yx0&ab_channel=TechWithTim

    NEAT Source Code: https://neat-python.readthedocs.io/en/latest/xor_example.html

    Information on How NEAT Works: https://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf
