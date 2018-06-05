import random
import numpy as np

class RandomMove:
    def __init__(self):
        self.name = 'Random Move'

    def move(self, game):
        return random.choice(game.legal_moves())


class AllLeft:
    def __init__(self):
        self.name = 'All to the Left'

    def move(self, game):
        arr = np.array(game.legal_moves())
        return arr.min()