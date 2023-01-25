from ClassesMazeEscape.LOCATIONS import LOCATIONS
from ClassesMazeEscape.DEQUE import DEQUE
import random
import math

trapList = ['hole', 'spikeTrap', 'glue']
terrainList = ['wall', 'mountain']
bonusList = ['cup', 'coin']

class ENVIRONMENT(LOCATIONS):
    """
    This is the class for cell information: impassable terrain, traps
    """
    def __init__(self, fieldSize, windowsWidth, windowsHeight, map, isTraps = True, isTerrain = True, numberBonuses = 1) -> None:
        super().__init__(fieldSize, windowsWidth, windowsHeight)
        self.setMap(map)
        self.fieldSize = fieldSize
        self.terrainLocations = list()
        self.trapLocations = list()
        self.bonusLocations = list()
        if (isTraps):
            numberOfTraps =  fieldSize + 1
        else:
            numberOfTraps = 0
        if (isTerrain):
            numberOfTerrains = fieldSize
        else:
            numberOfTerrains = 0
        self.initiateEnvironment(numberOfTerrains, numberOfTraps, numberBonuses)
    
    def addImpassableTerrain(self, row, column, terrainNumber) -> None:
        """"
        Updates the entity at row and column to be an impassable terrain of the given terrain number
        """
        if (self.isCellOpen(row, column) == True and self.isFieldEffect(row, column) == False):
            terrain = terrainList[terrainNumber]
            self.placeOnMap(row, column, terrain)
            self.terrainLocations.append((terrain, (row, column)))

    def addTrap(self, row, column, trapNumber) -> None:
        """
        Updates the entity at row and column to be a trap of the given trap number
        """
        if (self.isCellOpen(row, column) == True and self.isFieldEffect(row, column) == False):
            trap = trapList[trapNumber]
            self.placeOnMap(row, column, trap)
            self.trapLocations.append((trap, (row, column)))

    def addBonus(self, row, column, bonusNumber) -> None:
        """
        Updates the entity at the row and column to be a bonus of the given bonus number
        """
        if (self.isCellOpen(row, column) == True and self.isFieldEffect(row, column) == False):
            bonus = bonusList[bonusNumber]
            self.placeOnMap(row, column, bonus)
            self.bonusLocations.append((bonus, (row, column)))

    def initiateEnvironment(self, numberOfTerrains, numberOfTraps, numberOfBonuses = 1, trapType = None, terrainType = None, bonusType = None):
        """
        Initializes the environment and randomly places 'numberOfWalls' of walls and 'numberOfTraps' of traps on the map
        """
        bounds = self.fieldSize - 1
        if (trapType == None):
            trapNumber = random.randrange(0, len(trapList))
        else:
            trapNumber = trapType
        if (terrainType == None):
            terrainNumber = random.randrange(0, len(terrainList))
        else:
            terrainNumber = terrainType
        if (bonusType == None):
            bonusNumber = random.randrange(0, len(bonusList))
        else:
            bonusNumber = bonusType
        while len(self.trapLocations) < math.ceil(math.pow(numberOfTraps, 2)/5):
            trapColumn = random.randrange(0, bounds)
            trapRow = random.randrange(0, bounds)
            self.addTrap(trapRow, trapColumn, trapNumber)

        while len(self.terrainLocations) < math.ceil(math.pow(numberOfTerrains, 2)/5):
            terrainColumn = random.randrange(0, bounds)
            terrainRow = random.randrange(0, bounds)
            self.addImpassableTerrain(terrainRow, terrainColumn, terrainNumber)
            
        while len(self.bonusLocations) < numberOfBonuses:
            bonusColumn = random.randrange(0, bounds)
            bonusRow = random.randrange(0, bounds)
            self.addBonus(bonusRow, bonusColumn, bonusNumber)
        
        if (self.minPathFinder() == None):
            self.clearEnvironment()
            self.initiateEnvironment(numberOfTerrains, numberOfTraps, numberOfBonuses, trapType, terrainType, bonusType)

    def clearEnvironment(self) -> None:
        """
        Clears all data on previous traps and walls locations, removes all traps and terrain
        """
        while len(self.trapLocations) > 0:
            trapLocation = self.trapLocations.pop()[1]
            trapRow = trapLocation[0]
            trapColumn = trapLocation[1]
            self.setEmpty(trapRow, trapColumn)
        while len(self.terrainLocations) > 0:
            terrainLocation = self.terrainLocations.pop()[1]
            terrainRow = terrainLocation[0]
            terrainColumn = terrainLocation[1]
            self.setEmpty(terrainRow, terrainColumn)
        while len(self.bonusLocations) > 0:
            bonusLocation = self.bonusLocations.pop()[1]
            bonusRow = bonusLocation[0]
            bonusColumn = bonusLocation[1]
            self.setEmpty(bonusRow, bonusColumn)

    def minPathFinder(self) -> bool:
        """
        This uses the breadth-first search algorithm to find the minimum path from start to end
        """
        startRow, startColumn = self.getStart()
        queue = DEQUE()
        queue.enqueue((startRow, startColumn, 0))
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        visited = [[False] * self.fieldSize for _ in range(self.fieldSize)]

        while queue.length != 0:
            coord = queue.dequeue()
            visited[coord[0]][coord[1]] = True

            if (self.getFieldEffect(coord[0], coord[1]) == 'end'):
                # end was reached, so return the shortest length to the end
                return coord[2]
            
            for dir in directions:
                newRow = coord[0] + dir[0]
                newColumn = coord[1] + dir[1]
                if newRow < 0 or newRow >= self.fieldSize or newColumn < 0 or newColumn >= self.fieldSize or visited[newRow][newColumn]:
                    continue
                else:
                    if (self.getEntity(newRow, newColumn) in terrainList):
                        continue
                queue.enqueue((newRow, newColumn, coord[2] + 1))

    def initializeLocations(self) -> None:
        """
        Iterates through all the cells and keeps track of all locations of the entities on the map
        """
        for row in range(0, self.fieldSize):
            for column in range(0, self.fieldSize):
                entityAtCell = self.getEntity(row, column)
                if entityAtCell in trapList:
                    self.trapLocations.append((entityAtCell, (row, column)))
                elif entityAtCell in terrainList:
                    self.terrainLocations.append((entityAtCell, (row, column)))
                elif entityAtCell in bonusList:
                    self.bonusLocations.append((entityAtCell, (row, column)))