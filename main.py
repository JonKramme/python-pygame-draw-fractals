import sys, pygame
import numpy as np

pygame.init()
points = []
lastPoint = None
size = width, height = 320, 240
black = 0, 0, 0
drawing = True
screen = pygame.display.set_mode(size)
pointDistance = 5

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if pygame.mouse.get_pressed()[0] == 1:
            if lastPoint is not None:
                mouse = np.array(pygame.mouse.get_pos())
                if np.linalg.norm(lastPoint - mouse) > pointDistance:
                    points.append(lastPoint)
                    lastPoint = mouse

            else:
                lastPoint = np.array(pygame.mouse.get_pos())

        if pygame.mouse.get_pressed() == (0, 0, 1):
            lastPoint = pygame.mouse.get_pos()

    #screen.fill(black)
    if drawing and len(points) > 0:
        lp = points[0]
        for x in points[1::]:
            pygame.draw.line(screen, (255, 255, 255), lp, x, 1)
            lp = x
        pygame.draw.line(screen, (255, 255, 255), lastPoint, lp, 1)

    pygame.display.flip()
