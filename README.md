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
       trained neural network. The bot was trained over the course of several hours by leaving it to run overnight. 
       It should not be possible to beat this bot as it should have been trained to perfection but I guess it might 
       be possible to beat it. 



Making the pong game: https://www.youtube.com/watch?v=vVGTZlnnX3U&t=2s&ab_channel=TechWithTim

Implementing the AI: https://www.youtube.com/watch?v=2f6TmKm7yx0&ab_channel=TechWithTim

Run "source venv/bin/activate" to enable the virtual environmemt. If nothing seems to work, check that the interpreter is set the venv not base python