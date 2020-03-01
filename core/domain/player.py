from domain.base_models.entity import Entity
from util.colors import *
from util.settings import *
import pygame as pg
vec = pg.math.Vector2

class Player(Entity):
    
    def __init__(self,room, game, x, y, inventory=None, equipped_weapon=None):
        self.image = game.player_img
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        super().__init__(self.image, self.rect, room)
        self.inventory = inventory
        self.game = game
        self.equipped_weapon = equipped_weapon
        self.speed = 5
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.game.all_sprites.add(self)
        self.can_jump = True
        
    def get_keys(self):
        self.vel = vec(0, self.vel.y)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            if self.can_jump:
                self.jump()
                self.can_jump = False
        
    def jump(self):
        self.vel.y = -20
        
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.rect.x = self.pos.x
        if dir == 'y':
             hits = pg.sprite.spritecollide(self, self.game.walls, False)
             if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                    self.can_jump = True
                    self.vel.y = 0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                    self.vel.y = 0
                self.rect.y = self.pos.y
                
             hits = pg.sprite.spritecollide(self, self.game.platforms, False)
             if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                    self.can_jump = True
                    self.vel.y = 0
                self.rect.y = self.pos.y
             hits = pg.sprite.spritecollide(self, self.game.portals, False)
             if hits:
                self.game.change_map(self.game.map.to_e)

    def update(self):
        self.get_keys()
        self.acc.y = .5
        if self.vel.y >= MAX_GRAVITY:
            self.vel.y = MAX_GRAVITY
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')