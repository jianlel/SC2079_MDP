
from Algorithm.Environment import staticEnvironment
import itertools
import numpy as np
import Helper.settings as settings
from collections import deque
from Algorithm.Astar import Astar
from Helper.constants import DIRECTION

class NearestNeighbour:
    def __init__(self, env: staticEnvironment, start):
        self.env = env
        self.targetLocations = self.env.getTargetLocation()
        self.sequence = tuple()
        self.commands = deque()
        self.start = start
        self.optimalPathWithCoords = None
        self.commandList = None
        self.simulatorCommandList = []

    def computeSequence(self):
        """
        returns the sequence of vertices to visit with minimum cost
        :return:
        sequence of verticles with their pos
        """
        permutations = list(itertools.permutations(self.targetLocations))
        costList = []
        lowestDistance = 999999
        for perm in permutations:
            distance = 0
            for i in range(len(perm)-1):
                distance += self.euclideanDistance(perm[i], perm[i+1])
            if distance <= lowestDistance:
                lowestDistance = distance
                stmPath, path = self.findPath(list(perm))
                cost = self.calculateCost(stmPath)

                costList.append((stmPath, path, cost))
            else:
                continue
        optimalPath = min(costList, key=lambda tup: tup[2])
        #print("Stm path", optimalPath[0])
        #print("coords", optimalPath[1])
        dist = self.totalDistance(optimalPath[0])
        stmPath = self.STMPath(optimalPath[0])
        limitedSTMPath = self.STMLimitations(stmPath)
        #bufferedPath = self.addBuffer(limitedSTMPath)
        with open(settings.OUTPUT_FILE_PATH, "w") as file:
            file.write(str(limitedSTMPath) + "\n\n")
            file.write("Total distance travelled is: " + str(dist) + "\n")
        simCoords = optimalPath[1].copy()
        coords = self.convert_to_coords(optimalPath[1])
        self.commandList = list(optimalPath[0]), coords
        #print(("rpi path", self.commandList))
        self.optimalPathWithCoords = simCoords

    def euclideanDistance(self, start, end):

        return ((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5
    
    def STMPath(self, optimalPath):
        result = []

        for count in optimalPath:
            processed_string = ''
            for char in count[1].split(','):
                if char in {'s', 'v', 'u', 'b', 'd', 'w'}:
                    processed_string += char
            result.append(processed_string)

        # For inside lab
        path = self.convertToSTMCommandsInsideLab(result)
        # For outside lab
        #path = self.convertToSTMCommandsOutsideLab(result)

        return path
    
    def convertToSTMCommandsInsideLab(self, data):
        final_result = []

        for path_string in data:
            path = []
            current_command = None
            current_distance = 0

            for char in path_string:
                if char in settings.COMMANDS:
                    if current_command == settings.COMMANDS[char]:
                        current_distance += 5
                    else:
                        if current_command:
                            s = current_command + str(current_distance).zfill(3)
                            path.append(s)
                        current_command = settings.COMMANDS[char]
                        current_distance = 5
            
            if current_command:
                s = current_command + str(current_distance).zfill(3)
                path.append(s)
            
            final_result.append(path)

        for commands in final_result:
            for i in range(len(commands)):
                if commands[i][0] == 'C':
                    commands[i] = 'FR000'
                elif commands[i][0] == 'A':
                    commands[i] = 'FL000'
                elif commands[i][:2] == 'BL':
                    commands[i] = 'BL000'
                elif commands[i][:2] == 'BR':
                    commands[i] = 'BR000'

        return final_result
    
    def convertToSTMCommandsOutsideLab(self, data):
        final_result = []

        for path_string in data:
            path = []
            current_command = None
            current_distance = 0

            for char in path_string:
                if char in settings.COMMANDS:
                    if current_command == settings.COMMANDS[char]:
                        current_distance += 10
                    else:
                        if current_command:
                            s = current_command + str(current_distance).zfill(3)
                            path.append(s)
                        current_command = settings.COMMANDS[char]
                        current_distance = 10
            
            if current_command:
                s = current_command + str(current_distance).zfill(3)
                path.append(s)
            
            final_result.append(path)

        for commands in final_result:
            for i in range(len(commands)):
                if commands[i][0] == 'C':
                    #commands[i] = 'C0890'
                    commands[i] = 'FR200'
                elif commands[i][0] == 'A':
                    #commands[i] = 'A0890
                    commands[i] = 'FL200'
                elif commands[i][:2] == 'BL':
                    commands[i] = 'BL200'
                elif commands[i][:2] == 'BR':
                    commands[i] = 'BR200'

        return final_result

    def STMLimitations(self, data):
        result = []

        for commands in data:
            inner_result = []
            for string in commands:
                if string[0:2] != 'FW' and string[0:2] != 'BW':
                    inner_result.append(string)
                elif string[0:2] == 'FW':
                    distance = int(string[2:5])
                    if distance > 90:
                        inner_result.append('FW900')
                        distance -= 90
                        inner_result.append('FW' + str(distance) + '0')
                    else:
                        inner_result.append('FW' + str(distance) + '0')
                elif string[0:2] == 'BW':
                    distance = int(string[2:5])
                    if distance > 90:
                        inner_result.append('BW900')
                        distance -= 90
                        inner_result.append('BW' + str(distance) + '0')
                    else:
                        inner_result.append('BW' + str(distance) + '0')
                
            result.append(inner_result)

        return result
    
    """
    def addBuffer(self, data):
        result = []

        for commands in data:
            inner_result = []
            for string in commands:
                if string[0:2] == 'BR' or string[0:2] == 'BL':
                    inner_result.append(string)
                    inner_result.append('FW000')
                else:
                    inner_result.append(string)

            result.append(inner_result)
        
        return result
    """
    
    def totalDistance(self, optimalPath):
        distances = {
            's': 5,
            'b': 5,
            'd': 5 * np.pi,
            'u': 5 * np.pi,
            'w': 5 * np.pi,
            'v': 5 * np.pi
        }

        total_distance = 0
        for count in optimalPath:
            for char in count[1].split(','):
                total_distance += distances[char]
        return total_distance

    def findPath(self, targetLocations: list):
        """

        :param targetLocations: list[tuple]
        :return: stmPath and path
        """
        path = []
        stmPath = []
        start = self.start
        counter = 0
        for ob in targetLocations:
            aStar = Astar(self.env, start, ob)
            next = aStar.computePath()
            if next == None:
                print("no path found!!")
                break
            newPath = aStar.getPath()
            path.extend(newPath)
            cPath = aStar.getSTMCommands()
            stmPath.append((self.env.obID[self.env.getTargetLocation().index(ob)], cPath))
            start = next
            counter += 1
            """
            """
        if counter != len(targetLocations):
            print("Path is incomplete!!!")
            # path = []
            # stmPath = []
        return stmPath, path

    def calculateCost(self, path: list[tuple]):
        cost = 0
        diff = len(self.env.obID) - len(path)
        cost += (999 * diff)
        for tup in path:
            for command in tup[1]:
                if command == 's' or command == 'b':
                    cost += 1
                elif command == 'd' or command == 'u':
                    cost += 8
                elif command == 'OL' or command == 'OR':
                    cost += 10
                elif command == 'v' or command == 'w':
                    cost += 10
                elif command == '3P':
                    cost += 10
        return cost

    def convertToCommands(self, path):
        commandList = []
        prev = path[0][1]
        counter = 0
        for x in path:
            if x[1] == prev:
                counter += 1
            else:
                string = str(counter) + prev
                commandList.append(string)
                counter = 1
            prev = x[1]

        return commandList

    def getSTMCommands(self, path):
        commands = []
        for x in path:
            if x[3] is not "P":
                commands.extend(x[3])
        return commands

    def getOptimalWithCoords(self):
        return self.optimalPathWithCoords

    def getCommandList(self):
        return self.commandList

    def convert_to_coords(self, path):
        coords_path = []

        for x in path:
            coords_path.append(self.convertTuple( ("ROBOT",str(x[0]//10), str(x[1]//10), self.convert_direction(x[2].name) )) )

        return coords_path

    def convert_direction(self,f):
        if f == "TOP":
            return "N"
        elif f == "BOTTOM":
            return "S"
        elif f == "RIGHT":
            return "E"
        else:
            return "W"

    def convertTuple(self, tup):
        str = ', '.join(tup)
        return str

    def convert_to_simulator_commands(self):
        commands = []
        for x in self.commandList[0]:
            commands.extend(x[1].split(','))
        return commands


