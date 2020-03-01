import pygame as pg
from util.settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height
    
    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        self.camera = pg.Rect(x, y, self.width, self.height)
    
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)