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
        # Create the root node with the initial state
        cGrid = grid.clone()
        print("cGrid: ", cGrid.map)
        root = Node(cGrid)

        while root.total_playouts < 100:  # Adjust simulation count as needed
            curr = root
            print(f"Root playouts: {root.total_playouts}")

            # Selection: Traverse to a leaf node
            while curr.children:
                max_val = float('-inf')
                best_child = None
                for child in curr.children:
                    ucb1_val = self.UCB1(child)
                    if ucb1_val > max_val:
                        max_val = ucb1_val
                        best_child = child
                curr = best_child
                print(f"Traversing to child node: {curr.state.map}")

            # Expansion or Rollout
            if curr.children == []:
                print(f"Current node is a leaf with state: {curr.state.map}")
                if curr.total_playouts == 0:
                    print(f"Performing rollout for state: {curr.state.map}")
                    val = self.rollout(curr)
                    print(f"Rollout returned value: {val}")
                    self.backProp(val, curr)
                else:
                    print(f"Expanding node: {curr.state.map}")
                    possible_moves = curr.state.getAvailableMoves()
                    for move in possible_moves:
                        grid_copy = curr.state.clone()
                        if grid_copy.canMove([move]):
                            grid_copy.move(move)
                            curr.add_child(curr, Node(grid_copy, curr, move))
                            print(f"Added child with move {move}: {grid_copy.map}")
            else:
                # If we somehow get stuck, break out (this is a safeguard)
                print("Breaking loop to avoid infinite traversal.")
                break

        # Choose the best move
        best_child = max(root.children, key=lambda child: child.total_playouts)
        print(f"Best move: {best_child.prev_move}")
        return best_child.prev_move
            
  
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
