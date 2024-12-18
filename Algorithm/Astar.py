import Helper.constants as constants

from Algorithm.Commands import Command
from Algorithm.Environment import staticEnvironment
from Algorithm.Dubins import dist
from python_tsp.exact import solve_tsp_dynamic_programming
from queue import PriorityQueue

class Astar:
    def __init__(self, env: staticEnvironment, start, end):
        """
        :param env: Static Environment
        :param start: tuple (x,y,pos) in grid format
        :param end: tuple (x,y,pos) in grid format
        """
        self.env = env
        self.start = start
        self.end = end
        self.path = []

    def getNeighbours(self, pos):
        """
        Get next position relative to pos

        a fix distance of 10 when travelling straight

        robot will always make a 90 degrees turn
        :param pos: tuple (x,y,direction in rads)
        :return: list[nodes]
        """
        neighbours = []
        command = Command(pos)
        commandList = command.getCommands()
        turnPenalty = constants.COST.TURN_COST
        timeCost = constants.COST.MOVE_COST

        for index, c in enumerate(commandList):

            if self.env.isWalkable(c[0], c[1], 0):
                if index == constants.MOVEMENT.RIGHT or index == constants.MOVEMENT.LEFT or \
                        index == constants.MOVEMENT.REVLEFT or index == constants.MOVEMENT.REVRIGHT:
                    neighbours.append((c, turnPenalty))
                elif index == constants.MOVEMENT.REVERSE:
                    neighbours.append((c, timeCost+15))
                elif index == constants.MOVEMENT.TURN_O_LEFT or index == constants.MOVEMENT.TURN_O_RIGHT:
                    if self.onTheSpotCheck(self.env, (c[0], c[1]), c[2]):
                        neighbours.append((c, turnPenalty * 3))
                else:
                    neighbours.append((c, timeCost))
        return neighbours


    def onTheSpotCheck(self,env: staticEnvironment, pos, direction):
        """
        additional check for movment that requires reversing/turning
        :param env: StaticEnvironment
        :param pos: tuple
        :param direction: Enum
        :return: bool
        true if walkable
        """
        if direction == constants.DIRECTION.TOP:
            return env.isWalkable(pos[0], pos[1]-25, 0)
        elif direction == constants.DIRECTION.RIGHT:
            return env.isWalkable(pos[0]-25, pos[1], 0)
        elif direction == constants.DIRECTION.LEFT:
            return env.isWalkable(pos[0]+25, pos[1], 0)
        else:
            return env.isWalkable(pos[0], pos[1]-25,0)

    def heuristic(self, pos, end):
        """

        :param pos: tuple
        :param end: tuple
        :return:
        distance between 2 points
        """
        return dist(pos, end)


    def computePath(self):
        """
        YOLO A star attempt
        :return:

        """
        frontier = PriorityQueue()
        backtrack = dict()
        cost = dict()
        goalNode = self.end
        startNode = self.start

        offset = 0 # dk for what
        frontier.put((0, offset, startNode))
        cost[startNode] = 0

        backtrack[startNode] = None

        while not frontier.empty():

            priority, _, currentNode = frontier.get()

            if currentNode[:3] == goalNode[:3]:
                self.extractCommands(backtrack, currentNode)
                return currentNode

            for newNode, weight in self.getNeighbours(currentNode):

                newCost = cost[currentNode] + weight

                if newNode not in backtrack or newCost < cost[newNode]:
                    cost[newNode] = newCost
                    offset += 1
                    priority = newCost + self.heuristic((newNode[0], newNode[1]), (goalNode[0], goalNode[1]))
                    backtrack[newNode] = currentNode
                    frontier.put((priority, offset, newNode))

        return None



    def extractCommands(self, backtrack, goalNode):
        """
        Extract dem commands to get to destination
        :param backtrack: dist
        :param goalNode: tuple
        :return:
        yolo
        """
        commands = []
        current = goalNode

        while current != self.start:
            commands.append(current)
            current = backtrack[current]
        #commands.append((self.start[0], self.start[1], self.start[2], 'y'))

        commands.reverse()
        self.path.extend(commands)

    def getPath(self):

        """
        get the complete tuple path
        :return: list(tuple)
        """
        return self.path
    def getCommandPath(self):
        """
        get the parth with the direction and command
        :return: list(tuple)
        """
        commandList = [x[2:4] for x in self.path]
        return commandList


    def getSTMCommands(self):
        # get minimal version required to transmit to STM
        # :return: list(string)
        path = ""
        for index, x in enumerate(self.path):
            trail = ","
            if index == len(self.path)-1:
                trail= ""
            if x[3] is not 'P':
                path = path + x[3] + trail
        return path

