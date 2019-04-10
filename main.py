import pygame
from pygame.locals import *
import math
from time import sleep

WHITE = (255, 255, 255)
BLK = (0, 0, 0)
GREEN = (20, 255, 20)
i = 0


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

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
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLK)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


pygame.init()


screen = pygame.display.set_mode([800, 800])

pygame.display.set_caption('test')

all_sprite_list = pygame.sprite.Group()

wall_list = pygame.sprite.Group()

wall = Wall(0, 0, 10, 610)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(10, 0, 600, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(10, 600, 600, 10)
wall_list.add(wall)
all_sprite_list.add(wall)
# x, y, length, width
wall = Wall(600, 0, 10, 600)
wall_list.add(wall)
all_sprite_list.add(wall)

player = Player(50, 50)
player.walls = wall_list

all_sprite_list.add(player)

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
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

    screen.fill(GREEN)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)





