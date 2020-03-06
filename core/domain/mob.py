from domain.base_models.entity import Entity
from util.settings import *
import pygame as pg
import os.path as path
vec = pg.math.Vector2


class Mob(Entity):
    def __init__(self, game, x, y, room=None):
        self.game = game
        self.room = room
        self.image_orig = pg.image.load(path.join(sprite_folder, MOB_IMG)).convert_alpha()
        self.image = pg.image.load(path.join(sprite_folder, MOB_IMG)).convert_alpha()
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        super().__init__(self.image, self.rect, self.room)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.game.mobs.add(self)
        self.game.all_sprites.add(self)
        self.rot = 0
        
    def target(self, target):
        pass
    
    def attack(self, target):
        pass
        
    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
