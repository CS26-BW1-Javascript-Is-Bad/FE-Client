import pygame as pg
from core.util.colors import *

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(pg.font.match_font('arial'), size)
    # True is for Anti Aliasing
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)