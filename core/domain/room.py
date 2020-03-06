import pygame as pg
import pytmx
import requests
import json

from core.domain.map import Map
from core.util.constants import *
import os.path as path

from core.util.settings import tilemap_folder

class Room():
    def __init__(self, asset="", n_to=None, s_to=None, e_to=None, w_to=None, x=None, y=None, visited=None):
        self.asset = path.join(tilemap_folder, asset)
        self.n_to = n_to
        self.s_to = s_to
        self.e_to = e_to
        self.w_to = w_to
        self.x = x
        self.y = y
        self.visited = visited

    def get_coordinates(self):
        return (self.x, self.y)

    def init(self):
        tm = pytmx.load_pygame(self.asset, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledImageLayer):
                surface.blit(layer.image, (-5, 0))
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

