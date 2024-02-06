import pygame

from Algorithm.Environment import staticEnvironment

from Helper import obstacleGenerator
from Helper.constants import MOVEMENT
from Simulator import Simulator


def main():
    obs1 = obstacleGenerator.getTestObstacles()
    sim = Simulator(staticEnvironment((200, 200), obs1), obs1, False)
    sim.initialize()
    sim.run()

main()
