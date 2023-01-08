import pygame
import random
import numpy as np
"""
1. Create the environment, 5x5 (scalable maze, code it so that it can be as large as I want) maze with obstacles and rewards
2. General class for the player agent (can eventually lead to enemies?)
    - movement (left, right, up, down) --> w,a,s,d?
3. Scoring:
    - Finishing the maze
    - Bonuses in the maze
    - Maybe adding steps constraint
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

def generate_environment(screen, seed=0, field_size=5):
    """
    generates the environment, creates the playing field, and randomly places obstacles and bonuses.
    assigns:
    - start location
    - end location
    - 3 * Walls
    - 3 * Ditches
    """
    screen.fill(white)
    create_grid(screen, field_size)
    
def create_grid(screen, field_size=5):
    partition_width = int(windowsWidth/field_size)
    partition_height = int(windowsHeight/field_size)
    for partition_number in range(1, field_size):
        pygame.draw.line(screen, black, start_pos=(int(partition_number*partition_width), 0), end_pos=(int(partition_number*partition_width), windowsHeight), width=2) # draw vertical lines
        pygame.draw.line(screen, black, start_pos=(0, int(partition_number*partition_height)), end_pos=(windowsWidth, int(partition_number*partition_height)), width=2) # draw horizontal lines

def main():
    pygame.init()
    running = True

    horizontal_partitions = 5
    vertical_partitions = 5
    gameDisplay = pygame.display.set_mode((windowsWidth, windowsHeight))
    
    pygame.display.set_caption("Maze Escape")
    while running:
        
        generate_environment(gameDisplay, seed=0, field_size=5)
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == "__main__":
    main()