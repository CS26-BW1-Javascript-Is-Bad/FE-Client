import pygame as pg
import random
from os import path
from domain.room import Room
from domain.player import Player
from domain.mob import Mob
from util.colors import *
from util.settings import *
from domain.wall import *
from domain.platform import Platform
from domain.map import *
from camera import Camera


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.all_sprites = pg.sprite.Group()
        self.map_data = []
    
    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.load_data()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.camera = Camera(self.map.width, self.map.height)
        playerx, playery = 10, 10
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
        
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(Room(), self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'platform':
                Platform(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
    
    
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        
    def load_data(self):
        
        self.map = TiledMap(path.join(tilemap_folder, 'testmap1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.mob_img = pg.image.load(path.join(sprite_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (TILESIZE, TILESIZE))
        self.player_img = pg.image.load(path.join(sprite_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(sprite_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.platform_img = pg.image.load(path.join(sprite_folder, PLATFORM_IMG)).convert_alpha()
        self.platform_img = pg.transform.scale(self.platform_img, (TILESIZE, TILESIZE))
    
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

