import pygame
import Helper.settings as settings
from Entities.Rectangle import Rectangle
from Entities.Obstacle import Obstacle

"""
Represents the navigational area (default: 20x20 grid of 10x10cm grid cells)
"""
class Arena:
    def __init__(self,obstacles, width, height, blockSize):
        self.obstacles = obstacles
        self.height = height
        self.width = width
        self.blockSize = blockSize
        self.obList = []


    def drawGrid(self, SCREEN):
        # Draw the grid
        for x in range(0 + settings.GRID_OFFSET,self.width, self.blockSize):
            for y in range(0 + settings.GRID_OFFSET, self.height, self.blockSize):
                grid = pygame.Rect(x,y, self.blockSize, self.blockSize)
                pygame.draw.rect(SCREEN, settings.WHITE, grid, 1)
        #Draw the obstacles
        for obstacle in self.obstacles:
            ob = pygame.Rect(obstacle.gridPosition, obstacle.dimension)
            ob.bottomleft = obstacle.gridPosition
            self.obList.append(ob)
            pygame.draw.rect(SCREEN, settings.GREEN, ob)

            #Draw the borders surrounding obstacles
            self.drawBorder(obstacle, SCREEN, settings.RED, ob)
            self.drawInvisibleObstacle(obstacle,SCREEN, (0, 100, 255))
        #Draw the start zone
        start = pygame.Rect(0 + settings.GRID_OFFSET, 0 + settings.GRID_Y_OFFSET + 20, self.blockSize * 4, self.blockSize * 4)
        pygame.draw.rect(SCREEN, settings.YELLOW, start)

        #Draw the borders surrounding the arena


    def drawBorder(self, obstacle,  SCREEN, COLOUR, ob):
        if obstacle.imageOrientation == "N":
            pygame.draw.line(SCREEN, COLOUR, ob.topleft, ob.topright, 2)
        elif obstacle.imageOrientation == "E":
            pygame.draw.line(SCREEN, COLOUR, ob.topright, ob.bottomright, 2)
        elif obstacle.imageOrientation == "S":
            pygame.draw.line(SCREEN, COLOUR, ob.bottomleft, ob.bottomright, 2)
        elif obstacle.imageOrientation == "W":
            pygame.draw.line(SCREEN, COLOUR, ob.topleft, ob.bottomleft, 2)



    def drawInvisibleObstacle(self, obstacle: Obstacle, SCREEN, COLOUR):
        newRect = Rectangle(obstacle.pos, 'O')
        dim = (int(newRect.length/10)*settings.BLOCK_SIZE, int(newRect.length/10)*settings.BLOCK_SIZE)
        rectOb = pygame.Rect(obstacle.pos, dim)
        rectOb.topleft = self.posConverter((newRect.x, newRect.y))
        pygame.draw.line(SCREEN, COLOUR, rectOb.topleft, rectOb.topright, 2)
        pygame.draw.line(SCREEN, COLOUR, rectOb.topright, rectOb.bottomright, 2)
        pygame.draw.line(SCREEN, COLOUR, rectOb.bottomleft, rectOb.bottomright, 2)
        pygame.draw.line(SCREEN, COLOUR, rectOb.topleft, rectOb.bottomleft, 2)

    def drawInvisibleBorder(self, SCREEN):
        edge = pygame.Rect(0 + settings.GRID_OFFSET - 40, 0 + settings.GRID_Y_OFFSET - 340, self.blockSize * 24, self.blockSize * 24)
        pygame.draw.rect(SCREEN, settings.PURPLE, edge, 1)
        self.rect = edge

    def drawStuff(self, stuff: list[tuple], SCREEN, COLOUR):
        for s in stuff:
            pygame.draw.circle(SCREEN, COLOUR, self.posConverter(s), 20)


    def drawStuff(self, stuff: list[tuple], SCREEN, COLOUR):
        for s in stuff:
            #print(s)
            pygame.draw.circle(SCREEN, COLOUR, self.posConverterStuff(s), 10)

    def updateGrid(self, robot, SCREEN):
        SCREEN.fill((0,0,0))
        self.drawGrid(SCREEN)
        robot.drawCar(SCREEN)
        self.drawInvisibleBorder(SCREEN)
        self.robotCollisionRect(robot,SCREEN, (0, 100, 255))


    def robotCollisionRect(self, robot, screen, colour):
        newRect = Rectangle((robot.x,robot.y), 'R')
        dim = ((newRect.length // 10) * settings.BLOCK_SIZE, (newRect.length // 10) * settings.BLOCK_SIZE)
        rectOb = pygame.Rect((newRect.x, newRect.y), dim)
        rectOb.topleft = self.posConverter((newRect.x, newRect.y))
        pygame.draw.line(screen, colour, rectOb.topleft, rectOb.topright, 2)
        pygame.draw.line(screen, colour, rectOb.topright, rectOb.bottomright, 2)
        pygame.draw.line(screen, colour, rectOb.bottomleft, rectOb.bottomright, 2)
        pygame.draw.line(screen, colour, rectOb.topleft, rectOb.bottomleft, 2)

    @staticmethod
    def posConverter(pos):
        return (pos[0] // settings.GRID_SCALE_FACTOR) * settings.BLOCK_SIZE + settings.GRID_OFFSET, \
                            (settings.GRID_Y_OFFSET - (pos[1] // settings.GRID_SCALE_FACTOR) * settings.BLOCK_SIZE) + \
                            settings.GRID_OFFSET
    
    @staticmethod
    def posConverterStuff(pos):
        return (pos[0] // settings.GRID_SCALE_FACTOR) * settings.BLOCK_SIZE + settings.GRID_OFFSET + settings.STUFF_X_OFFSET, \
                            (settings.GRID_Y_OFFSET - (pos[1] // settings.GRID_SCALE_FACTOR) * settings.BLOCK_SIZE) + \
                            settings.GRID_OFFSET - settings.STUFF_Y_OFFSET

    @staticmethod
    def drawPath(path: list):
        pass

