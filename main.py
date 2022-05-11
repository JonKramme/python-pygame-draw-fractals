import sys, pygame
import time
#https://medium.com/@hhtun21/l-systems-draw-your-first-fractals-139ed0bfcac2
import numpy as np

theta = np.radians(270)
rotation = np.array(((np.cos(theta), -np.sin(theta)),
                     (np.sin(theta),  np.cos(theta))))

pointTranslations = None
pygame.init()
points = []
size = height, width = 800, 600
black = 0, 0, 0
white = 255, 255, 255
colorDecrement = 255, 255, 255
planning = True
screen = pygame.display.set_mode(size)
minPointDistance = 2  # has to be lower than stepDistance!! TODO:rework this
alignAxis = False
fixedStep = False # currently only available during alignAxis Mode.
stepDistance = 5
nextPoint = np.array(pygame.mouse.get_pos())
fractalDepth = 5

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS:
                fractalDepth += 1

            if event.key == pygame.K_MINUS:
                fractalDepth -= 1

        if planning:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    alignAxis = True

                if event.key == pygame.K_f:
                    fixedStep = not fixedStep

                if event.key == pygame.K_SPACE:
                    planning = False

                if event.key == pygame.K_PLUS:
                    fractalDepth += 1

                if event.key == pygame.K_MINUS:
                    fractalDepth -= 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    alignAxis = False

            # LEFT MOUSE BUTTON EVENT
            if pygame.mouse.get_pressed()[0] == 1:
                if len(points) != 0:
                    # minimum distance to make hold and drag possible without too many points.
                    if np.linalg.norm(points[-1] - nextPoint) > minPointDistance:
                        points.append(nextPoint)

                # No points so just add the first one
                else:
                    points.append(np.array(pygame.mouse.get_pos()))

            # RIGHT MOUSE BUTTON EVENT
            if pygame.mouse.get_pressed() == (0, 0, 1):
                points = points[:-1]  # set the list to the same list without the last element. Better than pop as it
                # throws no error

        # calculate the next position
        nextPoint = np.array(pygame.mouse.get_pos())
        if alignAxis and len(points) > 0:
            if abs(nextPoint[0]-points[-1][0]) > abs(nextPoint[1]-points[-1][1]):
                nextPoint[1] = points[-1][1]  # set to the axis of the last point
                if fixedStep:
                    # multiply the stepDistance by the direction of the vectors
                    nextPoint[0] = points[-1][0]+stepDistance*(nextPoint[0]-points[-1][0])//abs(nextPoint[0]-points[-1][0])
            else:
                nextPoint[0] = points[-1][0]  # set to the axis of the last point
                if fixedStep:
                    nextPoint[1] = points[-1][1]+stepDistance*(nextPoint[1]-points[-1][1])//abs(nextPoint[1]-points[-1][1])



    if len(points) > 0:
        if planning:
            screen.fill(black)
            lp = nextPoint  # Points are drawn in revers starting from the "next" position/ the cursor
            for x in points[::-1]:
                pygame.draw.line(screen, (255, 255, 255), lp, x, 1)
                lp = x
        else: # fractal drawing time!
            if pointTranslations is None:
                screen.fill(black)
                pointTranslations = []
                for x in range(len(points) - 1):
                    pointTranslations.append(np.array(points[x + 1] - points[x]))
                lp = (height / 2, width / 2)
            for x in range(len(pointTranslations)):
                nextPoint = lp + pointTranslations[x]
                pygame.draw.line(screen, (255, 255, 255), lp, nextPoint, 1)
                pygame.display.update() # shows every line after it has been drawn
                time.sleep(0.001)
                lp = nextPoint
            pointTranslations.extend([x.dot(rotation) for x in pointTranslations])
            #colorDecrement = [x-(256/fractalDepth) for x in colorDecrement]


    pygame.display.flip()
