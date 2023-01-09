import LOCATIONS
import numpy as np

class AGENT(LOCATIONS):
    """
    This is the class defining the player's movement and points
    """
    def __init__(self, field_size, windowsWidth, windowsHeight, startRow, startColumn, map) -> None:
        super().__init__(field_size, windowsWidth, windowsHeight, startRow, startColumn)
        self.currentEntityName = "player"
        self.currentRow = startRow
        self.currentColumn = startColumn
        self.setMap(map)

    def move(self, action):
        if (action == 'left'):
            newColumn = self.currentColumn - 1
            if (self.isOutOfBounds(self.currentRow, newColumn)):
                # reset to start? don't do anything - act as wall?
                pass

        elif (action == 'right'):
            newColumn = self.currentColumn + 1
            if (self.isOutOfBounds(self.currentRow, newColumn)):
                pass

        elif (action == 'up'):
            newRow = self.currentRow - 1
            if (self.isOutOfBounds(newRow, self.currentColumn)):
                pass

        elif (action == 'down'):
            newRow = self.currentRow + 1
            if (self.isOutOfBounds(newRow, self.currentColumn)):
                pass
        else:
            pass
            # stay at current cell
        pass

    def moveResult(self, row, column):
        """
        Returns the new row and column of the agent
        """
        if (self.isOutOfBounds(row, column)):
            # Puts the agent back to the start
            # reward-100
            pass

        elif (self.isWall(row, column)):
            # Agent Cannot Move to cell, so it stays at current location
            pass

        elif (self.isTrap(row, column)):
            # Action is dependent on the trap?
            pass

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

