import pygame
import settings
from ui import Button, TextView, LinearLayout, Clickable


class Menu:
    def __init__(self, level, callback, screen, commands=None):
        self.callback = callback
        self.screen = screen

        self.logo = pygame.image.load(settings.logo).convert_alpha()

        self.card = LinearLayout(pygame.image.load(settings.card_lg).convert_alpha(),
                                 settings.WIDTH * 0.6, settings.HEIGHT * 0.1)
        self.inputs = pygame.sprite.Group()

        TextView(level, pygame.font.SysFont('arialblack', 28), self.card)

        if commands is None:
            for i in range(settings.commands):
                InputField(self.activate, i, f'Команда {i + 1}', self.card, self.inputs)
        else:
            for el in commands:
                InputField(lambda: None, None, el, self.card)

        self.button = TextView('Начать игру', pygame.font.SysFont('arialblack', 24), self.card)
        self.clickable = Clickable(self.on_click)
        self.card.update()

        self.active = None

    def activate(self, i):
        if self.active is not None:
            self.inputs.sprites()[self.active].set_active(False)
        self.active = i
        self.inputs.sprites()[self.active].set_active(True)

    def keyboard(self, char):
        if self.active is not None:
            sprite = self.inputs.sprites()[self.active]
            if char is None:
                if len(sprite.text) != 0:
                    sprite.set_text(sprite.text[:-1])
            else:
                sprite.set_text(sprite.text + char)

    def on_click(self):
        commands = [sprite.placeholder if sprite.text == '' else sprite.text for sprite in self.inputs.sprites()]
        self.callback(commands)

    def update(self):
        self.screen.blit(self.logo, (settings.WIDTH * 0.05, settings.HEIGHT * 0.05))
        self.clickable.update(self.button.rect)
        self.inputs.update()
        self.card.draw(self.screen)


class InputField(Button):
    def __init__(self, callback, i, placeholder, *groups):
        super().__init__(callback, i, placeholder, pygame.font.SysFont('arialblack', 20),
                         pygame.image.load(settings.card_sm), *groups)
        self.placeholder, self.text = placeholder, ''
        self.active = False

    def set_text(self, text):
        self.text = text
        super().set_text(self.placeholder if self.text == '' and not self.active else self.text)

    def set_active(self, active):
        self.active = active
        if self.text == '':
            super().set_text('' if self.active else self.placeholder)
