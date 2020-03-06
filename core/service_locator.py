"""`Singleton` providers example."""

import collections
import pygame
import os
import dependency_injector.providers as providers
import domain.player as Player

# Singleton provider creates new instance of specified class on first call and
# returns same instance on every next call.




pygame.init()
pygame.mixer.init()
pygame.display.set_mode((800, 600))
pygame_provider = providers.Object(pygame)


pygame_service = pygame_provider()
