from util.settings import *
from util.colors import *
import math
import os.path as path
import pygame as pg
import pytmx

from core.util.settings import *


class Map:
    def __init__(self, rooms):
        self.rooms = rooms
        self.size = math.sqrt(len(rooms))
        self.visited_list = []
        self.game = None
        self.mini_map = None

    def make_mini_map(self):
        self.mini_map = MiniMap(self.game, self)


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