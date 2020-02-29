import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, asset, rect, room, health=50, lat=50, lon=50):
        pygame.sprite.Sprite.__init__(self)
        self.asset = asset
        self.rect = rect
        self.health = health
        self.lat = lat
        self.lon = lon
        self.room = room
