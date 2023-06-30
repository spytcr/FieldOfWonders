import pygame
import settings
from ui import Button, TextView, ClickableText, LinearLayout, load, font


class Menu:
    def __init__(self, callback, screen):
        self.callback = callback
        self.screen = screen

        self.logo = load(settings.logo)

        self.card = LinearLayout(load(settings.card_lg), screen.get_width() * 0.62, screen.get_height() * 0.2)

    def update(self):
        self.screen.blit(self.logo, (self.screen.get_width() * 0.02, self.screen.get_height() * 0.06))
        self.card.draw(self.screen)


class StartMenu(Menu):
    def __init__(self, level, callback, screen, commands=None):
        super().__init__(callback, screen)
        self.inputs = pygame.sprite.Group()

        TextView(level, font(45), self.card)

        if commands is None:
            for i in range(settings.commands):
                InputField(self.activate, i, f'Команда {i + 1}', self.card, self.inputs)
        else:
            for el in commands:
                InputField(lambda: None, None, el, self.card)

        self.button = ClickableText('Начать игру', font(40), self.on_click, self.card)
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
        super().update()
        self.button.update()
        self.inputs.update()


class EndMenu(Menu):
    def __init__(self, winner, callback, screen):
        super().__init__(callback, screen)
        for el in ['Победила команда', f'"{winner[0]}"', 'со счетом', f'{winner[1]}']:
            TextView(el, font(40), self.card)
        self.card.update()

    def keyboard(self, char):
        self.callback()


class InputField(Button):
    def __init__(self, callback, i, placeholder, *groups):
        super().__init__(callback, i, placeholder, font(36), load(settings.card_sm), *groups)
        self.placeholder, self.text = placeholder, ''
        self.active = False

    def set_text(self, text):
        self.text = text
        super().set_text(self.placeholder if self.text == '' and not self.active else self.text)

    def set_active(self, active):
        self.active = active
        if self.text == '':
            super().set_text('' if self.active else self.placeholder)
