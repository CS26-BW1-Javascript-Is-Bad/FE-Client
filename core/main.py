import pygame
import random
import os
from core.domain.room import Room
from core.domain.player import Player

WIDTH = 800
HEIGHT = 600
FPS = 30

# setup assets folders
game_folder = os.path.dirname(__file__)
asset_folder = os.path.join(game_folder, "assets")
sprite_folder = os.path.join(asset_folder, "sprites")
tilemap_folder = os.path.join(asset_folder, "tilemaps")
sound_folder = os.path.join(asset_folder, "sound")


test_room = Room()
player_asset = pygame.image.load(
    os.path.join(sprite_folder, "test_char.png")).convert()
player = Player(player_asset, test_room)

# initialize Pygame and create window
pygame.init()
# allows sound
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Javascript is Bad")
# allows constant fps
clock = pygame.time.Clock()
# sets all sprites group, all sprites in a room should be added to this
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
mobs = pygame.sprite.Group()
items = pygame.sprite.Group()

all_sprites.add(player)
player_group.add(player)
# Game Loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # sets up double buffering - always doing this After drawing everything
    pygame.display.flip()

pygame.quit()
