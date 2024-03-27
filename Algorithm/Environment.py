import pygame
import numpy as np
import shapely as sp

from Entities.Rectangle import Rectangle
from Entities.Obstacle import Obstacle
from Entities.RectRobot import RectRobot
from Helper.constants import DIRECTION
from Helper.helperFunctions import radiansToDegrees
from Helper.helperFunctions import basic_angle


class staticEnvironment:

    def __init__(self, dimensions, obstacles: list[Obstacle]):
        self.dimensions = dimensions
        self.obstacles = obstacles
        self.obID = []
        self.targetLocations = self.generateTargetLocations()

    # Function to check if robot is can occupy this location
    # Takes in (x, y) coordinates and time
    # Returns boolean value True/False
    def isWalkable(self, x, y, time=0):
        if x < 0 or x > (self.dimensions[0] - 30) or y < 0 or (y > self.dimensions[1] - 30):
            return False
        robotRect = Rectangle((x, y), 'R')
        for obstacle in self.obstacles:
            pos = Rectangle(obstacle.pos, 'O')
            if robotRect.isCollided(pos):
                return False
            
        return True

    # Function to check if robot can turn at current position
    def turnCheck(self, pos):
        for obs in self.obstacles:
            ob_pos = Rectangle(obs.pos, 'O')
            print(pos[2])
            if not self.direction_turn_check(pos[2], pos, (ob_pos.x, ob_pos.y)):
                return False
        return True

    # Helper function for the above
    def direction_turn_check(self, dir, pos1, pos2):
        if dir == DIRECTION.TOP:
            if pos1[1] - pos2[1] < 10:
                return False
        elif dir == DIRECTION.RIGHT:
            if pos1[0] - pos2[0] < 40:
                return False
        elif dir == DIRECTION.LEFT:
            if pos2[0] - pos1[0] < 40:
                return False
        else:
            if pos2[1] - pos1[1] < 10:
                return False
        return True

    # Function to get the next position in continuous step
    # Takes in coordinate (pos), type of turn (type), steering angle (delta)
    def nextPos(self, pos, type, delta):
        """
        Get the next position in continuous step
        :param pos:
        :param v:
        :param steeringAngle:
        :return:
        """
        direction = pos[2]
        if type == "s":
            new_X = pos[0] + delta * np.cos(direction)
            new_Y = pos[1] + delta * np.sin(direction)
            new_orientation = direction
        elif type == "d":
            new_X = pos[0] + delta * np.cos(direction)
            new_Y = pos[1] + delta * np.sin(direction)
            new_orientation = basic_angle(direction - delta / 20)
        elif type == "u":
            new_X = pos[0] + delta * np.cos(direction)
            new_Y = pos[1] + delta * np.sin(direction)
            new_orientation = basic_angle(direction + delta / 20)
        elif type == "b":
            new_X = pos[0] - delta * np.cos(direction)
            new_Y = pos[1] - delta * np.sin(direction)
            new_orientation = direction
        elif type == "w":
            new_X = pos[0] - delta * np.cos(direction)
            new_Y = pos[1] - delta * np.sin(direction)
            new_orientation = basic_angle(direction + delta / 20)
        elif type == "v":
            new_X = pos[0] - delta * np.cos(direction)
            new_Y = pos[1] - delta * np.sin(direction)
            new_orientation = basic_angle(direction - delta / 20)
        return new_X, new_Y, new_orientation

    def randomFreeSpace(self):
        x = np.random.rand() * self.dimensions[0]
        y = np.random.rand() * self.dimensions[1]
        while not self.isWalkable(x, y):
            x = np.random.rand() * self.dimensions[0]
            y = np.random.rand() * self.dimensions[1]
        return x, y, np.random.rand() * np.pi * 2

    def getTargetLocation(self):

        """
        get all the configurations that the robot needs to visit
        :param obstacles: List[Obstacles]
        :return:
            list of configurations in the form (x,y,direction in char)
        """
        return self.targetLocations

    def generateTargetLocations(self):
        """
        generate the required locations
        :return:
        """

        targetLocations = []
        # possible_pos = {"E": [(40, -10), (40, 0), (40, -20), (30, -10), (30, 0), (30, -20)],
        #                 "N": [(-10, 40), (0, 40), (-20, 40), (-10, 30), (0, 30), (-20, 30)],
        #                 "W": [(-40, -10), (-40, 0), (-40, -20), (-30, -10), (-30, 0), (-30, -20)],
        #                 "S": [(-10, -40), (-20, -40), (0, -40), (-10, -30), (-20, -30), (0, -30)]}
        possible_pos =   {"E": [(40, -10), (40, 0), (40, -20)],
                        "N": [(-10, 40), (0, 40), (-20, 40), (-10, 30), (0, 30), (-20, 30)],
                        "W": [(-40, -10), (-40, 0), (-40, -20)],
                        "S": [(-10, -40), (-20, -40), (0, -40)]}

        for ob in self.obstacles:
            valid_pos = None
            if ob.imageOrientation == "E":
                for x in possible_pos["E"]:
                    if self.isWalkable(ob.pos[0] + x[0], ob.pos[1] + x[1]):
                        valid_pos = ob.pos[0] + x[0] - 10, ob.pos[1] + x[1], DIRECTION.LEFT
                        break
            elif ob.imageOrientation == "N":
                for x in possible_pos["N"]:
                    if self.isWalkable(ob.pos[0] + x[0], ob.pos[1] + x[1]):
                        valid_pos = ob.pos[0] + x[0], ob.pos[1] + x[1] - 10, DIRECTION.BOTTOM
                        break
            elif ob.imageOrientation == "W":
                for x in possible_pos["W"]:
                    if self.isWalkable(ob.pos[0] + x[0], ob.pos[1] + x[1]):
                        valid_pos = ob.pos[0] + x[0] - 10, ob.pos[1] + x[1], DIRECTION.RIGHT
                        break
            else:
                for x in possible_pos["S"]:
                    if self.isWalkable(ob.pos[0] + x[0], ob.pos[1] + x[1]):
                        valid_pos = ob.pos[0] + x[0], ob.pos[1] + x[1] - 10, DIRECTION.TOP
                        break
            if valid_pos:
                targetLocations.append(valid_pos)
                self.obID.append(ob.ObId)
            else:
                pass
            
            is_found = valid_pos is not None
            print(f'for {ob.ObId} found= {is_found}, loc = {valid_pos} ')
        
        print("test")

        return targetLocations

    def generateTargetLocationInRads(self):
        """
        same stuff as the generateTargetLocation but in rads
        :return:
        """

        targetLocations = []
        for ob in self.obstacles:
            if ob.imageOrientation == "right":
                targetLocations.append((ob.pos[0] + 40, ob.pos[1] - 5, DIRECTION.LEFT.value))
            elif ob.imageOrientation == "top":

                targetLocations.append((ob.pos[0] - 5, ob.pos[1] + 40, DIRECTION.BOTTOM.value))
            elif ob.imageOrientation == "left":
                targetLocations.append((ob.pos[0] - 40, ob.pos[1] - 5, DIRECTION.RIGHT.value))
            else:
                targetLocations.append((ob.pos[0] + 5, ob.pos[1] - 40, DIRECTION.TOP.value))
        return targetLocations
