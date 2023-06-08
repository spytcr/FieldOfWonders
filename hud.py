import pygame
import settings
from ui import LinearLayout, Clickable, TextView


class Hud:
    def __init__(self, callback, screen):
        self.callback = callback
        self.screen = screen

        self.score = LinearLayout(pygame.image.load(settings.card_md).convert_alpha(),
                                  settings.WIDTH * 0.02, settings.HEIGHT * 0.1)

        self.alert = LinearLayout(pygame.image.load(settings.card_md).convert_alpha(),
                                  settings.WIDTH * 0.02, settings.HEIGHT * 0.55)

        self.button = LinearLayout(pygame.image.load(settings.card_md).convert_alpha(),
                                   settings.WIDTH * 0.75, settings.HEIGHT * 0.55)

        self.clickable = Clickable(self.on_click)
        self.active = True

    @staticmethod
    def set_text(attr, text):
        attr.empty()
        for el in text:
            TextView(el, pygame.font.SysFont('arialblack', 26), attr)
        attr.update()

    def on_click(self):
        self.active = False
        self.callback()

    def update(self):
        self.score.draw(self.screen)
        self.alert.draw(self.screen)
        if self.active:
            self.clickable.update(self.button.sprite.rect)
            self.button.draw(self.screen)
