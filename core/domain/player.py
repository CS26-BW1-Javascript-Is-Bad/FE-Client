import pygame as pg

from core.domain.remote_data_source import room_from_id
from core.domain.base_models.entity import *
from core.util.settings import *

vec = pg.math.Vector2

class Player(Entity):
    
    def __init__(self, game, x, y, inventory=None, equipped_weapon=None):
        self.image = game.player_img
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        super().__init__(self.image, self.rect)
        self.inventory = inventory
        self.game = game
        self.equipped_weapon = equipped_weapon
        self.speed = 5
        self.start_x = x
        self.start_y = y
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.game.all_sprites.add(self)
        self.can_jump = True
        self.can_move = False
        self.move_right = True
        
    def get_keys(self):
        self.vel = vec(0, self.vel.y)
        keys = pg.key.get_pressed()
        if keys[pg.K_u]:
            self.pos = vec(self.game.room.width//2, self.game.room.height//2)
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -self.speed
            if self.move_right:
                self.image = pg.transform.flip(self.image, True, False)
                self.move_right = False
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = self.speed
            if not self.move_right:
                self.image = pg.transform.flip(self.image, True, False)
                self.move_right = True
        if keys[pg.K_SPACE]:
            if self.can_jump:
                self.jump()
                self.can_jump = False
        if keys[pg.K_m]:
            self.game.map.show_map()
        
    def jump(self):
        self.vel.y = -20
        
    def collide_with_walls(self, dir):
        keys = pg.key.get_pressed()
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
             if hits and not (keys[pg.K_s] or keys[pg.K_DOWN]):
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                    self.can_jump = True
                    self.vel.y = 0
                self.rect.y = self.pos.y
             elif hits and (keys[pg.K_s] or keys[pg.K_DOWN]):
                 pass
                #add logic to slow player down if holding key down and falling through platform
             hits = pg.sprite.spritecollide(self, self.game.portals, False)
             if hits:
                 self.vel.y = 0
                 self.vel.x = 0
                 self.game.dir = hits[0].dir
                 if hits[0].dir == 'n':
                    self.game.change_room(room_from_id(self.game.room.n_to))
                 if hits[0].dir == 's':
                    self.game.change_room(room_from_id(self.game.room.s_to))
                 if hits[0].dir == 'e':
                    self.game.change_room(room_from_id(self.game.room.e_to))
                 if hits[0].dir == 'w':
                    self.game.change_room(room_from_id(self.game.room.w_to))

    def update(self):
        if self.can_move:
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
        else:
            self.acc.y = 0
            self.acc.x = 0
            self.vel.y = 0
            self.vel.x = 0
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
            if self.game.dir == 'n':
                self.vel.y = -5
            self.can_move = True
