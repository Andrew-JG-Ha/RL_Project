import numpy as np

class LOCATIONS:
    """
    This is the base class for all movement and positioning of entities onto the board
    """
    def __init__(self, field_size, windowsWidth, windowsHeight) -> None:
        self.map = initializeLocations(field_size, windowsWidth, windowsHeight)
        self.fieldSize = field_size

    def __init__(self, field_size, windowsWidth, windowsHeight, startCoord, endCoord) -> None:
        self.map = initializeLocations(field_size, windowsWidth, windowsHeight)
        self.fieldSize = field_size
        self.updateStartLocation(startCoord[0], startCoord[1])
        self.updateEndLocation(endCoord[0], endCoord[1])

    def getLocations(self, entityType:type[str]):
        """
        Returns an array of locations of the searched for entity
        """
        return np.argwhere(self.dataStructure['entity'] == entityType)

    def getEntity(self, row, column) -> str:
        """
        Returns the entity stored at the row and column entered
        """
        return self.dataStructure[row][column]["entity"]
    
    def getMap(self):
        """
        Returns the current ndarray map
        """
        return self.map

    def setMap(self, map):
        """
        Update the existing map stored within object
        """
        self.map = map
    
    def placeOnMap(self, row, column, entityName) -> None:
        """
        Places an object on the map
        """
        self.map[row][column]['entity'] = entityName

    def updateEntityLocation(self, previousRow, previousColumn, newRow, newColumn, entityName) -> None:
        """
        Updates the location of the current object
        """
        self.map[previousRow][previousColumn]['entity'] = ''
        self.map[newRow][newColumn]['entity'] = entityName

    def updateStartLocation(self, newRow, newColumn):
        """
        Updates the location of the start
        """
        currentLocation = self.getLocations('start')
        self.updateEntityLocation(currentLocation[0], currentLocation[1], newRow, newColumn, 'start')

    def updateEndLocation(self, newRow, newColumn):
        """
        Updates the location of the end
        """
        currentLocation = self.getLocations('end')
        self.updateEntityLocation(currentLocation[0], currentLocation[1], newRow, newColumn, 'end')

    def isCellOpen(self, row, column) -> bool:
        """
        Returns a boolean on if the specified cell has an entity already
        """
        if (self.dataStructure[row][column]['entity'] == ""):
            return True
        else:
            return False

    def showBoard(self) -> None:
        """"
        Prints out the board and what is stored in the data structures
        """
        print('─'*(16*self.fieldSize-self.fieldSize))
        for numRows in range(0, self.fieldSize):
            for numColumns in range(0, self.fieldSize):
                print("| {:12} ".format(self.map[numRows][numColumns]['entity']), end='')
            print("|")
            print('─'*(16*self.fieldSize-self.fieldSize))
                
    def clearBoard(self) -> None:
        """
        Removes all entities on the board and resets them to be empty strings: ''
        """
        self.map['entity'] = ''

    def randomizeStartEnd(self):
        """
        Randomize the locations of the start and end and ensure they are on opposite ends of one another
        """

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