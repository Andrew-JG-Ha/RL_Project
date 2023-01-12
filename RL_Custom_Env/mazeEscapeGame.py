import pygame
import numpy as np
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
# COLORS
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

# RESOLUTION
windowsWidth = 1280
windowsHeight = 720
textAreaHeight = 80

# PYGAME WINDOW INITIALIZATION AND IMAGE LOADING
pygame.init()
gameDisplay = pygame.display.set_mode((windowsWidth, windowsHeight+textAreaHeight))
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

def generate_blank_environment(gameDisplay, field_size=5):
    """
    Generates the environment, creates the playing field, and randomly places obstacles and bonuses.
    assigns:
    - start location
    - end location
    - Walls
    - Ditches

    returns a data structure (numpy array of characters, where each character relates to the status of the cell) 
    that contains the details on the placement of all obstacles, and the start and end locations
    [[1, 1, 1]
     [1, 1, 1]
     [1, 1, 1]]
    """
    create_grid(gameDisplay, field_size)
    
def create_grid(gameDisplay, field_size=5):
    """
    Generates the grids onto the gameDisplay of the pygame window
    """
    partition_width = int(windowsWidth/field_size)
    partition_height = int(windowsHeight/field_size)
    for partition_number in range(1, field_size):
        pygame.draw.line(gameDisplay, black, start_pos=(int(partition_number*partition_width), 0), end_pos=(int(partition_number*partition_width), windowsHeight), width=2) # draw vertical lines
        pygame.draw.line(gameDisplay, black, start_pos=(0, int(partition_number*partition_height)), end_pos=(windowsWidth, int(partition_number*partition_height)), width=2) # draw horizontal lines

def renderEnvironment(environment:type[ENVIRONMENT], fieldSize, windowsWidth, windowsHeight):
    """
    Loads and places the images onto the board 
    """
    widthScaleFactor = windowsWidth/fieldSize
    heightScaleFactor = windowsHeight/fieldSize
    bounds = fieldSize
    map = environment.getMap()
    for row in range(0, bounds):
        for column in range(0, bounds):
            entityType = environment.getEntity(row, column)
            imageYPos = map[row][column]['y_pos']
            imageXPos = map[row][column]['x_pos']
            entityImage = getImage(entityType)
            if (environment.getFieldEffect(row, column) == 'end'):
                entityImage = endImg
            entityImage = pygame.transform.scale(entityImage, (widthScaleFactor, heightScaleFactor))
            gameDisplay.blit(entityImage, (imageXPos, imageYPos))

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

def regenerateEnvironment(environment, agent, fieldSize):
    """
    Randomizes the map and resets the players 
    """
    environment.clearEnvironment()
    environment.remakeMap()
    environment.initiateEnvironment(fieldSize, fieldSize)
    agent.restartPlayer()

def main():
    render = True
    continuous = True

    running = True
    fieldSize = 5

    map = LOCATIONS(fieldSize, windowsWidth, windowsHeight)
    environment = ENVIRONMENT(fieldSize, windowsWidth, windowsHeight, map.getMap())
    myAgent = AGENT(fieldSize, windowsWidth, windowsHeight, map.getMap())

    pygame.display.set_caption("Maze Escape")
    if (render == True):
        while running:
            renderEnvironment(environment, fieldSize, windowsWidth, windowsHeight)
            generate_blank_environment(gameDisplay, field_size=fieldSize)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        myAgent.move('down')
                    if event.key == pygame.K_UP:
                        myAgent.move('up')
                    if event.key == pygame.K_RIGHT:
                        myAgent.move('right')
                    if event.key == pygame.K_LEFT:
                        myAgent.move('left')

            if (myAgent.isCurrentEnd() and continuous == True):
                myAgent.printLog()
                regenerateEnvironment(environment, myAgent, fieldSize)

            elif (myAgent.isCurrentEnd() and continuous == False):
                break
    pygame.quit()
if __name__ == "__main__":
    main()