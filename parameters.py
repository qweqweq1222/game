import math
# game settings
WORLD_WIDTH = 2400
WIDTH = 1200

WORLD_HEIGHT = 1600
HEIGHT = 800
TILE = 100

# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300
MAX_DEPTH = 800
FAKE = 100
DELTA_ANGLE = FOV / NUM_RAYS
DISTANCE = 0.5 * NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DISTANCE * TILE
SCALE = WIDTH // NUM_RAYS
CENTER_RAY = NUM_RAYS // 2 - 1

# player settings
player_pos = (200, 150)
player_angle = 0
player_speed = 3

# map
MINIMAP_SCALE = 5
MAP_SCALE = 2 * MINIMAP_SCALE
MAP_TILE = TILE // MAP_SCALE

# texture
TEXTURE_SCALE = WIDTH // TILE
# colors
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)



