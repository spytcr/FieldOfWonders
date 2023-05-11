import pygame


class ScoreManager:
    def __init__(self, commands, screen):
        self.commands = tuple([0, name] for name in commands)
        self.command = 0
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 28)

    def update(self):
        x, y = 25, 25
        for i in range(len(self.commands)):
            sign = self.font.render(f'{self.commands[i][1]}: {self.commands[i][0]}', True,
                                    pygame.Color('green' if i == self.command else 'white'))
            self.screen.blit(sign, (x, y + i * 35))


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
