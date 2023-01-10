import pygame
import random
import numpy as np
import sys
from ClassesMazeEscape.LOCATIONS import LOCATIONS
from ClassesMazeEscape.AGENT import AGENT
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

def generate_environment(gameDisplay, seed=0, field_size=5):
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
    gameDisplay.fill(white)
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

def main():
    pygame.init()
    running = True

    fieldSize = 5

    # map = LOCATIONS(fieldSize, windowsWidth, windowsHeight)

    test123 = LOCATIONS(fieldSize, windowsWidth, windowsHeight)
    testMap = test123.getMap()
    myAgent = AGENT(fieldSize, windowsWidth, windowsHeight, testMap)
    myStart = test123.getStart()
    test123.showBoard()

    # test = np.zeros((5, 5), dtype=[('entity', '<U10'), ('x_pos', '<i8'), ('y_pos', '<i8'), ('isStart', '?'), ('isEnd', '?')])
    # test[0][0].T[0] = "test123123"
    # test[1][1].T[0] = "test123123"
    # test[0][1].T[0] = "HELLO WORLD"


    gameDisplay = pygame.display.set_mode((windowsWidth, windowsHeight))
    
    pygame.display.set_caption("Maze Escape")
    while running:
        generate_environment(gameDisplay, seed=0, field_size=fieldSize)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == "__main__":
    main()