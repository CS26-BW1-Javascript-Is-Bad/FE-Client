from core.domain.base_models.entity import Entity


class Player(Entity):
    def __init__(self, asset, rect, room, inventory=None, equipped_weapon=None):
        super().__init__(asset, rect, room)
        self.inventory = inventory
        self.equipped_weapon = equipped_weapon
