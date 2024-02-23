import pygame
import sys

import Helper.settings as settings
from Algorithm.Environment import staticEnvironment

from Helper import obstacleGenerator
from Helper.constants import MOVEMENT
from Simulator import Simulator


def main():
    obs = obstacleGenerator.getTestObstacles()
    obs1 = obstacleGenerator.getTestObstacles1()
    obs2 = obstacleGenerator.getTestObstacles2()
    obs3 = obstacleGenerator.getTestObstacles3()
    obs4 = obstacleGenerator.getTestObstacles4()
    obs5 = obstacleGenerator.getTestObstacles5()
    obsTest = obstacleGenerator.getTestObstaclesTest()
    #userInputObs = obstacleGenerator.getObstaclesThroughUserInput()
    inputTxtObs = obstacleGenerator.getObstaclesThroughTxt()

    sim = Simulator(staticEnvironment((200, 200), inputTxtObs), inputTxtObs, False)   
    sim.initialize()
    sim.run()

if __name__ == '__main__':
    main()









