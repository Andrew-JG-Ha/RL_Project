import numpy as np

class LOCATIONS:
    """
    This is the base class for all movement and positioning of entities onto the board
    """
    def __init__(self, field_size, windowsDimensions:type[np.array(int, int)], current_locations:type[np.array] = None) -> None:
        self.currentEntityName = ""
        self.currentLocationX
        self.currentLocationY 
        if (current_locations.size == 0 or current_locations == None):
            self.dataStructure = initializeLocations(field_size, windowsDimensions[0], windowsDimensions[1])
        else:
            self.dataStructure = current_locations

    def getLocations(self, entityType:type[str]):
        """
        Returns an array of locations of the searched for object
        """
        np.array()
        return np.argwhere(self.dataStructure['entity'] == entityType)

    def setLocation(self, newValueX, newValueY) -> None:
        """
        Sets the location of the current object
        """
        self.dataStructure[newValueY][newValueX]['entity'] = self.currentEntityName

    def moveLocation(self, newValueX, newValueY):
        """
        Moves the object to the next specified location, then returns the updated locations of all parts
        """
        pass


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
