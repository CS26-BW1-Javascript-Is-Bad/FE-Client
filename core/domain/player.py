from core.domain.base_models.entity import Entity
from core.util.colors import *


class Player(Entity):
    def __init__(self, asset, room, inventory=None, equipped_weapon=None):
        self.asset.set_colorkey(BLACK)
        self.rect = self.asset.get_rect()
        super().__init__(asset, self.rect, room)
        self.inventory = inventory
        self.equipped_weapon = equipped_weapon
