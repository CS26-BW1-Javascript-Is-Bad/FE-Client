import os
from util.colors import *

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
MAX_GRAVITY = 30

TITLE = "Javascript is Bad"

TILESIZE = 32
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE


# images
PLAYER_IMG = "test_char.png"
WALL_IMG = "element_green_square.png"
MOB_IMG = "test_enemy.png"
PLATFORM_IMG = "element_blue_square.png"

# Assets
game_folder = os.path.join(os.path.abspath(os.curdir))
asset_folder = os.path.join(game_folder, "assets")
sprite_folder = os.path.join(asset_folder, "sprites")
tilemap_folder = os.path.join(asset_folder, "tilemaps")
sound_folder = os.path.join(asset_folder, "sound")
