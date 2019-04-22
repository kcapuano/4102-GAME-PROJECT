import pygame
from pygame.locals import *
import random
from os import path

# Mostly initializing here
pygame.init()

img_dir = path.join(path.dirname('_file_'), 'image_dir')

# colors (used under sprites or for things without sprites)
WHITE = (255, 255, 255)
BLK = (0, 0, 0)
GREEN = (20, 255, 20)
BLUE = (0, 0, 255)
YLLW = (255, 255, 0)
RED = (255, 0, 0)

# for window shape and things that need to be positionally based in the window

wHIGH = 400
wWIDE = 800

i = 0
clock = pygame.time.Clock()
typeface = pygame.font.match_font('comic_sans_MS')
screen = pygame.display.set_mode([wWIDE, wHIGH])

# text init


def show_text(surf, t, large, pos_x, pos_y):
    type_face = pygame.font.Font(typeface, large)
    f_render = type_face.render(t, True, GREEN)
    text_pos = f_render.get_rect()
    text_pos.midtop = (pos_x, pos_y)
    surf.blit(f_render, text_pos)


pygame.display.set_caption('Dodge game')


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # loads player image
        player_image = pygame.image.load(path.join(img_dir, "player.png")).convert_alpha()

        self.image = pygame.transform.scale(player_image, (50, 38))

        # self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        # player position relative to window
        self.rect.x = wWIDE / 2
        self.rect.y = wHIGH / 1.2
        # default speed
        self.change_x = 0
        self.change_y = 0
        # old colis
        self.walls = None
        self.radius = (self.rect.width * .5)

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):

        self.rect.y += self.change_y

        self.rect.x += self.change_x
        # for edge collision; stops player from going out of bounds
        if self.rect.right > wWIDE:
            self.rect.right = wWIDE
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > wHIGH:
            self.rect.bottom = wHIGH


class Blocks(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        # asteroid spawn pos
        self.rect.y = random.randrange(-100, 40)
        self.rect.x = random.randrange(wWIDE - self.rect.width)
        # variable speed (more y than x for top to bot)
        self.velocity_y = random.randrange(3, 5)
        self.velocity_x = random.randrange(-2, 2)
        # collision circle
        self.radius = self.rect.width * .75
        self.image = asteroid

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x
        # for reseting the asteroids
        if self.rect.top > wHIGH + 10:
            self.rect.x = random.randrange(wWIDE - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocity_y = random.randrange(3, 5)
            self.velocity_x = random.randrange(-2, 2)


# blocks that move from left to right
class BlocksRight(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(wHIGH - self.rect.height)
        self.rect.x = random.randrange(-100, 40)
        # must have more x than y for right blocks
        self.velocity_x = random.randrange(3, 5)
        self.velocity_y = random.randrange(-2, 2)
        self.radius = self.rect.width * .75
        self.image = asteroid

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        if self.rect.right > wWIDE + 10:
            self.rect.x = random.randrange(0, 30)
            self.rect.y = random.randrange(wHIGH + self.rect.height)
            self.velocity_x = random.randrange(3, 5)
            self.velocity_y = random.randrange(-2, 2)


# currently unused (for the old boundary system, can be used for obstacles though)
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


# this is for starting the game should show text for instructions but doesnt
# It still works, a blank screen will show up but if you press f the game will start
def main_menu():

    screen.blit(background, bg_full)
    # *does not show up*
    show_text(screen, "F to start/restart, arrow keys to move", 20, wWIDE /2, wHIGH/2)
    standby = True
    while standby:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                # f to restart/pay respects
                if event.key == K_f:
                    standby = False


wall_list = pygame.sprite.Group()

block_list = pygame.sprite.Group()

# image init
background = pygame.image.load(path.join(img_dir, "SPAAAAACE.jpg")).convert()
asteroid = pygame.image.load(path.join(img_dir, "Asteroid.png")).convert()
bg_full = background.get_rect()
# points for score!
points = 0
# state init
dead = True

done = True
# game loop starts here
while done:
    # player state (resets game state on death)
    if dead:

        main_menu()
        all_sprite_list = pygame.sprite.Group()
        space_rocks = pygame.sprite.Group()
        player = Player()
        all_sprite_list.add(player)
        points = 0
        dead = False
        for i in range(5):
            dodge_entity_top = Blocks()
            all_sprite_list.add(dodge_entity_top)
            space_rocks.add(dodge_entity_top)

            dodge_entity_right = BlocksRight()
            all_sprite_list.add(dodge_entity_right)
            space_rocks.add(dodge_entity_right)
    # player controls and manual exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                player.changespeed(-3, 0)
            if event.key == K_UP:
                player.changespeed(0, -3)
            if event.key == K_DOWN:
                player.changespeed(0, 3)
            if event.key == K_RIGHT:
                player.changespeed(3, 0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            if event.key == pygame.K_UP:
                player.changespeed(0, 3)
            if event.key == pygame.K_DOWN:
                player.changespeed(0, -3)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
    # collison check
    collis = pygame.sprite.spritecollide(player, space_rocks, False, pygame.sprite.collide_circle)
    if collis:
        dead = True
    # so the points dont look like they're going to fast
    points += 1/8
    # background
    screen.fill(BLK)
    screen.blit(background, bg_full)
    all_sprite_list.update()
    show_text(screen, "Points: " + str(int(points)), 20, 500, 20)
    all_sprite_list.draw(screen)
    pygame.display.flip()

    clock.tick(60)
