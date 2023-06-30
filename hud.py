import pygame
import settings
from ui import LinearLayout, Clickable, TextView, ClickableText, load, font


class Hud:
    def __init__(self, callback, screen):
        self.callback = callback
        self.screen = screen

        self.score = LinearLayout(load(settings.card_md), screen.get_width() * 0.02, screen.get_height() * 0.13)

        self.alert = LinearLayout(load(settings.card_md), screen.get_width() * 0.02, screen.get_height() * 0.55)

        self.button = LinearLayout(load(settings.card_md), screen.get_width() * 0.71, screen.get_height() * 0.55)

        self.clickable = Clickable(self.on_click)
        self.prize = None
        self.active = True

    @staticmethod
    def set_text(attr, text):
        attr.empty()
        for el in text:
            TextView(el, font(40), attr)
        attr.update()

    def set_prize(self, callback):
        self.prize = pygame.sprite.Group()
        self.alert.empty()
        ClickableText('Забрать приз', font(40), lambda: callback(True), self.prize, self.alert)
        ClickableText('Получить 500 очков', font(40), lambda: callback(False), self.prize, self.alert)
        self.alert.update()

    def on_click(self):
        self.active = False
        self.callback()

    def update(self):
        self.score.draw(self.screen)
        self.alert.draw(self.screen)
        if self.active:
            self.clickable.update(self.button.sprite.rect)
            self.button.draw(self.screen)
        if self.prize is not None:
            self.prize.update()
