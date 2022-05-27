import pygame
from pygame.sprite import Sprite
from random import randint


class Star(Sprite):

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load('images/bullets/lv1Bullet.bmp')
        rand_size = randint(self.settings.min_star_size, self.settings.max_star_size)
        self.image = pygame.transform.scale(self.image, (rand_size, rand_size))
        self.rect = self.image.get_rect()

        self.rect.x = randint(0, self.settings.screen_width)
        self.rect.y = randint(0, self.settings.screen_height)
