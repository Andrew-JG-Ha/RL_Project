class LOCATIONS:
    """
    This is the base class for all movement and positioning of entities onto the board
    """
    def __init__(self) -> None:
        pass

    def getLocation(self):
        pass

    def setLocation(self):
        pass




class AGENT(LOCATIONS):
    """
    This is the class defining the player's movement and points
    """
    def __init__(self) -> None:
        super().__init__()

class OBSTRUCTIONS(LOCATIONS):
    """
    This is the class for obstacles: walls, ditches, traps
    """
    def __init__(self) -> None:
        super().__init__()

class BONUSES(LOCATIONS):
    """
    This is the class for bonuses that can be places around the map
    """
    def __init__(self) -> None:
        super().__init__()