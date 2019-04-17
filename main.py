import pygame
from pygame.locals import *
import random
import math
from time import sleep

WHITE = (255, 255, 255)
BLK = (0, 0, 0)
GREEN = (20, 255, 20)
BLUE = (0, 0, 255)
YLLW = (255, 255, 0)
RED = (255, 0, 0)

wHIGH = 400
wWIDE = 800

i = 0


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0
        self.walls = None

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


pygame.init()


screen = pygame.display.set_mode([wWIDE, wHIGH])

pygame.display.set_caption('Dodge game')

all_sprite_list = pygame.sprite.Group()

wall_list = pygame.sprite.Group()

block_list = pygame.sprite.Group()

# player init

player = Player(50, 50)

# wall list

player.walls = wall_list


# player collision add?

space_rocks = pygame.sprite.Group()
all_sprite_list.add(player)

for i in range(5):
    dodge_entity_top = Blocks()
    all_sprite_list.add(dodge_entity_top)
    space_rocks.add(dodge_entity_top)

    dodge_entity_right = BlocksRight()
    all_sprite_list.add(dodge_entity_right)
    space_rocks.add(dodge_entity_right)


dead = True

clock = pygame.time.Clock()

done = False

while dead:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = False
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
    all_sprite_list.update()

    screen.fill(BLK)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)





