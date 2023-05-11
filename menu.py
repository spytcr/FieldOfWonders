import pygame
import settings
from hud import Button

INPUT_W, INPUT_H = 450, 50


class StartMenu:
    def __init__(self, start, screen):
        self.start = start
        self.screen = screen

        font = pygame.font.SysFont('arialblack', 44)
        self.sign = font.render('Поле чудес', True, pygame.Color('white'))

        self.inputs = pygame.sprite.Group()
        x, self.y = (settings.WIDTH - INPUT_W) // 2, (settings.HEIGHT - settings.commands * (INPUT_H + 20)) // 2
        for i in range(settings.commands):
            InputField(f'Название команды {i + 1}', i, self.activate, x, self.y + i * (INPUT_H + 20), self.inputs)

        self.button = pygame.sprite.GroupSingle()
        surface = pygame.image.load(settings.button).convert_alpha()
        Button(self.callback, surface, (settings.WIDTH - surface.get_width()) // 2,
               (settings.HEIGHT + settings.commands * (INPUT_H + 20)) // 2, self.button)
        self.button.sprite.set_text('Начать игру', 30, pygame.Color('white'))

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
        self.screen.blit(self.sign, ((settings.WIDTH - self.sign.get_width()) // 2,
                                     self.y - self.sign.get_height() // 2 - 60))
        self.inputs.update()
        self.inputs.draw(self.screen)
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
    def __init__(self, winner, start, screen):
        self.start = start
        self.screen = screen
        font = pygame.font.SysFont('arial', 40)
        self.sign1 = font.render(f'Победила команда "{winner[1]}"', True, pygame.Color('white'))
        self.sign2 = font.render(f'Со счетом {winner[0]}', True, pygame.Color('white'))
        self.button = pygame.sprite.GroupSingle()
        surface = pygame.image.load(settings.button).convert_alpha()
        Button(self.start, surface, (settings.WIDTH - surface.get_width()) // 2, settings.HEIGHT // 2, self.button)
        self.button.sprite.set_text('Назад', 30, pygame.Color('white'))

    def update(self):
        self.screen.blit(self.sign1, ((settings.WIDTH - self.sign1.get_width()) // 2,
                                      (settings.HEIGHT - self.sign1.get_height() - self.sign2.get_height()) // 2 - 60))
        self.screen.blit(self.sign2, ((settings.WIDTH - self.sign2.get_width()) // 2,
                                      (settings.HEIGHT - self.sign2.get_height()) // 2 - 40))
        self.button.update()
        self.button.draw(self.screen)
