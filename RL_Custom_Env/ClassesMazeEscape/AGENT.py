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
        self.totalReward = 0
        self.actionLog = list()

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
        self.actionLog.append(action)


    def isMoveValid(self, row, column):
        """
        Checks to see if the move is a valid move and assigns appropriate deductions 
        """
        if (self.isOutOfBounds(row, column)):
            # Remains on same cell
            self.totalReward -= 100
            return False
        else:
            if (self.isTrap(row, column)):
                # Action is dependent on the trap - will add later
                # Can move onto a trap but deduction in points
                self.totalReward -= 25
                # Traps will have unique abilities - to be added
                return True
            elif (self.isWall(row, column)):
                self.totalReward -= 100
                return False
            else:
                # Is valid move, no deduction
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
        Checks if this current cell is a trap, and returns penalty
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

    def isCurrentEnd(self) -> bool:
        """
        Checks to see if the player's current cell is the end cell
        """
        fieldEffect = self.getFieldEffect(self.currentRow, self.currentColumn)
        if (fieldEffect == "end"):
            return True
        else:
            return False

    def restartPlayer(self):
        """
        Sets the player to the starting cell and resets all scoring and logs
        """
        self.totalReward = 0
        self.actionLog.clear()
        previousColumn = self.currentColumn
        previousRow = self.currentRow
        self.currentRow, self.currentColumn = self.getStart()
        self.updateEntityLocation(previousRow, previousColumn, self.currentRow, self.currentColumn)