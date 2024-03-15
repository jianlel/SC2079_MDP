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
#from model import *

app = Flask(__name__)
CORS(app)
#model = load_model()
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
    obs4 = obstacleGenerator.getTestObstacles4()
    obs5 = obstacleGenerator.getTestObstacles5()
    obsTest = obstacleGenerator.getTestObstaclesTest()
    #userInputObs = obstacleGenerator.getObstaclesThroughUserInput()
    inputTxtObs = obstacleGenerator.getObstaclesThroughTxt()
    """

    jsonObstacles = obstacleGenerator.getObstaclesThroughJson(content)
    
    print("test1")
    sim = Simulator(staticEnvironment((200, 200), jsonObstacles), jsonObstacles, False)   
    sim.initialize_without_simulator()
    #sim.initialize()
    #sim.run()
    print("test2")
    
    with open("log.txt" , "r") as file:
        command_string = file.readline().strip()

    return command_string
    
"""
@app.route('/image', methods=['POST'])
def image_predict():

    #This is the main endpoint for the image prediction algorithm
    #:return: a json object with a key "result" and value a dictionary with keys "obstacle_id" and "image_id"

    file = request.files['file']
    filename = file.filename
    file.save(os.path.join('uploads', filename))
    # filename format: "<timestamp>_<obstacle_id>_<signal>.jpeg"
    constituents = file.filename.split("_")
    obstacle_id = constituents[1]

    ## Week 8 ## 
    #signal = constituents[2].strip(".jpg")
    #image_id = predict_image(filename, model, signal)

    ## Week 9 ## 
    # We don't need to pass in the signal anymore
    image_id = predict_image_week_9(filename,model)

    # Return the obstacle_id and image_id
    result = {
        "obstacle_id": obstacle_id,
        "image_id": image_id
    }
    return jsonify(result)

@app.route('/stitch', methods=['GET'])
def stitch():
    
    #This is the main endpoint for the stitching command. Stitches the images using two different functions, in effect creating two stitches, just for redundancy purposes
    
    img = stitch_image()
    img.show()
    img2 = stitch_image_own()
    img2.show()
    return jsonify({"result": "ok"})
"""

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

    sim = Simulator(staticEnvironment((400, 400), obs5), obs5, False)   
    #sim.initialize_without_simulator()
    sim.initialize()
    sim.run()
    

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    simulation()