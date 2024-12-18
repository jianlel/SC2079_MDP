import numpy as np

BLOCK_SIZE = 20

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

FRAMES = 1

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (122, 213, 1)
BLUE = (0, 0, 128)
RED = (251, 0, 0)
PURPLE = (198, 115, 255)
YELLOW = (253, 235, 163)

TURNING_RADIUS_X = 20 # Original is 20
TURNING_RADIUS_Y = 20 # Original is 20 
SPEED_FACTOR = 10
MAX_STEERING_ANGLE = np.pi / 5

GRID_OFFSET = 100
GRID_Y_OFFSET = 400
GRID_SCALE_FACTOR = 10

STUFF_X_OFFSET = 10
STUFF_Y_OFFSET = 10

COMMANDS = {
    's': 'FW',
    'b': 'BW',
    'd': 'C',
    'u': 'A',
    'w': 'BR',
    'v': 'BL'
}

DIR = {
    0: 'N',
    4: 'S',
    6: 'W',
    2: 'E'
}

OUTPUT_FILE_PATH = "log.txt"

INPUT_FILE_PATH = "input.txt"