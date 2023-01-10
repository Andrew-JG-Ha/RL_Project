from ClassesMazeEscape.LOCATIONS import LOCATIONS
import numpy as np

class AGENT(LOCATIONS):
    """
    This is the class defining the player's movement and points
    """
    def __init__(self, field_size, windowsWidth, windowsHeight, map, startRow = None, startColumn = None) -> None:
        super().__init__(field_size, windowsWidth, windowsHeight)
        self.currentEntityName = "player"
        if (startColumn is not None and startRow is not None):
            self.currentRow = startRow
            self.currentColumn = startColumn
        else:
            self.currentRow, self.currentColumn = self.getStart()
        self.setMap(map)
        self.placeOnMap(self.currentRow, self.currentColumn, self.currentEntityName)
        self.totalReward = 0

    def move(self, action):
        if (action == 'left'):
            newColumn = self.currentColumn - 1
            if (self.moveValid == True):
                previousColumn = self.currentColumn
                self.currentColumn = newColumn
                self.updateEntityLocation(self.currentRow, previousColumn, self.currentRow, self.currentColumn)

        elif (action == 'right'):
            newColumn = self.currentColumn + 1
            if (self.moveValid == True):
                previousColumn = self.currentColumn
                self.currentColumn = newColumn
                self.updateEntityLocation(self.currentRow, previousColumn, self.currentRow, self.currentColumn)

        elif (action == 'up'):
            if (self.moveValid == True):
                previousRow = self.currentRow
                self.currentRow = newRow
                self.updateEntityLocation(previousRow, self.currentColumn, self.currentRow, self.currentColumn)

        elif (action == 'down'):
            newRow = self.currentRow + 1
            if (self.moveValid == True):
                previousRow = self.currentRow
                self.currentRow = newRow
                self.updateEntityLocation(previousRow, self.currentColumn, self.currentRow, self.currentColumn)
        else:
            pass
            # stay at current cell
        pass

    def moveValid(self, row, column):
        """
        Returns the new row and column of the agent
        """
        if (self.isOutOfBounds(row, column) or self.isWall(row, column)):
            # Remains on same cell
            self.totalReward -= 100
            return False

        elif (self.isTrap(row, column)):
            # Action is dependent on the trap?
            # Can move onto a trap but deduction in points
            self.totalReward -= 25
            # Traps will have unique abilities - to be added
            return False
        else:
            # Is valid move, no deduction
            return True

    def isOutOfBounds(self, row, column) -> bool:
        """
        Checks if the current cell is out of bounds, is outside the play area
        """
        if (row < 0 or row > self.fieldSize):
            return True
        if (column < 0 or column > self.fieldSize):
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
        else:
            return False

    def isTrap(self, row, column) -> bool:
        """
        Checks if this current cell is a trap, and returns penalty
        """
        entityOnCell = self.getEntity(row, column)
        if (entityOnCell == 'ditch'):
            return True
        else:
            return False

