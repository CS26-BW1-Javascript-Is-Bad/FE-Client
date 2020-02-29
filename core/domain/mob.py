from core.domain.base_models.entity import Entity


class Mob(Entity):
    def __init__(self, asset, rect, room):
        super().__init__(asset, rect, room)
