import pygame
import sys

import Helper.settings as settings
from Algorithm.Environment import staticEnvironment

from Helper import obstacleGenerator
from Helper.constants import MOVEMENT
from Simulator import Simulator


def main():
    obs1 = obstacleGenerator.getTestObstacles()
    obs2 = obstacleGenerator.getTestObstacles1()
    obs3 = obstacleGenerator.getTestObstacles2()
    obs4 = obstacleGenerator.getTestObstacles3()
    obs5 = obstacleGenerator.getTestObstacles4()

    sim = Simulator(staticEnvironment((200, 200), obs1), obs1, False)   
    sim.initialize()
    sim.run()

main()









