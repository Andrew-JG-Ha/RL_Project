import pygame
import numpy as np
import pickle as pkl
import os
from ClassesMazeEscape.LOCATIONS import LOCATIONS
from ClassesMazeEscape.AGENT import AGENT
from ClassesMazeEscape.ENVIRONMENT import ENVIRONMENT, trapList, terrainList, bonusList

"""
1. Create the environment, 5x5 (scalable maze, code it so that it can be as large as I want) maze with obstacles and rewards
2. General class for the player agent (can eventually lead to enemies?)
    - movement (left, right, up, down) --> w,a,s,d?
3. Scoring:
    - Finishing the maze
    - Bonuses in the maze
    - Maybe adding steps constraint
    - Time Limit?
4. Obstacles/Bonuses
    - Ditches: Restart
    - Walls: Can't pass
    - Traps: Deduction in moves or points
    - Trophy: +10 points
"""
# GENERATE EMPTY MAP FUNCTION
def generateEmptyMap(_fieldSize, _windowsWidth, _windowsHeight):
    """
    Creates and returns an empty map with no terrain or traps
    """
    newMap = LOCATIONS(_fieldSize, _windowsWidth, _windowsHeight)
    emptyMap = ENVIRONMENT(_fieldSize, _windowsWidth, _windowsHeight, newMap.getMap())
    emptyMap.clearEnvironment()
    return emptyMap.getMap()

# COLORS
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

# RESOLUTION
windowsWidth = 1280
windowsHeight = 720
textAreaHeight = 80
fieldSize = 8

# EMPTY MAP INITIALIZATION
emptyMap = generateEmptyMap(fieldSize, windowsWidth, windowsHeight)
print(emptyMap.dtype)

# PYGAME WINDOW INITIALIZATION AND IMAGE LOADING
pygame.init()
coinImg = pygame.image.load("RL_Custom_Env\GameImages\coin.png")
emptyImg = pygame.image.load("RL_Custom_Env\GameImages\empty.png")
glueImg = pygame.image.load("RL_Custom_Env\GameImages\glue.png")
holeImg = pygame.image.load("RL_Custom_Env\GameImages\hole.png")
mountainImg = pygame.image.load("RL_Custom_Env\GameImages\mountain.png")
playerImg = pygame.image.load("RL_Custom_Env\GameImages\player.png")
spikeTrapImg = pygame.image.load("RL_Custom_Env\GameImages\spikeTrap.png")
cupImg = pygame.image.load("RL_Custom_Env\GameImages\cup.png")
wallImg = pygame.image.load("RL_Custom_Env\GameImages\wall.png")
endImg = pygame.image.load("RL_Custom_Env\GameImages\emptyEnd.png")

# FONT
courierNew = pygame.font.SysFont('couriernew', 30, True, False)

class mazeEscape():
    def __init__(self, _fieldSize = fieldSize, _windowsWidth = windowsWidth, _windowsHeight = windowsHeight, _textAreaHeight = textAreaHeight, _map = emptyMap) -> None:
        self.gameDisplay = initializePygame(_windowsWidth, _windowsHeight, _textAreaHeight)

        self.fieldSize = _fieldSize
        self.windowsWidth = _windowsWidth
        self.windowsHeight = _windowsHeight
        self.textAreaHeight = _textAreaHeight
        if (_map is emptyMap):
            map = LOCATIONS(_fieldSize, _windowsWidth, _windowsHeight).getMap()
            self.environment = ENVIRONMENT(_fieldSize, _windowsWidth, _windowsHeight, map)
        elif ((self.fieldSize != fieldSize or self.windowsHeight != windowsHeight or self.windowsWidth != windowsWidth) and _map is emptyMap):
            map = LOCATIONS(_fieldSize, _windowsWidth, _windowsHeight).getMap()
            self.environment = ENVIRONMENT(_fieldSize, _windowsWidth, _windowsHeight, map)
        else:
            map = _map
            self.environment = ENVIRONMENT(_fieldSize, _windowsWidth, _windowsHeight, map)

        self.agent = AGENT(_fieldSize, _windowsWidth, _windowsHeight, map)
        self.initialMap = map.copy()

        self.maxSteps = _fieldSize*4
        self.state = (self.agent.currentRow, self.agent.currentColumn)
        self.observationSpace = (_fieldSize, _fieldSize)
        self.actionSpace = self.agent.validActions

    def generateBlankDisplay(self) -> None:
        """
        Generates the blank display, creates the playing field
        """
        self.gameDisplay.fill(white, rect = (0, windowsHeight, windowsWidth, windowsHeight+textAreaHeight))
        self.create_grid()
        
    def create_grid(self) -> None:
        """
        Generates the grids onto the gameDisplay of the pygame window
        """
        partition_width = int(self.windowsWidth/self.fieldSize)
        partition_height = int(self.windowsHeight/self.fieldSize)
        for partition_number in range(1, self.fieldSize):
            pygame.draw.line(self.gameDisplay, black, start_pos=(int(partition_number*partition_width), 0), end_pos=(int(partition_number*partition_width), self.windowsHeight), width=2) # draw vertical lines
            pygame.draw.line(self.gameDisplay, black, start_pos=(0, int(partition_number*partition_height)), end_pos=(self.windowsWidth, int(partition_number*partition_height)), width=2) # draw horizontal lines
        pygame.draw.line(self.gameDisplay, black, start_pos=(0, self.windowsHeight), end_pos=(self.windowsWidth, self.windowsHeight), width=5)

    def renderEnvironment(self) -> None:
        """
        Loads and places the images onto the board 
        """
        widthScaleFactor = self.windowsWidth/self.fieldSize
        heightScaleFactor = self.windowsHeight/self.fieldSize
        for row in range(0, self.fieldSize):
            for column in range(0, self.fieldSize):
                entityType = self.environment.getEntity(row, column)
                imageYPos = self.environment.getMap()[row][column]['y_pos']
                imageXPos = self.environment.getMap()[row][column]['x_pos']
                entityImage = getImage(entityType)
                if (self.environment.getFieldEffect(row, column) == 'end'):
                    entityImage = endImg
                entityImage = pygame.transform.scale(entityImage, (widthScaleFactor, heightScaleFactor))
                self.gameDisplay.blit(entityImage, (imageXPos, imageYPos))

    def regenerateEnvironment(self):
        """
        Randomizes the map and resets the players 
        """
        self.environment.clearEnvironment()
        self.environment.remakeMap()
        self.environment.initiateEnvironment(self.fieldSize, self.fieldSize)
        self.agent.restartPlayer()

    def putText(self, inputText:type[str]):
        """
        Places inputText at centered at location
        """
        location = (self.windowsWidth//2, self.windowsHeight+self.textAreaHeight//2)
        text = courierNew.render(inputText, True, black, white)
        textRectangle = text.get_rect()
        textCenter = textRectangle.center
        locationX = location[0] - textCenter[0]
        locationY = location[1] - textCenter[1]
        self.gameDisplay.blit(text, (locationX, locationY))

    def step(self, action):
        """
        Take an action from the action space and have the RL model apply it to the board
        """
        previousTotalReward = self.agent.getScore()
        self.agent.move(mapAction(action))
        self.state = (self.agent.currentRow, self.agent.currentColumn)
        actionReward = self.agent.getScore() - previousTotalReward
        self.maxSteps -= 1
        if self.agent.isCurrentEnd() or self.maxSteps < 0:
            done = True
        elif self.agent.getScore() < self.agent.minReward:
            done = True
        else:
            done = False
        return self.state, actionReward, done

    def render(self):
        """
        Render and show the current state of the game, where the agent's at and what the current map looks like
        """
        self.renderEnvironment()
        self.generateBlankDisplay()
        self.putText("Score:{}".format(self.agent.getScore()))
        pygame.display.update()

    def reset(self):
        """
        Resets the agent to the start and resets the map
        """
        self.maxSteps = self.fieldSize*4
        self.environment.clearEnvironment()
        self.environment.setMap(self.initialMap.copy())
        self.agent.setMap(self.environment.getMap())
        self.agent.restartPlayer()
        self.state = (self.agent.currentRow, self.agent.currentColumn)
        return self.state

    def playGame(self, repeatMap = False):
        """
        Allows the user to play the game, it will be initialized to be in the state of a 10x10 square map unless fieldSize is changed
        """
        running = True

        round = 0
        while running:
            self.renderEnvironment()
            self.generateBlankDisplay()
            self.putText("Round:{}, Score:{}".format(round, self.agent.getScore()))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.agent.move('down')
                    if event.key == pygame.K_UP:
                        self.agent.move('up')
                    if event.key == pygame.K_RIGHT:
                        self.agent.move('right')
                    if event.key == pygame.K_LEFT:
                        self.agent.move('left')
            if (self.agent.isCurrentEnd() and repeatMap == False):
                round += 1
                self.regenerateEnvironment()
            elif (self.agent.isCurrentEnd() and repeatMap == True):
                round += 1
                self.reset()
        self.close()

    def close(self):
        """
        Close the pygame environment
        """
        pygame.quit()

# Helper Functions
def getImage(entityName):
    """
    Gets and returns the corresponding instance of the image (one-hot encoding)
    """
    if (entityName == 'coin'):
        return coinImg
    elif (entityName == 'glue'):
        return glueImg
    elif (entityName == 'hole'):
        return holeImg
    elif (entityName == 'mountain'):
        return mountainImg
    elif (entityName == 'player'):
        return playerImg
    elif (entityName == 'spikeTrap'):
        return spikeTrapImg
    elif (entityName == 'cup'):
        return cupImg
    elif (entityName == 'wall'):
        return wallImg
    else:
        return emptyImg

def initializePygame(_windowsWidth, _windowsHeight, _textAreaHeight):
    pygame.init()
    pygame.display.init()
    gameDisplay = pygame.display.set_mode((_windowsWidth, _windowsHeight + _textAreaHeight))
    pygame.display.set_caption("Maze Escape")
    return gameDisplay

def mapAction(action) -> str:
    """
    Maps an integer value from 0->3 to a string action
    0 -> up
    1 -> down
    2 -> left
    3 -> right
    """
    if action == 0:
        return "up"
    elif action == 1:
        return "down"
    elif action == 2:
        return "left"
    elif action == 3:
        return "right"
    else:
        return action
