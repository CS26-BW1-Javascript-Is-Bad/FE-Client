import math
import core.util.constants as constants
import os.path as path
import pygame as pg
import pytmx

from core.util.colors import *
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

        self.game.screen.fill(BLACK)
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

            while i < grid_size + 1:
                j = 1
                while j < grid_size + 1:
                    offsetx = j * room_size + 40
                    offsety = i * room_size + 40
                    pg.draw.rect(self.game.screen, LIGHTGREY, (pos[0] + offsetx + 5, pos[1] + offsety + 5, room_size, room_size))

                    self.game.screen
                    if self.rooms[counter].n_to:
                        pass
                        # draw north rect
                    if self.rooms[counter].s_to:
                        pass
                        # draw south rect
                    if self.rooms[counter].e_to:
                        pass
                        # draw east rect
                    if self.rooms[counter].w_to:
                        pass
                        # draw west rect
                    j += 1
                    counter += 1
                i += 1
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
