import numpy as np

class LOCATIONS:
    """
    This is the base class for all movement and positioning of entities onto the board
    """
    def __init__(self, field_size, windowsWidth, windowsHeight, current_locations:type[np.array] = None) -> None:
        self.currentEntityType = ""
        if (current_locations == None):
            self.dataStructure = initializeLocations(field_size, windowsWidth, windowsHeight)
        else:
            self.dataStructure = current_locations

    def getLocations(self, entityType:type[str]):
        """
        Returns an array of locations of the searched for object
        """
        return np.argwhere(self.dataStructure['entity'] == entityType)

    def setLocation(self, row, column) -> None:
        """
        Sets the location of the current object
        """
        self.dataStructure[row][column]['entity'] = self.currentEntityName

    def isCellOpen(self, row, column) -> bool:
        """
        Returns a boolean on if the specified cell had an entity already
        """
        if (self.dataStructure[row][column]['entity'] == ""):
            return False
        else:
            return True

    def updateEntity(self, row, column, newEntity:type[str]):
        """
        Updates the specified array cell's entity type
        """
        self.dataStructure[row][column]

    def showBoard(self) -> None:
        """"
        Prints out the board and what is stored in the data structures
        """
        pass

# Helper Functions
def initializeLocations(field_size, windowsWidth, windowsHeight):
    initialDS = np.zeros((field_size, field_size), dtype=[('entity', '<U20'), ('x_pos', '<i8'), ('y_pos', '<i8')])
    partitionWidth = int(windowsWidth/field_size)
    partitionHeight = int(windowsHeight/field_size)
    partitionWidthHalved = int(partitionWidth/2)
    partitionHeightHalved = int(partitionHeight/2)
    for partitionNumberX in range(0, field_size):
        for partitionNumberY in range(0, field_size):
            initialDS[partitionNumberY][partitionNumberX]['x_pos'] = partitionWidthHalved + partitionNumberX*partitionWidth
            initialDS[partitionNumberY][partitionNumberX]['y_pos'] = partitionHeightHalved + partitionNumberY*partitionHeight
    return initialDS
