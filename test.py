import json
from Entities.Obstacle import Obstacle
import Helper.settings as settings
import Simulator
import pygame
import sys
import os

import Helper.settings as settings
from Algorithm.Environment import staticEnvironment

from Helper import obstacleGenerator
from Helper.constants import MOVEMENT
from Simulator import Simulator

x = {
  "cat": "obstacles",
  "value": {
    "obstacles": [
      {
        "x": 1,
        "y": 2,
        "d": 0,
        "id": 1
      },
      {
        "x": 4,
        "y": 3,
        "d": 2,
        "id": 2
      }
    ],
    "mode": "0"
  }
}

obstacles = x["value"]["obstacles"]

def getObstacles(data):
    obstacles = data["value"]["obstacles"]
    result = []

    for obstacle in obstacles:
        x = obstacle["x"]
        y = obstacle["y"]
        id = obstacle["id"]
        dirCode = obstacle["d"]
        dir = settings.DIR[int(dirCode)]
        obs = Obstacle((int(x), int(y)), dir, (settings.BLOCK_SIZE, settings.BLOCK_SIZE), id)

        result.append(obs)

    return result

obsList = []
#getObstacles(x)
#print(obsList)
#print(input)

input1 = {'cat': 'obstacles', 'value': {'obstacles': [{'x': 2, 'y': 12, 'd': 0, 'id': 2}, {'x': 18, 'y': 2, 'd': 0, 'id': 1}, {'x': 8, 'y': 0, 'd': 0, 'id': 3}, {'x': 2, 'y': 11, 'd': 4, 'id': 4}, {'x': 6, 'y': 10, 'd': 2, 'id': 5}, {'x': 15, 'y': 9, 'd': 4, 'id': 6}, {'x': 19, 'y': 15, 'd': 6, 'id': 7}, {'x': 11, 'y': 18, 'd': 4, 'id': 8}], 'mode': '0'}}

def getObstaclesThroughTxt():
    test = []
    file = open(settings.INPUT_FILE_PATH, 'r')
    id_counter = 1
    
    for line in file:
        components = line.strip().split(",")
        if len(components) == 3:
            x = components[0]
            y = components[1]
            dir = components[2].strip().upper()
            id = id_counter

            obs = Obstacle((int(x), int(y)), dir, (settings.BLOCK_SIZE, settings.BLOCK_SIZE), id)
            test.append(obs)
            id_counter += 1

    return test

def getObstaclesThroughJson(obstacles_data):
    test = []
    
    obstacles = obstacles_data["value"]["obstacles"]

    for obstacle in obstacles:
        x = obstacle["x"]
        y = obstacle["y"]
        id = obstacle["id"]
        dir_code = obstacle["d"]
        dir = settings.DIR[int(dir_code)]

        obs = Obstacle((int(x * 10), int(y * 10)), dir, (settings.BLOCK_SIZE, settings.BLOCK_SIZE), id)
        test.append(obs)
        
    return test

#Obs1 = getObstaclesThroughJson(input1)
#Obs2 = getObstaclesThroughTxt()

"""
for obs1, obs2 in zip(Obs1, Obs2):
      if obs1.ObId != obs2.ObId \
                or obs1.pos != obs2.pos \
                or obs1.imageOrientation != obs2.imageOrientation \
                or obs1.dimension != obs2.dimension \
                or obs1.gridPosition != obs2.gridPosition:
          print("different")
      else:
          print("same")
"""


#sim = Simulator(staticEnvironment((400, 400), Obs1), Obs1, False)   
#sim.initialize_without_simulator()

#sim1 = Simulator(staticEnvironment((400, 400), Obs2), Obs2, False)
#sim1.initialize_without_simulator() 


x_coord = 0
y_coord = 0
direction = 0
counter = 0

input = [['FW300', 'FR200', 'FW700', 'FL200'], ['FW100',  'BL200', 'FW000', 'FW600'], ['BW100', 'FR200', 'FW200'], ['FW100', 'BL200', 'FW000', 'FW300', 'FL200', 'FR200', 'FW400'], ['BW100', 'FR200', 'FW300', 'BL200', 'FW000', 'FW200'], ['BW100', 'FL200', 'FW300', 'FL200'], ['BW100', 'FR200', 'FW200', 'FR200', 'FW200'], ['BW200', 'FR200', 'FW300', 'FL200', 'FW600', 'FL200', 'FW300', 'FL200', 'BW100']]

for list in input:
    for commands in list:
        if commands[:2] == "FR":
          # Facing north
          if direction == 0:
            x_coord = x_coord + 2
            y_coord = y_coord + 2
          # Facing East
          elif direction == 2:
            x_coord = x_coord + 2
            y_coord = y_coord - 2
          # Facing South
          elif direction == 4:
            x_coord = x_coord - 2
            y_coord = y_coord - 2
          # Facing West
          else:
            x_coord = x_coord - 2
            y_coord = y_coord + 2
          direction = (direction + 2) % 8
          
        # Left turn
        elif commands[:2] == "FL": 
          # Facing north
          if direction == 0:
            x_coord = x_coord - 2
            y_coord = y_coord + 2
          # Facing East
          elif direction == 2:
            x_coord = x_coord + 2
            y_coord = y_coord + 2
          # Facing South
          elif direction == 4:
            x_coord = x_coord + 2
            y_coord = y_coord - 2
          # Facing West
          else:
            x_coord = x_coord - 2
            y_coord = y_coord - 2
          direction = (direction - 2) % 8
          if direction == -2:
            direction = 6

        # Back Right turn
        elif commands[:2] == "BR":
          # Facing north
          if direction == 0:
            x_coord = x_coord + 2
            y_coord = y_coord - 2
          # Facing East
          elif direction == 2:
            x_coord = x_coord - 2
            y_coord = y_coord - 2
          # Facing South
          elif direction == 4:
            x_coord = x_coord - 2
            y_coord = y_coord + 2
          # Facing West
          else:
            x_coord = x_coord + 2
            y_coord = y_coord + 2
          direction = (direction - 2) % 8
          if direction == -2:
            direction = 6
            

        elif commands[:2] == "BL":
          # Facing north
          if direction == 0:
            x_coord = x_coord - 2
            y_coord = y_coord - 2
          # Facing east
          elif direction == 2:
            x_coord = x_coord - 2
            y_coord = y_coord + 2
          # Facing south
          elif direction == 4:
            x_coord = x_coord + 2
            y_coord = y_coord + 2
          # Facing west
          else:
            x_coord = x_coord + 2
            y_coord = y_coord - 2
          direction = (direction + 2) % 8

        elif commands[:2] == "FW":
          distance = int(commands[2])
          # Facing north
          if direction == 0:
            y_coord = y_coord + distance
          # Facing east
          elif direction == 2:
            x_coord = x_coord + distance
          # Facing south
          elif direction == 4:
            y_coord = y_coord - distance
          # Facing west
          else:
            x_coord = x_coord - distance

        elif commands[:2] == "BW":
          distance = int(commands[2])
          # Facing north
          if direction == 0:
            y_coord = y_coord - distance
          # Facing east
          elif direction == 2:
            x_coord = x_coord - distance
          # Facing south
          elif direction == 4:
            y_coord = y_coord + distance
          # Facing west
          else:
            x_coord = x_coord + distance

        # Replace this with the android sending
        #counter += 1
        print("current x_coord = " + str(x_coord))
        print("current y_coord = " + str(y_coord))
        print("current direction = " + str(direction))
        print()

#print(counter)