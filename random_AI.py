from random import randint
from BaseAI_3 import BaseAI
from Displayer_3 import Displayer
import numpy as np
import time

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

class randomAI(BaseAI):
    # returns a random move from all possible moves from current grid state
    def getMove(self, grid):
        available = grid.getAvailableMoves()
        if len(available) == 0:
            return None
        return available[randint(0,len(available)-1)]