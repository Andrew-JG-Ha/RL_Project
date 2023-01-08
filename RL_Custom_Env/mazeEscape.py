import pygame

pygame.init()

windowsWidth = 750
windowsHeight = 500
windowsDimensions = (windowsWidth, windowsHeight)

screen = pygame.display.set_mode(windowsDimensions)
running = True

# COLORS
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(white)

    pygame.draw.rect(screen, blue, rect=[100,100,50,50])
    pygame.draw.lines(screen, black, points=[(100, 100), (200,200), (300,300)], closed=False)
    pygame.display.flip()

pygame.quit()