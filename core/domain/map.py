import math
import core.util.constants as constants
import os.path as path
import pygame as pg
import pytmx

from core.util.colors import *
from core.util.functions import draw_text
from core.util.settings import *


class Map:
    def __init__(self, rooms):
        self.rooms = rooms
        self.size = math.sqrt(len(rooms))
        self.visited_list = []
        self.game = None
        self.mini_map = None


    def show_map(self):
        grid_size = math.sqrt(len(self.rooms))
        x, y = self.game.screen.get_size()
        room_size = int(x / grid_size * .2)
        pos = (x//2 - (room_size * (grid_size//2)), y//2 - (room_size * (grid_size//2)))

        #self.game.screen.fill(BLACK)
        while True:

            offsety = 0
            offsetx = 0
            i = 1
            counter = 0
            events = pg.event.get()
            for event in events:
                print(event)
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            keys = pg.key.get_pressed()
            if keys[pg.K_n]:
                return
            room_dimension = 12
            room_scale = 30
            n_to_x_offset = 4
            n_to_y_offset = 17
            n_to_line_width = 4
            n_to_line_height = 18
            for room in self.rooms:
                room_color = PURPLE
                if room.x == self.game.room.x and room.y == self.game.room.y:
                    room_color = GREEN
                pg.draw.rect(self.game.screen, room_color, (room.y * room_scale, room.x * room_scale, room_dimension, room_dimension))
                if room.n_to != 0:
                    pg.draw.rect(self.game.screen, RED, (room.y * room_scale + n_to_x_offset,
                                                         room.x * room_scale - n_to_y_offset, n_to_line_width,
                                                         n_to_line_height))
                if room.e_to != 0:
                    pg.draw.rect(self.game.screen, RED, (room.y * room_scale + n_to_y_offset - 4,
                                                         room.x * room_scale + n_to_x_offset, n_to_line_height,
                                                         n_to_line_width))

            pg.display.update()
            pg.display.flip()


class MiniMap():
    def __init__(self, game, map):
        self.game = game
        self.map = map

    def build_map(self):
        self.map_group = pg.sprite.Group()
        col = 0
        room_index = 0
        self.map_node_list = []
        while col < self.map.size:
            row = 0
            while row < self.map.size:
                room = self.map.rooms[room_index]
                if room == self.game.room:
                    contains_player = True
                else:
                    contains_player = False
                node = MiniMapNode(row, col, room.visited, contains_player)
                self.map_node_list.append(node)
                self.map_group.add(node)
                row += 1
                room_index += 1
            col += 1
        return self.map_group


class MiniMapNode(pg.sprite.Sprite):
    def __init__(self, x, y, visited, contains_player):
        self.image = pg.image.load(path.join(sprite_folder, PLATFORM_IMG))
        self.rect = self.image.get_rect()
        pg.sprite.Sprite.__init__(self)
