import numpy as np

BLOCK_SIZE = 10

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

FRAMES = 30

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (122, 213, 1)
BLUE = (0, 0, 128)
RED = (251, 0, 0)
PURPLE = (198, 115, 255)
YELLOW = (253, 235, 163)

TURNING_RADIUS_X = 15
TURNING_RADIUS_Y = 15
SPEED_FACTOR = 5
CORNER_OFFSET = 15
MAX_STEERING_ANGLE = np.pi / 5

GRID_OFFSET = 100
GRID_Y_OFFSET = 400
GRID_SCALE_FACTOR = 5

STUFF_X_OFFSET = 5
STUFF_Y_OFFSET = 5

OUTPUT_FILE_PATH = "log.txt"

INPUT_FILE_PATH = "input.txt"

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

