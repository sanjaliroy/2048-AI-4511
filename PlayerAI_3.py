from random import randint
from BaseAI_3 import BaseAI
from Displayer_3 import Displayer
import numpy as np

class PlayerAI(BaseAI):
	depth = 0
	
	def getMove(self, grid):
		(maxChild, maxUtility) = self.maximize(grid, -float('inf'), float('inf'))
		move = self.findmove(grid, maxChild)
		self.depth = 0
		return move
	
	def children(self, grid):
		children = []
		if grid.canMove():
			for move in grid.getAvailableMoves():
				child = grid.clone()
				child.move(move)
				children.append(child)
		return children

	def findmove(self, grid, child):
		for move in grid.getAvailableMoves():
			testchild = grid.clone()
			testchild.move(move)
			if child.map == testchild.map:
				return move

	def minimize(self, grid, alpha, beta):
		if not grid.getAvailableCells():
			return (None, self.evaluate(grid))
		(minChild, minUtility) = (None, float('inf'))
		cells = grid.getAvailableCells()
		move = cells[randint(0, len(cells) - 1)]
		child = grid.clone()
		child.map[move[0]][move[1]] = self.getNewTileValue()
		self.depth += 1
		(_, utility) = self.maximize(child, alpha, beta)
		if utility < minUtility:
			(minChild, minUtility) = (child, utility)
		if minUtility <= alpha:
			return (minChild, minUtility)
		if minUtility < beta:
			beta = minUtility
		return (minChild, minUtility)

	def maximize(self, grid, alpha, beta):
		if self.depth>=5:
			return (None, self.evaluate(grid))
		(maxChild, maxUtility) = (None, -float('inf'))
		self.depth += 1
		for child in self.children(grid):
			(_, utility) = self.minimize(child, alpha, beta)
			if utility > maxUtility:
				(maxChild, maxUtility) = (child, utility)
			if maxUtility >= beta:
				return (maxChild, maxUtility)
			if maxUtility > alpha:
				alpha = maxUtility
		return (maxChild, maxUtility)

	def getNewTileValue(self):
		if randint(0,99) < 90: 
			return 2 
		else: 
			return 4

	def evaluate(self, grid):
		value = len(grid.getAvailableCells())**2 + grid.getMaxTile()
		return value
