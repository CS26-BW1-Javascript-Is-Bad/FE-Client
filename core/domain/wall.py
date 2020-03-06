import pygame as pg
import os.path as path
from util.colors import *
from util.settings import *

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites, game.walls
        self.image = pg.image.load(path.join(sprite_folder, "blank.png")).convert_alpha()
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
class Portal(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, dir):
        self.dir = dir
        self.groups = game.all_sprites, game.portals
        self.image = pg.image.load(path.join(sprite_folder, "temp_portal.png"))
        self.image.set_colorkey(BLACK)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if dir == 'n':
            self.image = pg.transform.rotate(self.image, 90)
            self.rect = pg.Rect(x, y, w, h)
        if dir == 's':
            self.image = pg.transform.rotate(self.image, 270)
            self.rect = pg.Rect(x, y+40, w, h)
        if dir == 'w':
            self.rect = pg.Rect(x+32, y, w, h)
        if dir == 'e':
            self.rect = pg.Rect(x, y, w, h)
        self.image = pg.transform.scale(self.image, (int(w), int(h)))
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y