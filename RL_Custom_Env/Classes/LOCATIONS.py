import numpy as np

class LOCATIONS:
    """
    This is the base class for all movement and positioning of entities onto the board
    """
    def __init__(self, current_locations) -> None:
        self.dataStructure = np.zeros()

    def getLocation(self) -> np.array[chr ,(int, int)]:
        """
        Returns the location of the current object
        """
        pass

    def setLocation(self) -> None:
        """
        Sets the location of the current object
        """
        pass

    def moveLocation(self):
        """
        Moves the object to the next specified location, then returns the updated locations of all parts
        """
        pass