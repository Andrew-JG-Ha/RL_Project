from ClassesMazeEscape.ENVIRONMENT import ENVIRONMENT
from collections import deque


class PATHFINDER:
    """
    uses the breadth-first search algorithm to search for a path
    """
    def __init__(self, map:type[ENVIRONMENT]) -> None:
        self.map = map
        self.fieldSize = map.fieldSize
    
    def solveMaze(self):
        """
        Applies the breadth-first search algorithm to solve the maze given in the map
        """
        startRow, startColumn = self.map.getStart()
        for row in range(self.map.)
        
    