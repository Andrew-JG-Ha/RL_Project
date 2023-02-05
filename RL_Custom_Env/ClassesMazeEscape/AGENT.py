from ClassesMazeEscape.LOCATIONS import LOCATIONS
import numpy as np

class AGENT(LOCATIONS):
    """
    This is the class defining the player's movement and points
    """
    def __init__(self, fieldSize, windowsWidth, windowsHeight, map, startRow = None, startColumn = None) -> None:
        super().__init__(fieldSize, windowsWidth, windowsHeight)
        self.currentEntityName = "player"
        self.setMap(map)
        if (startColumn is not None and startRow is not None):
            self.currentRow = startRow
            self.currentColumn = startColumn
        else:
            self.currentRow, self.currentColumn = self.getStart()

        self.placeOnMap(self.currentRow, self.currentColumn, self.currentEntityName)

        self.minReward = -0.5 * self.getMap().size
        self.totalReward = 0.0
        
        self.actionLog = list()
        self.visited = set()
        self.visited.add((self.currentRow, self.currentColumn))

        self.validActions = {"up":0, "down":1, "left":2, "right":3}

    def move(self, action):
        if (action == 'left'):
            newColumn = self.currentColumn - 1
            if (self.isMoveValid(self.currentRow, newColumn) == True):
                previousColumn = self.currentColumn
                self.currentColumn = newColumn
                self.updateEntityLocation(self.currentRow, previousColumn, self.currentRow, self.currentColumn)
        elif (action == 'right'):
            newColumn = self.currentColumn + 1
            if (self.isMoveValid(self.currentRow, newColumn) == True):
                previousColumn = self.currentColumn
                self.currentColumn = newColumn
                self.updateEntityLocation(self.currentRow, previousColumn, self.currentRow, self.currentColumn)
        elif (action == 'up'):
            newRow = self.currentRow - 1
            if (self.isMoveValid(newRow, self.currentColumn) == True):
                previousRow = self.currentRow
                self.currentRow = newRow
                self.updateEntityLocation(previousRow, self.currentColumn, self.currentRow, self.currentColumn)
        elif (action == 'down'):
            newRow = self.currentRow + 1
            if (self.isMoveValid(newRow, self.currentColumn) == True):
                previousRow = self.currentRow
                self.currentRow = newRow
                self.updateEntityLocation(previousRow, self.currentColumn, self.currentRow, self.currentColumn)
        else:
            pass
            # stay at current cell
        self.visited.add((self.currentRow, self.currentColumn))
        self.actionLog.append(action)


    def isMoveValid(self, row, column):
        """
        Checks to see if the move is a valid move and assigns appropriate deductions 
        """
        if (self.isOutOfBounds(row, column)):
            # Remains on same cell
            self.totalReward += (self.minReward - 1)
            return False
        else:
            if (self.isTrap(row, column)):
                self.totalReward -= 0.15
                return True
            if (self.isWall(row, column)):
                self.totalReward -= 0.75
                return False
            if (self.isBonus(row, column)):
                self.totalReward += 10
                return True
            if ((row, column) in self.visited):
                self.totalReward -=0.45
                return True
            else:
                self.totalReward -=0.05
                return True

    def isOutOfBounds(self, row, column) -> bool:
        """
        Checks if the current cell is out of bounds, is outside the play area
        """
        if (row < 0 or row >= self.fieldSize):
            return True
        if (column < 0 or column >= self.fieldSize):
            return True
        return False
        
    def isWall(self, row, column) -> bool:
        """
        Checks if the current cell is of a field effect that doesn't allow the user to be on the cell
        - Mountains
        - Rivers
        """
        entityOnCell = self.getEntity(row, column)
        if (entityOnCell == 'wall'):
            return True
        elif (entityOnCell == 'river'):
            return True
        elif (entityOnCell == 'blockade'):
            return True
        elif (entityOnCell == 'mountain'):
            return True
        else:
            return False

    def isTrap(self, row, column) -> bool:
        """
        Checks if this current cell is a trap
        """
        entityOnCell = self.getEntity(row, column)
        if (entityOnCell == 'hole'):
            return True
        elif (entityOnCell == 'spikeTrap'):
            return True
        elif (entityOnCell == 'glue'):
            return True
        else:
            return False

    def isBonus(self, row, column) -> bool:
        """
        Checks if this current cell is a bonus
        """
        entityOnCell = self.getEntity(row, column)
        if (entityOnCell == 'coin'):
            return True
        elif (entityOnCell == 'cup'):
            return True
        else:
            return False

    def isCurrentEnd(self) -> bool:
        """
        Checks to see if the player's current cell is the end cell
        """
        fieldEffect = self.getFieldEffect(self.currentRow, self.currentColumn)
        if (fieldEffect == "end"):
            self.totalReward += 25
            return True
        else:
            return False

    def restartPlayer(self):
        """
        Sets the player to the starting cell and resets all scoring and logs
        """
        self.totalReward = 0
        self.actionLog.clear()
        self.visited = set()
        self.currentRow, self.currentColumn = self.getStart()
        self.placeOnMap(self.currentRow, self.currentColumn, self.currentEntityName)

    def getScore(self) -> float:
        """
        Returns the current score of the agent
        """
        return self.totalReward

    def printLog(self):
        """
        Prints the actions taken and the total score
        """
        print("Total Actions: {}".format(len(self.actionLog)))
        print("Total Score: {}".format(self.totalReward))