from random import randint, choice
from BaseAI_3 import BaseAI
from Grid_3 import Grid
import time

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

# original code
# class ComputerAI(BaseAI):
#     def getMove(self, grid):
#         cells = grid.getAvailableCells()
#         return cells[randint(0, len(cells) - 1)] if cells else None

class RandomAI(BaseAI):
    # Random AI movement
    def getMove(self, grid):
        cells = grid.getAvailableCells()
        return cells[randint(0, len(cells) - 1)] if cells else None

class MinimaxAI(BaseAI):
    def __init__(self, depth=6):
        self.max_depth = depth

    def getMove(self, grid):
        # loops through all possible moves
        # simulates move and evaluates using min() for random tile placements
        # returns the best score
        best_score = float('-inf')
        best_move = None
        for direction in vecIndex:
            grid_clone = grid.clone()
            grid_clone.move(direction)
            score = self.min(grid_clone, depth=1, alpha=float('-inf'), beta=float('inf'))
            if score > best_score:
                best_score = score
                best_move = direction
        return best_move

    def min(self, grid, depth, alpha, beta):
        # simulates random tile placement (of a 2 or 4)
        # tries to minimize score
        # calls max() to alternate turns
        if depth >= self.max_depth or not grid.canMove():
            return self.eval(grid)
        min_score = float('inf')
        cells = grid.getAvailableCells()
        for direction in vecIndex:
            grid_copy = grid.clone()
            if grid_copy.move(direction):
                score = self.max(grid_copy, depth + 1, alpha, beta)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return min_score

    def max(self, grid, depth, alpha, beta):
        # simulates the ai moves
        # tries to maximize the score
        # calls min() to alternate turns
        if depth >= self.max_depth or not grid.canMove():
            return self.eval(grid)
        max_score = float('-inf')
        moves = grid.getAvailableMoves()
        for direction in vecIndex:
            grid_copy = grid.clone()
            if grid_copy.move(direction):
                score = self.min(grid_copy, depth + 1, alpha, beta)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return max_score
    
    def eval(self, grid):
        # scores the simulation
        # more empty cells and higher max tile is ranked higher
        empty_cells = len(grid.getAvailableCells())
        max_tile = grid.getMaxTile()
        scoring_eq = (2 * empty_cells) + (2 * max_tile)
        return scoring_eq


class MontecarloAI(BaseAI):
    def __init__ (self, max_simulations=1000, max_depth=6, max_time=5.0):
        self.max_simulations = max_simulations
        self.max_depth = max_depth
        self.max_time = max_time

    def getMove(self, grid):
        best_move = None
        best_score = float('-inf')
        start_time = time.time()
        for direction in vecIndex:
            grid_clone = grid.clone()
            grid_clone.move(direction)
            simulations = 0
            total_score = 0
            while simulations < self.max_simulations and (time.time() - start_time) < self.max_time:
                total_score += self.simulate(grid_clone, depth=0)
                simulations += 1
            avg_score = total_score / simulations if simulations > 0 else 0 
            if avg_score > best_score:
                best_score = avg_score
                best_move = direction
        return best_move
    
    def simulate(self, grid, depth):
        current_grid = grid.clone()
        while current_grid.canMove() and depth < self.max_depth:
            possible_moves = current_grid.getAvailableMoves()
            move = choice(possible_moves)
            current_grid.move(move)
            depth += 1
        return current_grid.getMaxTile()
    