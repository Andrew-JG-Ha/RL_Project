import LOCATIONS
import numpy as np

class AGENT(LOCATIONS):
    """
    This is the class defining the player's movement and points
    """
    def __init__(self, field_size, windowsWidth, windowsHeight, startRow, startColumn, map:type[np.array] = None) -> None:
        super().__init__(field_size, windowsWidth, windowsHeight, map)
        self.currentEntityType = "player"
        self.currentRow = startRow
        self.currentColumn = startColumn

    def move(self, action):
        pass