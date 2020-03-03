import pygame as pg
import random
from os import path

from core.camera import *
from core.domain.platform import *
from core.domain.player import *
from core.domain.wall import *
from core.map_generator import *
from core.util.colors import *
from core.util.settings import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.all_sprites = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.map_data = []
        self.room = None
    
    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.portals = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.load_data()
        self.camera = Camera(self.room.width, self.room.height)
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == '2':
        #             Platform(self, col, row)
        #         if tile == 'm':
        #             Mob(self, col, row)
        #         if tile == 'p':
        #             playerx, playery = col, row
        
        
    
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        if self.player.pos.x < 0 or self.player.pos.x > self.room.width or self.player.pos.y < 0 or self.player.pos.y > self.room.height:
            self.player.pos = pg.math.Vector2(self.player.start_x, self.player.start_y)
        self.all_sprites.update()
        self.camera.update(self.player)
        
    def change_room(self, room):
        if room is None:
            return
        self.room = room
        self.room.init()
        self.all_sprites.empty()
        self.walls.empty()
        self.platforms.empty()
        self.mobs.empty()
        self.portals.empty()
        self.map_img = self.room.make_map()
        self.map_rect = self.map_img.get_rect()
        pg.time.delay(100)
        
        for tile_object in self.room.tmxdata.objects:
            if tile_object.name == 'p_n' and self.dir == 's':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'p_s'and self.dir == 'n':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'p_e'and self.dir == 'w':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'p_w'and self.dir == 'e':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'platform':
                Platform(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'portal_e':
                Portal(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, 'e')
            if tile_object.name == 'portal_w':
                Portal(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, 'w')
            if tile_object.name == 'portal_n':
                Portal(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, 'n')
            if tile_object.name == 'portal_s':
                Portal(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, 's')


    def load_data(self):
        self.mob_img = pg.image.load(path.join(sprite_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (TILESIZE, TILESIZE))
        self.player_img = pg.image.load(path.join(sprite_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(sprite_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.platform_img = pg.image.load(path.join(sprite_folder, PLATFORM_IMG)).convert_alpha()
        self.platform_img = pg.transform.scale(self.platform_img, (TILESIZE, TILESIZE))
        
        self.map = Room_Generator(6).set_rooms()
        #change this to starter room
        rand_room = random.choice(self.map)
        if rand_room.n_to is not None:
            self.dir = 's'
        elif rand_room.s_to is not None:
            self.dir = 'n'
        elif rand_room.e_to is not None:
            self.dir = 'w'
        elif rand_room.w_to is not None:
            self.dir = 'e'
        
        self.change_room(rand_room)
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                        self.playing = False
                self.running = False


    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
       # self.screen.fill(BGCOLOR)
       # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()
    
    def show_start_screen(self):
        pass
    
    def show_quit_screen(self):
        pass


g = Game()
while g.running:
    g.show_start_screen
    g.new()
    g.run()
    g.show_quit_screen
pg.quit()

