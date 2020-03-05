import pygame as pg
import random
from os import path
import json
from core.camera import *
from core.domain.map import *
from core.domain.platform import *
from core.domain.player import *
from core.domain.repository import *
from core.domain.wall import *
from core.map_generator import *
from core.util.colors import *
from core.util.functions import draw_text
from core.util.settings import *
from core.util.text_input import *
import core.util.constants as constants


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
        self.first_load = True
    
    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.portals = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.mini_map_sprite = pg.sprite.Group()
        self.load_data()
        self.camera = Camera(self.room.width, self.room.height)
        
    
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
        self.room.visited = True
        self.all_sprites.empty()
        self.mini_map_sprite.empty()
        self.walls.empty()
        self.platforms.empty()
        self.mobs.empty()
        self.portals.empty()
        self.map_img = self.room.make_map()
        self.map_rect = self.map_img.get_rect()
        self.mini_map = MiniMap(self, self.map)
        
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
        if not self.first_load:
            player_change_room(self.dir)
        self.first_load = False



    def load_data(self):
        self.mob_img = pg.image.load(path.join(sprite_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (TILESIZE, TILESIZE))
        self.player_img = pg.image.load(path.join(sprite_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(sprite_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.platform_img = pg.image.load(path.join(sprite_folder, PLATFORM_IMG)).convert_alpha()
        self.platform_img = pg.transform.scale(self.platform_img, (TILESIZE, TILESIZE))

        self.map, first_room = get_map()
        self.map.game = self


        self.map.game = self

        if first_room.n_to != 0:
            self.dir = 's'
        elif first_room.s_to != 0:
            self.dir = 'n'
        elif first_room.e_to != 0:
            self.dir = 'w'
        elif first_room.w_to != 0:
            self.dir = 'e'
        
        self.change_room(first_room)
    
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
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect),)
       # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()
    
    def show_start_screen(self):
        draw_text(self.screen, "TEST TEXT", 24, 400, 400)

    
    def show_quit_screen(self):
        pass


    def game_intro(self):
        intro = True
        textinput = TextInput()
        textinput.antialias = True
        textinput.font_object = pg.font.Font(path.join(game_folder,'data/arial.ttf'), 30)

        textinput2 = TextInput()
        textinput2.antialias = True
        textinput2.font_object = pg.font.Font(path.join(game_folder, 'data/arial.ttf'), 30)

        username_focus = True
        login_successful = False

        while intro:
            events = pg.event.get()
            for event in events:
                print(event)
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            self.screen.fill((255, 255, 255))

            if username_focus:
                if textinput.update(events):
                    username_focus = False

            else:
                if textinput2.update(events):
                    username_focus = True

            # Blit its surface onto the screen
            w, h = pg.display.get_surface().get_size()

            draw_text(self.screen, "Username", 30, w//2, h//2 - 200)
            self.screen.blit(textinput.get_surface(), (w//2-100, h//2 - 150))
            draw_text(self.screen, "Password", 30, w//2, h//2)
            self.screen.blit(textinput2.get_surface(), (w//2-100, h//2 + 50))

            mouse = pygame.mouse

            if w//2-175 + 150 > mouse.get_pos()[0] > w//2-175 and 500+50 > mouse.get_pos()[1] > 500:
                pygame.draw.rect(self.screen, DARKGREY, (w//2-175, 500, 150, 50))
                if pg.mouse.get_pressed()[0]:
                    constants.TOKEN = login(textinput.get_text(), textinput2.get_text())
                    if constants.TOKEN:
                        return
            else:
                pygame.draw.rect(self.screen, LIGHTGREY, (w//2-175, 500, 150, 50))

            if w//2+25 + 150 > mouse.get_pos()[0] > w//2+25 and 500 + 50 > mouse.get_pos()[1] > 500:
                pygame.draw.rect(self.screen, DARKGREY, (w//2+25, 500, 150, 50))
                if pg.mouse.get_pressed()[0]:
                    constants.TOKEN = register(textinput.get_text(), textinput2.get_text())
                    if constants.TOKEN:
                        return
            else:
                pygame.draw.rect(self.screen, LIGHTGREY, (w//2+25, 500, 150, 50))

            draw_text(self.screen, "Login", 15, w // 2 + 100, 515)
            draw_text(self.screen, "Register", 15, w // 2 - 100, 515)

            pygame.display.update()
            self.clock.tick(30)


g = Game()
while g.running:
    g.show_start_screen()
    g.game_intro()
    g.new()
    g.run()
    g.show_quit_screen()
pg.quit()

