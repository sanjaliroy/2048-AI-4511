from random import randint
from BaseAI_3 import BaseAI
from ComputerAI_3 import ComputerAI
from Displayer_3 import Displayer
from Grid_3 import Grid
import math
import random


directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
(PLAYER_TURN, COMPUTER_TURN) = (0, 1)
computerAI  = ComputerAI()
possibleNewTiles = [2, 4]

# class for the nodes of the game tree
class Node():
   def __init__(self, state, parent = None, prev_move = None):
       self.state = state
       self.parent = parent
       self.prev_move = prev_move
       self.children = []
       self.total_value = 0
       self.total_playouts = 0
       self.possible_moves = self.state.getAvailableMoves()

   def add_child(self, parent, child_node):
       print("in add child")
       parent.children.append(child_node)
  
class montecarloAI(BaseAI):
    def getMove(self, grid):
       # based off implementation found in the AI textbook
        cGrid = grid.clone()
        print("cGrid: ", cGrid.map)
        root = Node(cGrid)
        while (root.total_playouts < 100):
            curr = root
            print("Root playouts: ", root.total_playouts)
           # if curr = leaf
            print(f"Current node children: {curr.children}")
            if (curr.children == []):
               # if the node has 0 playouts
                if (curr.total_playouts == 0):
                   val = self.rollout(curr)
                   print(f"Backpropagating value: {val}")
                   self.backProp(val, curr)
                else:
                   # if node does not have 0 playouts
                   # all the possible moves become children
                    print(f"Expanding node: {curr.state.map}")
                    for move in curr.possible_moves:
                        print("Move: ", move)
                        if move is not None and move >= 0 and move < 4:
                            grid_copy = curr.state.clone()
                            print("grid copy: ", grid_copy.map)
                            if grid_copy.canMove([move]):
                            #if grid_copy.canMove([move]):
                                grid_copy.move(move)
                                curr.add_child(curr, Node(grid_copy, curr, move))
                        else:
                            print("Invalid PlayerAI Move - 1")
                       # setting the parent of each child to the current node
                   # choose the first node because all have number of playouts = 0
                    print("Children: ", curr.children)
                    curr = curr.children[0]
           # if curr is NOT a leaf
            else:
                max_val = -(float('inf'))
                max_val_index = 0
               # for each child
                for child in curr.children:
                   # retrieve UCB val
                    UCB_val = self.UCB1(child)
                   # if UCB is greater than current max val
                    if UCB_val > max_val:
                       max_val = UCB_val
                       # take note of index of child in list of children
                       max_val_index = curr.children.index(child)
               # current node is the child with maximum value
                curr = curr.children[max_val_index]
        print("out of while loop")
        max_total_playouts = 0
        max_index = 0
        for child in root.children:
           if child.total_playouts > max_total_playouts:
               max_total_playouts = child.total_playouts
               max_index = root.children.index(child)
        print("best move: ", root.children[max_index].prev_move)
        return root.children[max_index].prev_move # the move in ACTIONS(state) whose node has highest number of playouts
  
    def getNewTileValue(self):
        if randint(0,99) < 100 * 0.9:
            return possibleNewTiles[0]
        else:
            return possibleNewTiles[1]

    def rollout(self, node):
       grid_copy = node.state.clone()
       simulation_node = Node(grid_copy)
       terminal_state = self.simulate(simulation_node)
       return terminal_state.getMaxTile()

    def simulate(self, node):
        turn = PLAYER_TURN
        state_copy = node.state.clone()
        
        while state_copy.canMove():
            if turn == PLAYER_TURN:
               move = random.choice(state_copy.getAvailableMoves())
               # Validate Move
               if move is not None and move >= 0 and move < 4:
                    if state_copy.canMove([move]):
                        state_copy.move(move)
            else:
                move = computerAI.getMove(state_copy)
                # Validate Move
                if move and state_copy.canInsert(move):
                    state_copy.setCellValue(move, self.getNewTileValue())
            turn = 1 - turn
        return state_copy
  
    def backProp(self, val, node):
        curr = node
        while curr is not None:
            curr.total_value += val
            curr.total_playouts = curr.total_playouts + 1
            curr = curr.parent
  
   # PARAM: Node object node
   # using UCT formula (upper confidence bound applied to trees)
    def UCB1(self, node):
       if node.total_playouts == 0:
           return float('inf')
       C = 2 # textbooks says this is works well theoretically
       return ((node.total_value / node.total_playouts) +
                   (C * math.sqrt(math.log(node.parent.total_playouts) / node.total_playouts)))
