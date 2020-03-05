import pygame as pg
from core.util.colors import *
import os.path as path

from core.util.settings import game_folder


def draw_text(surf, text, size, x, y):
    font = pg.font.Font(path.join(game_folder, 'data/arial.ttf'), size)
    # True is for Anti Aliasing
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
