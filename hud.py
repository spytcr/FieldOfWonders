import pygame
import settings


class Hud:
    def __init__(self, callback, screen):
        self.callback = callback
        self.screen = screen

        self.round = pygame.sprite.GroupSingle()
        TextView(36, 0, settings.HEIGHT * 0.01, self.round)

        self.score = pygame.sprite.GroupSingle()
        TextView(24, settings.WIDTH * 0.03, settings.HEIGHT * 0.1, self.score)

        self.alert = pygame.sprite.GroupSingle()
        TextView(24, 0, settings.HEIGHT * 0.8, self.alert)
        self.btn_alert = pygame.sprite.GroupSingle()
        ImageButton('Продолжить игру', self.clicked, 0, 0, self.btn_alert)
        self.btn_alert.sprite.rect.centerx = settings.WIDTH // 2
        self.active = False

    def clicked(self):
        self.active = False
        self.callback()

    def set_round(self, name):
        self.round.sprite.set_text([name])
        self.round.sprite.rect.centerx = settings.WIDTH // 2

    def set_score(self, score):
        self.score.sprite.set_text([f'{el[0]}: {el[1]}' for el in score])

    def set_alert(self, alert):
        self.alert.sprite.set_text([alert])
        self.alert.sprite.rect.centerx = settings.WIDTH // 2
        self.btn_alert.sprite.rect.y = self.alert.sprite.rect.bottom + 3
        self.active = True

    def update(self):
        self.round.draw(self.screen)
        self.score.draw(self.screen)
        if self.active:
            self.alert.draw(self.screen)
            self.btn_alert.update()
            self.btn_alert.draw(self.screen)


class TextView(pygame.sprite.Sprite):
    def __init__(self, size, x, y, group):
        super().__init__(group)
        self.font = pygame.font.SysFont('arialblack', size)
        self.x, self.y = x, y

    def set_text(self, text):
        sign = [self.font.render(el, True, pygame.Color('white')) for el in text]
        width = max(map(lambda x: x.get_width(), sign))
        height = sign[0].get_height() + 2
        self.image = pygame.Surface((width + 4, height * len(sign) + 2))
        self.image.fill(pygame.Color('royalblue'))
        for i, el in enumerate(sign):
            self.image.blit(el, ((width - el.get_width()) // 2 + 2, height * i + 2))
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class Button(pygame.sprite.Sprite):
    _clicked = False

    def __init__(self, on_click, surface, x, y, group):
        super().__init__(group)
        self.on_click = on_click
        self.image = surface
        self.rect = self.image.get_rect(x=x, y=y)

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if not Button._clicked:
                x, y = pygame.mouse.get_pos()
                if self.rect.collidepoint(x, y):
                    Button._clicked = True
                    self.on_click()
        elif Button._clicked:
            Button._clicked = False

    def set_text(self, text, size, color):
        font = pygame.font.SysFont('arialblack', size)
        sign = font.render(text, True, color)
        self.image.blit(sign, ((self.rect.w - sign.get_width()) // 2, (self.rect.h - sign.get_height()) // 2))


class ImageButton(Button):
    def __init__(self, text, on_click, x, y, group):
        surface = pygame.image.load(settings.button).convert_alpha()
        super().__init__(on_click, surface, x, y, group)
        self.set_text(text, 30, pygame.Color('white'))
