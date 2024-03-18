import json
from Entities.Obstacle import Obstacle
import Helper.settings as settings

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
getObstacles(x)
print(obsList)