import numpy as np
import random

class LOCATIONS:
    """
    This is the base class for all movement and positioning of entities onto the board
    """
    def __init__(self, fieldSize, windowsWidth, windowsHeight) -> None:
        self.map = initializeLocations(fieldSize, windowsWidth, windowsHeight)
        self.fieldSize = fieldSize
        self.isContinuousGame = False
        self.randomizeStartEnd()

    def getLocations(self, entityType:type[str]):
        """
        Returns an array of locations of the searched for entity
        """
        return np.argwhere(self.map['entity'] == entityType)

    def getEntity(self, row, column) -> str:
        """
        Returns the entity stored at the row and column entered
        """
        return self.map[row][column]["entity"]
    
    def getFieldEffect(self, row, column) -> str:
        """
        Returns the Field Effect name at the row and column entered
        """
        return self.map[row][column]["fieldEffect"]

    def getMap(self):
        """
        Returns the current ndarray map
        """
        return self.map

    def getStart(self):
        """
        Returns the start coordinates
        """
        startCoords = np.argwhere(self.map['fieldEffect'] == 'start')[0]
        return startCoords[0], startCoords[1]

    def getFieldSize(self):
        """
        Returns the fieldSize
        """
        return self.fieldSize

    def setMap(self, map):
        """
        Update the existing map stored within object
        """
        self.map = map

    def setStart(self, row, column):
        """
        Updates the fieldEffect member in the datastructure to be 'start'
        """
        self.map[row][column]['fieldEffect'] = 'start'

    def setEnd(self, row, column):
        """
        Updates the fieldEffect member in the datastructure to be 'end'
        """
        self.map[row][column]['fieldEffect'] = 'end'
    
    def setEmpty(self, row, column) -> None:
        """
        Sets the input row and column's entity value to be '' (empty)
        """
        self.map[row][column]['entity'] = ''
    
    def placeOnMap(self, row, column, entityName) -> None:
        """
        Places an object on the map
        """
        self.map[row][column]['entity'] = entityName

    def updateEntityLocation(self, previousRow, previousColumn, newRow, newColumn) -> None:
        """
        Updates the location of the current object
        """
        entityName = self.map[previousRow][previousColumn]['entity']
        self.map[previousRow][previousColumn]['entity'] = ''
        self.map[newRow][newColumn]['entity'] = entityName

    def updateStartLocation(self, newRow, newColumn) -> None:
        """
        Updates the location of the start
        """
        previousLocations = np.argwhere(self.map['fieldEffect'] == 'start')
        for location in previousLocations:
            self.map[location[0]][location[1]]['fieldEffect'] = ''
        self.map[newRow][newColumn]['fieldEffect'] = 'start'

    def updateEndLocation(self, newRow, newColumn) -> None:
        """
        Updates the location of the end
        """
        previousLocations = np.argwhere(self.map['fieldEffect'] == 'end')
        for location in previousLocations:
            self.map[location[0]][location[1]]['fieldEffect'] = ''
        self.map[newRow][newColumn]['fieldEffect'] = 'end'

    def isCellOpen(self, row, column) -> bool:
        """
        Returns a boolean on if the specified cell has an entity already
        """
        if (self.map[row][column]['entity'] == ''):
            return True
        else:
            return False

    def isFieldEffect(self, row, column) -> bool:
        """
        Returns a boolean on if the specified cell has a field effect
        """
        if (self.map[row][column]['fieldEffect'] == ''):
            return False
        else:
            return True

    def showBoard(self) -> None:
        """"
        Prints out the board and what is stored in the data structures
        """
        print('???'*(16*self.fieldSize-self.fieldSize))
        for numRows in range(0, self.fieldSize):
            for numColumns in range(0, self.fieldSize):
                if (self.map[numRows][numColumns]['fieldEffect'] == 'start'):
                    print("|S:{:12}".format(self.map[numRows][numColumns]['entity']), end='')
                elif (self.map[numRows][numColumns]['fieldEffect'] == 'end'):
                    print("|E:{:12}".format(self.map[numRows][numColumns]['entity']), end='')
                else:
                    print("| {:12} ".format(self.map[numRows][numColumns]['entity']), end='')
            print("|")
            print('???'*(16*self.fieldSize-self.fieldSize))
                
    def clearBoard(self) -> None:
        """
        Removes all entities on the board and resets them to be empty strings: ''
        """
        self.map['entity'] = ''
        self.map['fieldEffect'] = ''

    def randomizeStartEnd(self) -> None:
        """
        Randomize the locations of the start and end and ensure they are on opposite ends of one another
        """
        bounds = self.fieldSize - 1
        startColumn = random.choice([0, bounds]) # 0 means start will be on left side, 1 means start will be on the right side
        endColumn = bounds
        if (startColumn == bounds):
            endColumn = 0
        startRow = random.randint(0, bounds)
        endRow = random.randint(0, bounds)
        if (startRow == endRow):
            startRow = (startRow + 1) % bounds
            endRow = (endRow - 1) % bounds
        self.updateStartLocation(startRow, startColumn)
        self.updateEndLocation(endRow, endColumn)

    def remakeMap(self) -> None:
        """
        Restarts and resets the map, randomizes the start and end locations
        """
        self.clearBoard()
        self.randomizeStartEnd()

# Helper Functions
def initializeLocations(fieldSize, windowsWidth, windowsHeight):
    initialDS = np.zeros((fieldSize, fieldSize), dtype=[('entity', '<U20'), ('x_pos', '<i8'), ('y_pos', '<i8'), ('fieldEffect', '<U20')])
    partitionWidth = int(windowsWidth/fieldSize)
    partitionHeight = int(windowsHeight/fieldSize)
    for partitionNumberX in range(0, fieldSize):
        for partitionNumberY in range(0, fieldSize):
            initialDS[partitionNumberY][partitionNumberX]['x_pos'] = partitionNumberX*partitionWidth 
            initialDS[partitionNumberY][partitionNumberX]['y_pos'] =  + partitionNumberY*partitionHeight 
    return initialDS