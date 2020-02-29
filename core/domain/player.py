from domain.base_models.entity import Entity
from util.colors import *
import pygame as pg


class Player(Entity):
    
    def __init__(self, image, room, inventory=None, equipped_weapon=None):
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        super().__init__(self.image, self.rect, room)
        self.inventory = inventory
        self.equipped_weapon = equipped_weapon
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a] or keystate[pg.K_LEFT]:
            self.speedx = -5
        if keystate[pg.K_d] or keystate[pg.K_RIGHT]:
            self.speedx = 5
        if keystate[pg.K_w] or keystate[pg.K_UP]:
            self.speedy = -5
        if keystate[pg.K_s] or keystate[pg.K_DOWN]:
            self.speedy = 5


        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > self.room.WIDTH:
            self.rect.right = self.room.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.room.HEIGHT:
            self.rect.bottom = self.room.HEIGHT