import pygame as pg
import os.path as path
from util.colors import *
from util.settings import *

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(sprite_folder, "blank.png")).convert_alpha()
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        