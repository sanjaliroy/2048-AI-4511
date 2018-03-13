from random import randint
from BaseAI_3 import BaseAI
from Displayer_3 import Displayer
import numpy as np

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

class PlayerAI(BaseAI):
	depth = 0
	mon_grad = np.array([[ 7,  6,  5,  4],
						 [ 6,  5,  4, 3],
						 [ 5,  4, 3, 2],
						 [ 4, 3, 2, 1]])

	def getMove(self, grid):
		(maxChild, maxUtility) = self.maximize(grid, -float('inf'), float('inf'))
		move = maxChild[1]
		self.depth = 0
		return move
	
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
			child.insertTile(cell, 4)
			children.append(child)
		return children

	def minimize(self, grid, alpha, beta):
		if not grid.getAvailableCells():
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
		if self.depth>=6 or not grid.getAvailableMoves():
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



	# def compactness(self,grid):
	# 	down=0;
	# 	up=0;
	# 	d1=0;
	# 	d2=0;
	# 	u1=0;
	# 	u2=0;
	# 	for x in range(grid.size):
	# 		for y in range(grid.size):
	# 			if(grid.map[x][y] !=0):
	# 				if(x>=y):
	# 					d1=d1+1;
	# 				else:
	# 					d2=d2+1;
	# 				if(x+y>=3):
	# 					u1=u1+1;
	# 				else:
	# 					u2=u2+1;
	# 		down=abs(d1-d2)
	# 		up=abs(u1-u2)
	# 		if(down>=up):
	# 			return down
	# 		else:
	# 			return up

	# def edgeBonus(self,grid):
	# 	r1=0
	# 	r2=0
	# 	d1=0
	# 	d2=0
	# 	max=0
	# 	list=[]
	# 	for x in range(grid.size):
	# 		r1=r1+grid.map[x][0]
	# 		r2=r2+grid.map[x][grid.size-1]
	# 	if(r1<r2):
	# 		r1=r2
	# 	for y in range(grid.size):
	# 		d1=d1+grid.map[0][y]
	# 		d2=d2+grid.map[grid.size-1][y]
	# 	if(d1<d2):
	# 		d1=d2
	# 	if(r1<d1):
	# 		r1=d1
	# 	return r1

	# def monotonic(self,grid):
	# 	penalty=0
	# 	inc=0
	# 	dec=0
	# 	vertical=0;# vertical penalty incresases going downwards
	# 	for x in range(grid.size):
	# 		for y in range(grid.size-1):
	# 			a= grid.map[x][y]
	# 			b= grid.map[x][y+1]
				
	# 			if((a==0) or (b==0) ):
	# 				pass
	# 			else: # should increase  going left->right
	# 				if(a > b):
	# 					inc=inc+1        # does not decrease so penalty
		
	# 	for y in range(grid.size):
	# 		for x in range(grid.size-1):
	# 			a= grid.map[x][y]
	# 			c= grid.map[x+1][y]
	# 			if((a==0) or (c==0)):
	# 				pass
	# 			else:
	# 				if(a>c):
	# 					vertical=vertical+1
		
	# 	return inc+vertical


	# def eval(self,grid):
	# 	f1= grid.getMaxTile()*2;
	# 	f2= len(grid.getAvailableCells())*400

	# 	f4= self.compactness(grid)*300
	# 	f5= self.edgeBonus(grid)*7
	# 	f6= self.monotonic(grid)*(-1000) #penalty
	# 	#print "heuristic",f1,f2,f4,f5,f6;
	# 	sv= f1+f2+f4+f5+f6  # static value
	# 	return sv
# --------------------------------
	# def evaluate(self, grid):
	# 	# monotonicity = np.sum(self.mon_grad*np.array(grid.map))
	# 	# value = len(grid.getAvailableCells())**2 + grid.getMaxTile()**0.5 + monotonicity**0.5
	# 	# return value

	# 	smoothWeight = 0.1
	# 	monoWeight  = 1.0
	# 	emptyWeight  = 2.7
	# 	maxWeight    = 1.0
	# 	empty = 1 if len(grid.getAvailableCells()) == 0 else len(grid.getAvailableCells())
	# 	return self.smoothness(grid) * smoothWeight + \
	# 		self.monotonicity(grid)*monoWeight + \
	# 		np.log(empty)*emptyWeight +\
	# 		grid.getMaxTile()*maxWeight

	# def smoothness(self, grid):
	# 	smoothness = 0
	# 	for i in range(4):
	# 		for j in range(4):
	# 			if not grid.canInsert((i,j)):
	# 				value = np.log(grid.map[i][j])/np.log(2)
	# 				for vector in [RIGHT_VEC, DOWN_VEC]:
	# 					targetCell = self.findfarthest(grid, (i,j), vector)['far']
	# 					if not grid.canInsert(targetCell):
	# 						target = grid.getCellValue(targetCell)
	# 						targetValue = np.log(target)/np.log(2)
	# 						smoothness -= abs(value - targetValue)
	# 	return smoothness


	# def monotonicity(self, grid):
	# 	totals = [0, 0, 0, 0]
	# 	# up/down
	# 	for i in range(4):
	# 		current = 0
	# 		nxt = current + 1
	# 		while nxt < 4:
	# 			while nxt < 4 and grid.canInsert((i, nxt)):
	# 				nxt+=1
	# 			if nxt >= 4:
	# 				nxt -= 1
	# 			currentValue = np.log(grid.getCellValue((i, current)))/np.log(2) if not grid.canInsert((i, current)) else 0
	# 			nextValue = np.log(grid.getCellValue((i, nxt)))/np.log(2) if not grid.canInsert((i, nxt)) else 0
	# 			if currentValue > nextValue:
	# 				totals[0] += nextValue - currentValue
	# 			elif nextValue > currentValue:
	# 				totals[1] += currentValue - nextValue
	# 			current = nxt
	# 			nxt += 1

	# 	# left/right
	# 	for j in range(4):
	# 		current = 0
	# 		nxt = current + 1
	# 		while nxt < 4:
	# 			while nxt < 4 and grid.canInsert((nxt, j)):
	# 				nxt+=1
	# 			if nxt >= 4:
	# 				nxt -= 1
	# 			currentValue = np.log(grid.getCellValue((current, j)))/np.log(2) if not grid.canInsert((current, j)) else 0
	# 			nextValue = np.log(grid.getCellValue((nxt, j)))/np.log(2) if not grid.canInsert((nxt, j)) else 0
	# 			if currentValue > nextValue:
	# 				totals[2] += nextValue - currentValue
	# 			elif nextValue > currentValue:
	# 				totals[3] += currentValue - nextValue
	# 			current = nxt
	# 			nxt += 1
	# 	return max(totals[0], totals[1]) + max(totals[2], totals[3])


	# def findfarthest(self, grid, cell, vector):
	# 	while True:
	# 		prev = cell
	# 		cell = (prev[0] + vector[0], prev[1] + vector[1])
	# 		if grid.crossBound(cell) or not grid.canInsert(cell):
	# 			return {'far': prev, 'nxt': cell}

# -------------------------------------------


	def evaluate(self, board,commonRatio=0.25):
		linearWeightedVal = 0
		invert = False
		weight = 1.
		malus = 0
		criticalTile = (-1,-1)
		for y in range(0,4):
			for x in range(0,4):
				b_x = x
				b_y = y
				if invert:
					b_x = 4 - 1 - x
				#linearW
				currVal=board.getCellValue((b_x,b_y))
				if(currVal == 0 and criticalTile == (-1,-1)):
					criticalTile = (b_x,b_y)
				linearWeightedVal += currVal*weight
				weight *= commonRatio
			invert = not invert
			
		linearWeightedVal2 = 0
		invert = False
		weight = 1.
		malus = 0
		criticalTile2 = (-1,-1)
		for x in range(0,4):
			for y in range(0,4):
				b_x = x
				b_y = y
				if invert:
					b_y = 4 - 1 - y
				#linearW
				currVal=board.getCellValue((b_x,b_y))
				if(currVal == 0 and criticalTile2 == (-1,-1)):
					criticalTile2 = (b_x,b_y)
				linearWeightedVal2 += currVal*weight
				weight *= commonRatio
			invert = not invert
			
		
		linearWeightedVal3 = 0
		invert = False
		weight = 1.
		malus = 0
		criticalTile3 = (-1,-1)
		for y in range(0,4):
			for x in range(0,4):
				b_x = x
				b_y = 4 - 1 - y
				if invert:
					b_x = 4 - 1 - x
				#linearW
				currVal=board.getCellValue((b_x,b_y))
				if(currVal == 0 and criticalTile3 == (-1,-1)):
					criticalTile3 = (b_x,b_y)
				linearWeightedVal3 += currVal*weight
				weight *= commonRatio
			invert = not invert
			
		linearWeightedVal4 = 0
		invert = False
		weight = 1.
		malus = 0
		criticalTile4 = (-1,-1)
		for x in range(0,4):
			for y in range(0,4):
				b_x = 4 - 1 - x
				b_y = y
				if invert:
					b_y = 4 - 1 - y
				#linearW
				currVal=board.getCellValue((b_x,b_y))
				if(currVal == 0 and criticalTile4 == (-1,-1)):
					criticalTile4 = (b_x,b_y)
				linearWeightedVal4 += currVal*weight
				weight *= commonRatio
			invert = not invert
			
			
		linearWeightedVal5 = 0
		invert = True
		weight = 1.
		malus = 0
		criticalTile5 = (-1,-1)
		for y in range(0,4):
			for x in range(0,4):
				b_x = x
				b_y = y
				if invert:
					b_x = 4 - 1 - x
				#linearW
				currVal=board.getCellValue((b_x,b_y))
				if(currVal == 0 and criticalTile5 == (-1,-1)):
					criticalTile5 = (b_x,b_y)
				linearWeightedVal5 += currVal*weight
				weight *= commonRatio
			invert = not invert
			
		linearWeightedVal6 = 0
		invert = True
		weight = 1.
		malus = 0
		criticalTile6 = (-1,-1)
		for x in range(0,4):
			for y in range(0,4):
				b_x = x
				b_y = y
				if invert:
					b_y = 4 - 1 - y
				#linearW
				currVal=board.getCellValue((b_x,b_y))
				if(currVal == 0 and criticalTile6 == (-1,-1)):
					criticalTile6 = (b_x,b_y)
				linearWeightedVal6 += currVal*weight
				weight *= commonRatio
			invert = not invert
			
		
		linearWeightedVal7 = 0
		invert = True
		weight = 1.
		malus = 0
		criticalTile7 = (-1,-1)
		for y in range(0,4):
			for x in range(0,4):
				b_x = x
				b_y = 4 - 1 - y
				if invert:
					b_x = 4 - 1 - x
				#linearW
				currVal=board.getCellValue((b_x,b_y))
				if(currVal == 0 and criticalTile7 == (-1,-1)):
					criticalTile7 = (b_x,b_y)
				linearWeightedVal7 += currVal*weight
				weight *= commonRatio
			invert = not invert
			
		linearWeightedVal8 = 0
		invert = True
		weight = 1.
		malus = 0
		criticalTile8 = (-1,-1)
		for x in range(0,4):
			for y in range(0,4):
				b_x = 4 - 1 - x
				b_y = y
				if invert:
					b_y = 4 - 1 - y
				#linearW
				currVal=board.getCellValue((b_x,b_y))
				if(currVal == 0 and criticalTile8 == (-1,-1)):
					criticalTile8 = (b_x,b_y)
				linearWeightedVal8 += currVal*weight
				weight *= commonRatio
			invert = not invert
			
		maxVal = max(linearWeightedVal,linearWeightedVal2,linearWeightedVal3,linearWeightedVal4,linearWeightedVal5,linearWeightedVal6,linearWeightedVal7,linearWeightedVal8)
		if(linearWeightedVal2 > linearWeightedVal):
			linearWeightedVal = linearWeightedVal2
			criticalTile = criticalTile2
		if(linearWeightedVal3 > linearWeightedVal):
			linearWeightedVal = linearWeightedVal3
			criticalTile = criticalTile3
		if(linearWeightedVal4 > linearWeightedVal):
			linearWeightedVal = linearWeightedVal4
			criticalTile = criticalTile4
		if(linearWeightedVal5 > linearWeightedVal):
			linearWeightedVal = linearWeightedVal5
			criticalTile = criticalTile5
		if(linearWeightedVal6 > linearWeightedVal):
			linearWeightedVal = linearWeightedVal6
			criticalTile = criticalTile6
		if(linearWeightedVal7 > linearWeightedVal):
			linearWeightedVal = linearWeightedVal7
			criticalTile = criticalTile7
		if(linearWeightedVal8 > linearWeightedVal):
			linearWeightedVal = linearWeightedVal8
			criticalTile = criticalTile8
		
		return maxVal
