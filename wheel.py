import pygame
import settings
from random import random


class Wheel:
    def __init__(self, select, screen):
        self.screen = screen
        self.wheel = pygame.sprite.GroupSingle()
        WheelSprite(select, settings.WIDTH // 2, int(settings.HEIGHT * 0.3), self.wheel)

    def rotate(self):
        self.wheel.sprite.rotate()

    def update(self, tick):
        self.wheel.update(tick)
        self.wheel.draw(self.screen)
        x = self.wheel.sprite.x
        y = self.wheel.sprite.y - self.wheel.sprite.sprite.get_height() // 2
        pygame.draw.polygon(self.screen, pygame.Color('orangered'), ((x - 10, y - 10), (x, y + 10), (x + 10, y - 10)))


class WheelSprite(pygame.sprite.Sprite):
    def __init__(self, callback, x, y, group):
        super().__init__(group)
        self.callback = callback
        self.x, self.y = x, y
        self.sprite = pygame.image.load(settings.wheel).convert_alpha()
        self.image = self.sprite
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.angle = random() * 360
        self.speed = 0

    def rotate(self):
        self.speed = settings.min_speed + random() * (settings.max_speed - settings.min_speed)

    def update(self, tick):
        if self.speed > 0:
            self.angle = (self.angle + self.speed * tick) % 360
            self.image = pygame.transform.rotate(self.sprite, self.angle)
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.speed -= settings.boost * tick
            if self.speed <= 0:
                self.callback(settings.options[int(self.angle / 360 * len(settings.options) + 0.49)])

