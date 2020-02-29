import pygame as pg
import random
import os
from domain.room import Room
from domain.player import Player
from util.colors import *
from util.settings import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.all_sprites = pg.sprite.Group()
    
    def new(self):
        self.player = Player(pg.image.load(os.path.join(sprite_folder, "test_char.png")).convert(), Room())
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        self.all_sprites.update()
    
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
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    
    def show_start_screen(self):
        pass
    
    def show_quit_screen(self):
        pass


g = Game()
while g.running:
    g.show_start_screen
    g.new()
    g.show_quit_screen
pg.quit()

