import os

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60

TITLE = "Javascript is Bad"

TILESIZE = 32
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE



# Assets
game_folder = os.path.join(os.path.abspath(os.curdir), "core")
asset_folder = os.path.join(game_folder, "assets")
sprite_folder = os.path.join(asset_folder, "sprites")
tilemap_folder = os.path.join(asset_folder, "tilemaps")
sound_folder = os.path.join(asset_folder, "sound")

