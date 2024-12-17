from random import randint
from BaseAI_3 import BaseAI
from Displayer_3 import Displayer
import numpy as np
import time
import math
import random

# NOTE:
# - a playout policy?
# - is there a diff between a terminal node and a node that has been fully expanded?

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

# class for the nodes of the game tree
class Node():
    def __init__(self, state, parent = None, prev_move = None):
        self.state = state # is a Grid obj
        self.parent = parent
        self.prev_move = prev_move # move made to parent state to get here
        self.children = []
        self.total_score = 0
        self.total_playouts = 0
        self.untried = state.getAvailableMoves() # untried moves from this state
    

class montecarloAI(BaseAI):
    time_limit = 0.3
    def getMove(self, grid):
        # based off implementation found in the AI textbook
        cGrid = grid.clone()
        root = Node(cGrid, None)
        while self.timeRemains():
            leaf = self.select(root)
            child = self.expand(leaf)
            res = self.simulate(child)
            self.backProp(res, child)
        # the move in state.getAvailableMoves whose node has highest number of playouts
        best_move = None
        max_playouts = 0
        for child in root.children:
            if child.total_playouts > max_playouts:
                best_move = child.prev_move
                max_playouts = child.total_playouts
        return best_move
            

    def timeRemains(self):
        if(time.process_time() - self.time_limit > 0):
            return False
        else:
            return True

    # PARAM: Node obj node
    # from node, select best (using UCB1) 
    def select(self, node):
        best_node = node
        best_val = -float('inf')
        while node.children: # go until we hit a leaf
            for child in node.children: # go thru each child on this level
                if(self.UCB1(child) > best_val): # calculate the best one (using selection policy)
                    best_val = self.UCB1(child)
                    best_node = child
            node = best_node # start again with the children of this node
        return best_node
    
    def expand(self, node):
        if not node.untried or not node.state.getAvailableMoves():
            return node
        newState = node.state.clone() # make clone of board
        rand_move = random.choice(node.untried) # choose some untried move
        node.untried.remove(rand_move) # move now tried
        newState.move(rand_move) # apply move and create the node
        child = Node(newState, node, rand_move)
        node.children.append(child)
        return child
    
    def simulate(self, node):
        grid = node.state
        while grid.getAvailableMoves() != []:
            rand_move = random.choice(grid.getAvailableMoves())
            grid.move(rand_move)
        return grid.getMaxTile()
    
    
    def backProp(self, result, node):
        while node.parent:
            node.total_playouts += 1
            node.total_score += result
            node = node.parent
        return
    
    # PARAM: Node object node
    # using UCT formula (upper confidence bound applied to trees)
    def UCB1(self, node):
        C = math.sqrt(2) # textbooks says this is works well theoretically
        return ((node.total_score / node.total_playouts) +
                    (C * math.sqrt(math.log(node.parent.total_playouts) / node.total_playouts)))
                