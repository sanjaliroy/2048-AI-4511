from Grid_3       import Grid
# from ComputerAI_3 import ComputerAI # 300
from ComputerAI_3 import RandomAI # 150
from ComputerAI_3 import MinimaxAI # 200
from ComputerAI_3 import MontecarloAI # 250
from PlayerAI_3   import PlayerAI
from Displayer_3  import Displayer
from random       import randint
import time

# NOTE: make sure you only have ONE uncommmented out of the following
# Random Search -> search "150" and uncomment those lines
# Minimax Search -> search "200" and uncomment those lines
# Monte Carlo Search -> search "250" and uncomment those lines
# original code -> to be deleted, "300"

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time Limit Before Losing
timeLimit = 0.2
allowance = 0.05

# time benchmarks at score 
benchmarks = [0,0,0,0]

class GameManager:
    def __init__(self, size = 4):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles  = defaultInitialTiles
        # self.computerAI = None # 300
        # self.randomAI = None #150
        # self.minimaxAI = None #200
        self.montecarloAI = None #250
        self.playerAI   = None
        self.displayer  = None
        self.over       = False

    # def setComputerAI(self, computerAI): # 300
    #     self.computerAI = computerAI

    # new additions
    # def setRandomAI(self, randomAI): # 150
    #     self.randomAI = randomAI

    # def setMinimaxAI(self, minimaxAI): # 200
    #     self.minimaxAI = minimaxAI

    def setMontecarloAI(self, montecarloAI): # 250
        self.montecarloAI = montecarloAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI

    def setDisplayer(self, displayer):
        self.displayer = displayer

    # def updateAlarm(self, currTime):
    #     if currTime - self.prevTime > timeLimit + allowance:
    #         self.over = True
    #     else:
    #         while time.clock() - self.prevTime < timeLimit + allowance:
    #             pass

    #         self.prevTime = time.clock()

    def start(self):
        for i in range(self.initTiles):
            self.insertRandomTile()

        # self.displayer.display(self.grid)

        # Player AI Goes First
        turn = PLAYER_TURN
        maxTile = 0

        self.prevTime = time.process_time()

        while not self.isGameOver() and not self.over:
            # Copy to Ensure AI Cannot Change the Real Grid to Cheat
            gridCopy = self.grid.clone()

            move = None

            if turn == PLAYER_TURN:
                #print("Player's Turn:", end="")
                move = self.playerAI.getMove(gridCopy)
                #print(actionDic[move])

                # Validate Move
                if move != None and move >= 0 and move < 4:
                    if self.grid.canMove([move]):
                        self.grid.move(move)

                        # Update maxTile
                        maxTile = self.grid.getMaxTile()
                    else:
                        print("Invalid PlayerAI Move")
                        self.over = True
                else:
                    print("Invalid PlayerAI Move - 1")
                    self.over = True
            else:
                #print("Computer's turn:")
                # move = self.computerAI.getMove(gridCopy) # 300
                # move = self.randomAI.getMove(gridCopy) # 150
                # move = self.minimaxAI.getMove(gridCopy) # 200 
                move = self.montecarloAI.getMove(gridCopy) # 250

                # Validate Move
                if move and self.grid.canInsert(move):
                    self.grid.setCellValue(move, self.getNewTileValue())
                else:
                    print("Invalid Computer AI Move")
                    self.over = True

            # if not self.over:
            #     self.displayer.display(self.grid)

            # Exceeding the Time Allotted for Any Turn Terminates the Game
            # self.updateAlarm(time.clock())

            turn = 1 - turn
        return maxTile

    def isGameOver(self):
        return not self.grid.canMove()

    def getNewTileValue(self):
        if randint(0,99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1];

    def insertRandomTile(self):
        tileValue = self.getNewTileValue()
        cells = self.grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)

def main():
    gameManager = GameManager()
    playerAI  	= PlayerAI()
    # computerAI  = ComputerAI() # 300
    # randomAI = RandomAI() # 150
    # minimaxAI = MinimaxAI() # 200
    montecarloAI = MontecarloAI() # 250
    displayer 	= Displayer()

    gameManager.setDisplayer(displayer)
    gameManager.setPlayerAI(playerAI)
    # gameManager.setComputerAI(computerAI) # 300
    # gameManager.setRandomAI(randomAI) # 150
    # gameManager.setMinimaxAI(minimaxAI) # 200
    gameManager.setMontecarloAI(montecarloAI) # 250

    start = time.process_time()
    maxTile = gameManager.start()
    end = time.process_time()
    print("COLLECTED DATA:")
    print("------------------------------")
    print("SCORE:", maxTile)
    print("Total elapsed CPU time:", end - start)

if __name__ == '__main__':
    main()
