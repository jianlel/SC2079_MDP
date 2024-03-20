import pygame
import sys
import os

import Helper.settings as settings
from Algorithm.Environment import staticEnvironment

from Helper import obstacleGenerator
from Helper.constants import MOVEMENT
from Simulator import Simulator

import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = None
@app.route('/status', methods=['GET'])
def status():
    """
    This is a health check endpoint to check if the server is running
    :return: a json object with a key "result" and value "ok"
    """
    return jsonify({"result": "ok"})


@app.route('/', methods=['POST'])
def path_finding():
    
    """
    This is the main endpoint for the path finding algorithm
    :return: a json object with a key "data" and value a dictionary with keys "distance", "path", and "commands"
    """
    # Get the json data from the request
    content = request.json
    
    #obstacle_data = json.loads(content)

    """  	
    obstacles = content['obstacles']
    obs = obstacleGenerator.getTestObstacles()
    obs1 = obstacleGenerator.getTestObstacles1()
    obs2 = obstacleGenerator.getTestObstacles2()
    obs3 = obstacleGenerator.getTestObstacles3()
    obs4 = obstacleGenerato r.getTestObstacles4()
    obs5 = obstacleGenerator.getTestObstacles5()
    obsTest = obstacleGenerator.getTestObstaclesTest()
    #userInputObs = obstacleGenerator.getObstaclesThroughUserInput()
    inputTxtObs = obstacleGenerator.getObstaclesThroughTxt()
    """
    print(content)
    jsonObstacles = obstacleGenerator.getObstaclesThroughJson(content)
    #print(jsonObstacles)
    #print(jsonObstacles[0].pos)
    print("test1")
    sim = Simulator(staticEnvironment((250, 250), jsonObstacles), jsonObstacles, False)   
    sim.initialize_without_simulator()
    #print("test2")
    #sim.initialize()
    #sim.run()
    
    with open("log.txt" , "r") as file:
        command_string = file.readline().strip()

    if command_string != "":
        print(command_string)
        print("Command string has been successfully generated and sent over")

    return command_string


def simulation():
    obs = obstacleGenerator.getTestObstacles()
    obs1 = obstacleGenerator.getTestObstacles1()
    obs2 = obstacleGenerator.getTestObstacles2()
    obs3 = obstacleGenerator.getTestObstacles3()
    obs4 = obstacleGenerator.getTestObstacles4()
    obs5 = obstacleGenerator.getTestObstacles5()
    obsTest = obstacleGenerator.getTestObstaclesTest()
    #userInputObs = obstacleGenerator.getObstaclesThroughUserInput()
    inputTxtObs = obstacleGenerator.getObstaclesThroughTxt()

    sim = Simulator(staticEnvironment((220, 220), inputTxtObs), inputTxtObs, False)   
    #sim.initialize_without_simulator()
    sim.initialize()
    sim.run()
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #simulation()    