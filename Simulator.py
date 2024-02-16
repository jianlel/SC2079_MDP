from tkinter import messagebox

import pygame
import sys

from python_tsp.exact import solve_tsp_dynamic_programming

from Entities.Arena import Arena
from Entities.Robot import Robot
from Entities.Obstacle import Obstacle

from Algorithm.Commands import Command
from Algorithm.Environment import staticEnvironment
from Algorithm.Astar import Astar
from Algorithm.TSP import NearestNeighbour

from Helper import settings
from Helper.constants import DIRECTION

class Simulator:

    # Elements that are defined as None are to be initialized during the calling of the class
    def __init__(self, env: staticEnvironment, obstacles: list[Obstacle], shortestPath: bool):
        self.running = False
        self.commandList = []
        self.screen: pygame.surface = None
        self.clock : pygame.time = None
        self.env = env
        self.arena = None
        self.obstacles = obstacles
        self.robot: Robot = None
        self.commandCounter = 0
        self.moveCar = None
        self.timer = None
        self.text = None
        self.font = None
        self.optimalCoords = None
        self.shortestPath = shortestPath
        self.timeCounter = 0
        self.textTimer = None
        self.pause = False
        self.scanCounter = 0
        self.scanText = None
        self.scanCheck = None
        self.completed = False


    # Use this function to initialize the simulator
    def initialize(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.screen.fill(settings.BLACK)
        pygame.display.set_caption("MDP Algo")
        self.font = pygame.font.Font('Assets/font.ttf', 32)
        self.number_font = pygame.font.SysFont(None, 32)
        self.text = self.font.render("MDP Algo", True, settings.WHITE, settings.BLACK)
        self.text.get_rect().center = (600, 400)
        self.screen.blit(self.text, self.text.get_rect())

        # If the robot has not reached the obstacle yet
        if self.shortestPath == True:
            TSP = Astar(self.env, (0, 0, DIRECTION.TOP, 'P'), self.env.getTargetLocation()[0])
            TSP.computePath()
            self.optimalCoords = TSP.getPath()
            self.commandList = TSP.getCommandPath()

        # If the robot has reached the obstacle
        else:
            TSP = NearestNeighbour(self.env, (0, 0, DIRECTION.TOP, 'P'))
            TSP.computeSequence()
            self.optimalCoords = TSP.getOptimalWithCoords()
            self.commandList = TSP.convert_to_simulator_commands()
            print(self.optimalCoords)
            with open(settings.FILE_PATH, "a") as file:
                file.write("\n")
                file.write(str(self.optimalCoords) + "\n")

        pygame.display.set_caption("Starting simulator...")
        self.scanCheck = [x for x in self.env.getTargetLocation()]
        self.arena = Arena(self.obstacles, 400 + settings.GRID_OFFSET, 400 + settings.GRID_OFFSET, settings.BLOCK_SIZE)
        self.robot = Robot(self.arena.obList)
        self.arena.drawGrid(self.screen)
        self.robot.drawCar(self.screen)
        self.moveCar = pygame.USEREVENT + 0
        self.timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.moveCar, 1000)
        pygame.time.set_timer(self.timer, 1000)
        pygame.display.set_caption("Car go vroom vroom")

    def render(self):
        if len(self.commandList) > 0 and self.commandCounter <= len(self.commandList) - 1:
            self.text = self.font.render("Command: " + self.commandList[self.commandCounter], True, settings.GREEN,
                                         settings.BLUE)
            self.text.get_rect().center = (600, 400)
            self.screen.blit(self.text, self.text.get_rect())
            direction = self.font.render("Direction: " + self.optimalCoords[self.commandCounter][2].name, True,
                                         settings.GREEN, settings.BLUE)
            direction.get_rect().center = (600, 200)
            self.screen.blit(direction, (0, 30))
            self.textTimer = self.number_font.render("Time ({}secs): ".format(str(self.timeCounter)),True,settings.GREEN, settings.BLUE)
            #self.textTimer = self.font.render("Time ( secs): " + str(self.timeCounter), True, settings.GREEN,
            #                                  settings.BLUE)
            self.textTimer.get_rect().center = (600, 600)
            self.screen.blit(self.textTimer, (0, 60))
        self.scanText = self.font.render("Image Scanned: " + str(self.scanCounter), True, settings.GREEN, settings.BLUE)
        self.scanText.get_rect().center = (600, 600)
        self.screen.blit(self.scanText, (500, 100))

    def events(self):
        # pop up window after the simulator is done
        if self.scanCounter == 5 and not self.completed:
            messagebox.showinfo('ALL Images Found', 'OK')
            pygame.display.set_caption("Pathing Done")
            self.completed = True

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                elif event.key == pygame.K_LEFT and self.pause and self.commandCounter > 0:
                    self.commandCounter -= 1
                    self.timeCounter -= 1
                elif event.key == pygame.K_RIGHT and self.pause and self.commandCounter <= len(self.commandList) - 1:
                    self.commandCounter += 1
                    self.timeCounter += 1
            if event.type == self.moveCar:
                if self.commandCounter <= len(self.commandList) - 1:
                    if self.robot.command is None:
                        self.robot.setCurrentCommand(self.optimalCoords[self.commandCounter])
                    elif self.robot.command.tick == 0 and not self.pause:
                        self.commandCounter += 1
                        if self.commandCounter <= len(self.commandList) - 1:
                            self.robot.setCurrentCommand(self.optimalCoords[self.commandCounter])
                if self.commandCounter <= len(self.commandList) - 1:
                    self.robot.moveToDo(self.optimalCoords[self.commandCounter], self.screen)
                if self.robot.command is not None and self.robot.command.tick > 0:
                    self.robot.command.yoloTick()
                # check if already scan image:
                pos = (self.robot.pos[0], self.robot.pos[1], self.robot.orientation)
                if pos in self.scanCheck:
                    self.scanCounter += 1
                    self.scanCheck.remove(pos)
                self.arena.updateGrid(self.robot, self.screen)
                # self.arena.drawStuff(self.env.getTargetLocation(), self.screen, settings.GREEN)
            if event.type == self.timer and not self.pause:
                self.timeCounter += 1

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.events()
            self.render()
            self.clock.tick(30)
            # print(self.timeCounter)


"""
pygame.init()

SCREEN = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("MDP Algo")
font = pygame.font.Font('Assets/font.ttf', 32)
text = font.render("MDP Algo", False, settings.WHITE, settings.BLACK)
SCREEN.blit(text, (10, 10))


obstacle_list = getTestObstacles()

arena = Arena(obstacle_list, 400 + settings.GRID_OFFSET, 400 + settings.GRID_OFFSET, settings.BLOCK_SIZE)
robot = Robot(arena.obList)
command = Command(robot.pos)

while True:
    CLOCK.tick(settings.FRAMES)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    SCREEN.fill(settings.BLACK)
    SCREEN.blit(text, (10, 10))

    
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        current_car_pos = (current_car_pos[0], current_car_pos[1] - 20)
    elif key[pygame.K_DOWN]:
        current_car_pos = (current_car_pos[0], current_car_pos[1] + 20)
    elif key[pygame.K_LEFT]:
        current_car_pos = (current_car_pos[0] - 20, current_car_pos[1])
    elif key[pygame.K_RIGHT]:
        current_car_pos = (current_car_pos[0] + 20, current_car_pos[1])
 
    robot.moveToDo(command.moveStraight(), SCREEN)

    arena.drawGrid(SCREEN)
    robot.drawCar(SCREEN)

    pygame.display.update()
"""



