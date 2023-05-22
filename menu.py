import pygame
import settings
from hud import Button, ImageButton, TextView

INPUT_W, INPUT_H = 400, 50


class StartMenu:
    def __init__(self, start, screen):
        self.start = start
        self.screen = screen

        self.inputs = pygame.sprite.Group()
        x, y = (settings.WIDTH - INPUT_W) // 2, (settings.HEIGHT - settings.commands * (INPUT_H + 20)) // 2
        for i in range(settings.commands):
            InputField(f'Название команды {i + 1}', i, self.activate, x, y + i * (INPUT_H + 20), self.inputs)

        self.text = pygame.sprite.GroupSingle()
        TextView(36, 0, 0, self.text)
        self.text.sprite.set_text(['Поле математических', 'чудес'])
        self.text.sprite.rect.centerx, self.text.sprite.rect.bottom = settings.WIDTH // 2, y - 20

        self.button = pygame.sprite.GroupSingle()
        ImageButton('Начать игру', self.callback, 0,
                    (settings.HEIGHT + settings.commands * (INPUT_H + 20)) // 2, self.button)
        self.button.sprite.rect.centerx = settings.WIDTH // 2

        self.active = None

    def activate(self, i):
        if self.active is not None:
            self.inputs.sprites()[self.active].active = False
        self.active = i
        self.inputs.sprites()[self.active].active = True

    def keyboard(self, char):
        if self.active is not None:
            if char is None:
                if len(self.inputs.sprites()[self.active].text) != 0:
                    self.inputs.sprites()[self.active].text = self.inputs.sprites()[self.active].text[:-1]
            else:
                self.inputs.sprites()[self.active].text += char

    def callback(self):
        commands = [inp.text for inp in self.inputs.sprites()]
        self.start(commands)

    def update(self):
        self.inputs.update()
        self.inputs.draw(self.screen)
        self.text.draw(self.screen)
        self.button.update()
        self.button.draw(self.screen)


class InputField(Button):
    def __init__(self, placeholder, i, callback, x, y, group):
        super().__init__(lambda: callback(self.i), pygame.Surface((INPUT_W, INPUT_H)), x, y, group)
        self.placeholder = placeholder
        self.i = i
        self.active = False
        self.text = ''

    def update(self):
        super().update()
        self.image.fill(pygame.Color('lightgray' if self.active else 'white'))
        pygame.draw.rect(self.image, pygame.Color('black'), (0, 0, INPUT_W, INPUT_H), 2)
        if not self.active and self.text == '':
            self.set_text(self.placeholder, 18, pygame.Color('gray'))
        else:
            self.set_text(self.text, 20, pygame.Color('black'))


class EndMenu:
    def __init__(self, command, score, start, screen):
        self.start = start
        self.screen = screen

        self.text = pygame.sprite.GroupSingle()
        TextView(40, 0, settings.HEIGHT * 0.3, self.text)
        self.text.sprite.set_text([f'Победила команда "{command}"', f'Со счетом {score}', 'Поздравляем!'])
        self.text.sprite.rect.centerx = settings.WIDTH // 2

        self.button = pygame.sprite.GroupSingle()
        ImageButton('В главное меню', self.start, 0, self.text.sprite.rect.bottom + 15, self.button)
        self.button.sprite.rect.centerx = settings.WIDTH // 2

    def update(self):
        self.text.draw(self.screen)
        self.button.update()
        self.button.draw(self.screen)
