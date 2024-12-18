from random import randint
from BaseAI_3 import BaseAI
from Displayer_3 import Displayer
import numpy as np
import time
import math

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

# class for the nodes of the game tree
class Node():
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.total_wins = 0
        self.total_playouts = 0
        self.possible_moves = self.state.getAvailableMoves() 
    

class montecarloAI(BaseAI):
    time_limit = 0 
    def getMove(self, grid):
        # based off implementation found in the AI textbook
        cGrid = grid.clone()
        root = Node(cGrid)
        while self.timeRemains():
            leaf = self.select(root)
            child = self.expand(leaf)
            res = self.simulate(child)
            self.backProp(res, child)
        return # the move in ACTIONS(state) whose node has highest number of playouts

    def timeRemains(self):
        if(time.process_time() - self.time_limit > 0):
            return False
        else:
            return True

    # PARAM: Node obj node
    # from node, select best (using UCB1) 
    def select(self, node):
        # TODO:
            # 
        while len(node.children) != 0:
            for child in node.children: 
                #go thru and check each with UCB1
                pass
        return node
    
    def expand(self, leaf):
        return
    
    def simulate(self, child):
        return
    
    def backProp(self, result, child):
        return
    
    # PARAM: Node object node
    # using UCT formula (upper confidence bound applied to trees)
    def UCB1(self, node):
        C = math.sqrt(2) # textbooks says this is works well throetically
        return ((node.total_wins / node.total_playouts) +
                    (C * math.sqrt(math.log(node.parent.total_playouts) / node.total_playouts)))
                