import pygame
from pygame.locals import *
import random
from os import path

pygame.init()

img_dir = path.join(path.dirname('_file_'), 'image_dir')

WHITE = (255, 255, 255)
BLK = (0, 0, 0)
GREEN = (20, 255, 20)
BLUE = (0, 0, 255)
YLLW = (255, 255, 0)
RED = (255, 0, 0)

wHIGH = 400
wWIDE = 800

i = 0

typeface = pygame.font.match_font('comic_sans_MS')


def show_text(surf, t, large, pos_x, pos_y):
    type_face = pygame.font.Font(typeface, large)
    f_render = type_face.render(t, True, GREEN)
    text_pos = f_render.get_rect()
    text_pos.midtop = (pos_x, pos_y)
    surf.blit(f_render, text_pos)


screen = pygame.display.set_mode([wWIDE, wHIGH])

pygame.display.set_caption('Dodge game')


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_image = pygame.image.load(path.join(img_dir, "player.png")).convert_alpha()

        self.image = pygame.transform.scale(player_image, (50, 38))

        # self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = wWIDE / 2
        self.rect.y = wHIGH / 1.2
        self.change_x = 0
        self.change_y = 0
        self.walls = None
        self.radius = (self.rect.width * .5)

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):

        self.rect.y += self.change_y

        self.rect.x += self.change_x

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
        self.rect.y = random.randrange(-100, 40)
        self.rect.x = random.randrange(wWIDE - self.rect.width)
        self.velocity_y = random.randrange(3, 5)
        self.velocity_x = random.randrange(-2, 2)
        self.radius = self.rect.width * .75
        self.image = asteroid

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x
        if self.rect.top > wHIGH + 10:
            self.rect.x = random.randrange(wWIDE - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocity_y = random.randrange(3, 5)
            self.velocity_x = random.randrange(-2, 2)


class BlocksRight(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(wHIGH - self.rect.height)
        self.rect.x = random.randrange(-100, 40)
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


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


wall_list = pygame.sprite.Group()

block_list = pygame.sprite.Group()

# player collision add?


def main_menu():
    screen.blit(background, bg_full)
    # why wont this show up?????
    show_text(screen, "F to start/restart, arrow keys to move", 20, 400, 100)
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


background = pygame.image.load(path.join(img_dir, "SPAAAAACE.jpg")).convert()
asteroid = pygame.image.load(path.join(img_dir, "Asteroid.png")).convert()
bg_full = background.get_rect()

clock = pygame.time.Clock()

points = 0
dead = True

done = True

while done:
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

    collis = pygame.sprite.spritecollide(player, space_rocks, False, pygame.sprite.collide_circle)
    if collis:
        dead = True

    points += 1/8

    all_sprite_list.update()
    screen.fill(BLK)
    screen.blit(background, bg_full)
    show_text(screen, "Points: " + str(int(points)), 20, 500, 20)
    all_sprite_list.draw(screen)
    pygame.display.flip()

    clock.tick(60)
