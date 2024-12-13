from random import randint
from BaseAI_3 import BaseAI
from Displayer_3 import Displayer
import numpy as np
import time

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

class PlayerAI(BaseAI):
	depth = 0
	time = 0

	def getMove(self, grid):
		self.depth = 0
		self.time = time.process_time()
		(maxChild, maxUtility) = self.maximize(grid, -float('inf'), float('inf'))
		move = maxChild[1]
		# self.evaluate(maxChild[0],True)
		
		return move

	def timeup(self, depth):
		diff = time.process_time() - self.time
		if diff >= 0.1/depth:
			return True
		else:
			return False
	
	def maxchildren(self, grid):
		children = []
		if grid.canMove():
			for move in grid.getAvailableMoves():
				child = grid.clone()
				child.move(move)
				children.append((child, move))
		return children

	def minchildren(self, grid):
		children = []
		for cell in grid.getAvailableCells():
			child = grid.clone()
			child.insertTile(cell, 2)
			children.append(child)
		#	child.insertTile(cell, 4)
		#	children.append(child)
		return children

	def minimize(self, grid, alpha, beta):
		if self.timeup(self.depth+1) or not grid.getAvailableCells():
			return (None, self.evaluate(grid))
		(minChild, minUtility) = (None, float('inf'))
		self.depth += 1
		for child in self.minchildren(grid):
			(_, utility) = self.maximize(child, alpha, beta)
			if utility < minUtility:
				(minChild, minUtility) = (child, utility)
			if minUtility <= alpha:
				return (minChild, minUtility)
			if minUtility < beta:
				beta = minUtility
		return (minChild, minUtility)

	def maximize(self, grid, alpha, beta):
		if not grid.getAvailableMoves():
			return (None, self.evaluate(grid))
		(maxChild, maxUtility) = (None, -float('inf'))
		self.depth += 1
		for child in self.maxchildren(grid):
			(_, utility) = self.minimize(child[0], alpha, beta)
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

	def cellOccupied(self, grid, pos):
		return not not grid.getCellValue(pos)

	def monoton(self, grid):
	 	return np.log(np.sum(self.mon_grad*np.array(grid.map)))


	def evaluate(self, grid, prt = False):
		emptycells = len(grid.getAvailableCells())
		empty = emptycells if emptycells else 1
		smoothWeight = 0.5
		monoWeight  = 3.0 / empty
		emptyWeight  = 2.7 / empty
		maxWeight    = 4.0
		smooth = self.smoothness(grid) * smoothWeight
		monoton = self.monotonicity(grid) * monoWeight
		emptiness = np.log(empty) * emptyWeight
		maxval = self.max4tile(grid) * maxWeight
		total = smooth + monoton + emptiness + maxval
		if prt:
			print('smooth: ', smooth)
			print('monoton:', monoton)
			print('emptiness: ', emptiness)
			print('maxvalue: ', maxval)
			print('total: ', total)
		return total

	def smoothness(self, grid):
		smoothness = 0
		for i in range(4):
			for j in range(4):
				if not grid.canInsert((i,j)):
					value = np.log(grid.map[i][j])/np.log(2)
					for vector in [RIGHT_VEC, DOWN_VEC]:
						targetCell = self.findfarthest(grid, (i,j), vector)
						if self.cellOccupied(grid, targetCell):
							target = grid.getCellValue(targetCell)
							targetValue = np.log(target)/np.log(2)
							smoothness -= abs(value - targetValue)
		return smoothness

	def maxtile(self, grid):
		return np.log(grid.getMaxTile())/np.log(2)

	def max4tile(self, grid):
		arr = np.array(grid.map).reshape(16)
		top = np.sort(arr)[-4::]
		val = np.sum(top*np.array([1,2,4,8]))
		return np.log(val)


	def monotonicity(self, grid):
		totals = [0, 0, 0, 0]
		# up/down
		for i in range(4):
			current = 0
			nxt = current + 1
			while nxt < 4:
				while nxt < 4 and grid.canInsert((i, nxt)):
					nxt+=1
				if nxt >= 4:
					nxt -= 1
				currentValue = np.log(grid.getCellValue((i, current)))/np.log(2) if not grid.canInsert((i, current)) else 0
				nextValue = np.log(grid.getCellValue((i, nxt)))/np.log(2) if not grid.canInsert((i, nxt)) else 0
				if currentValue > nextValue:
					totals[0] += nextValue - currentValue
				elif nextValue > currentValue:
					totals[1] += currentValue - nextValue
				current = nxt
				nxt += 1

		# left/right
		for j in range(4):
			current = 0
			nxt = current + 1
			while nxt < 4:
				while nxt < 4 and grid.canInsert((nxt, j)):
					nxt+=1
				if nxt >= 4:
					nxt -= 1
				currentValue = np.log(grid.getCellValue((current, j)))/np.log(2) if not grid.canInsert((current, j)) else 0
				nextValue = np.log(grid.getCellValue((nxt, j)))/np.log(2) if not grid.canInsert((nxt, j)) else 0
				if currentValue > nextValue:
					totals[2] += nextValue - currentValue
				elif nextValue > currentValue:
					totals[3] += currentValue - nextValue
				current = nxt
				nxt += 1
		return max(totals[0], totals[1]) + max(totals[2], totals[3])


	def findfarthest(self, grid, cell, vector):
		while True:
			prev = cell
			cell = (prev[0] + vector[0], prev[1] + vector[1])
			if not grid.crossBound(cell) and grid.canInsert(cell):
				continue
			else:
				return cell
