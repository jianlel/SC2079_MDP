import json
import Helper.settings as settings
from Entities.Obstacle import Obstacle

"""
    Take note that range for obstacles is:
    x = [0, 190]
    y = [0, 190]
    Obstacle (x, y) MUST also be divisible by 10
"""

def getTestObstacles():
    test = [Obstacle((70, 100), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '1'),
            Obstacle((70, 140), "W", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '2'),
            Obstacle((120, 90), "E", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '3'),
            Obstacle((150, 150), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '4'),
            Obstacle((150, 40), "W", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '5')]
    return test

def getTestObstacles1():
    test = [
        Obstacle((40, 30), "N", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '1'),
        Obstacle((80, 80), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '2'),
        Obstacle((120, 100), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '3'),
        Obstacle((160, 140), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '4'),
        Obstacle((170, 30), "N", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '5')

    ]
    return test

def getTestObstacles2():
    test = [
        Obstacle((10, 150), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '1'),
        Obstacle((150, 80), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '2'),
        Obstacle((120, 100), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '3'),
        Obstacle((160, 120), "N", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '4'),
        Obstacle((30, 170), "E", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '5')

    ]
    return test



def getTestObstacles3():
    test = [
        Obstacle((10, 110), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '8'),
        Obstacle((70, 60), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '6'),
        Obstacle((120, 0), "N", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '7'),
        Obstacle((180, 30), "W", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '1'),
        Obstacle((120, 90), "E", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '4'),
        Obstacle((140, 180), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '5'),
        Obstacle((180, 130), "W", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '2'),
        Obstacle((60, 160), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '3'),
    ]
    return test

def getTestObstacles4():
    test = [
        Obstacle((20, 90), "E", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '8'),
        Obstacle((20, 170), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '6'),
        Obstacle((100, 160), "E", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '7'),
        Obstacle((160, 20), "W", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '1'),
        Obstacle((180, 190), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '4'),
        Obstacle((80, 60), "N", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '5'),
    ]
    return test

def getTestObstacles5():
    test = [
        Obstacle((10, 60), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '1'),
        Obstacle((150, 40), "N", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '2'),
        Obstacle((100, 120), "E", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '3'),
        Obstacle((90, 80), "W", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '4'),
        Obstacle((180, 190), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '5'),
        Obstacle((20, 190), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '6'),
        Obstacle((100, 180), "W", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '7'),
        Obstacle((90, 60), "S", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '8')
    ]

    return test

def getTestObstaclesTest(): 
    test = [
        Obstacle((50, 50 ), "W", (settings.BLOCK_SIZE, settings.BLOCK_SIZE), '1')
    ]

    return test


def getObstaclesThroughUserInput():
    test = []
    # Get the number of obstacles from user input
    numOfObstacles = int(input("Enter the number of obstacles: "))
    for i in range(numOfObstacles):
        print("Enter coordinates and direction for obstacle",i+1)
        x = int(input("X coordinate: "))
        y = int(input("Y coordinate: "))
        dir = input("Direction is: ")
        print("The coordinates of this obstacle is: " + x.__str__() + "," + y.__str__() + " and it is facing:" + dir.upper()) 
        uniqueID = chr(i + 1)
        obs = Obstacle((x, y), dir, (settings.BLOCK_SIZE, settings.BLOCK_SIZE), uniqueID)
        test.append(obs)

    return test


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

# Need to take in input from the android app to generate obstacles 
# Then feed back to the RPI the path generated on the log.txt
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
    