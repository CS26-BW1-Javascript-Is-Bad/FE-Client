from util.settings import *
import pygame as pg
import pytmx
import os.path as path


class Room():
    def __init__(self, asset=""):
        self.asset = asset
        self.e_to = None
        self.n_to = None
        self.w_to = None
        self.s_to = None
        
        
    def init(self):        
        tm = pytmx.load_pygame(self.asset, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
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
        
        
