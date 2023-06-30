import pygame
from abc import abstractmethod
import settings


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, *groups):
        super().__init__(*groups)
        self.surface = image
        self.rect = self.surface.get_rect()
        self.redraw()

    def redraw(self):
        self.image = self.surface.copy()


class TextView(pygame.sprite.Sprite):
    def __init__(self, text, font, *groups):
        super().__init__(*groups)
        self.font = font
        self.set_text(text)

    def set_text(self, text):
        sing = self.font.render(text, True, pygame.Color('black'))
        self.image = sing
        self.rect = self.image.get_rect()


class Clickable:
    _clicked = False

    def __init__(self, on_click, *args):
        self.on_click = on_click
        self.args = args

    def update(self, rect):
        if pygame.mouse.get_pressed()[0]:
            if not Clickable._clicked:
                x, y = pygame.mouse.get_pos()
                if rect.collidepoint(x, y):
                    Clickable._clicked = True
                    self.on_click(*self.args)
        elif Clickable._clicked:
            Clickable._clicked = False


class ClickableText(TextView):
    def __init__(self, text, font, on_click, *groups):
        super().__init__(text, font, *groups)
        self.clickable = Clickable(on_click)

    def update(self):
        self.clickable.update(self.rect)


class Button(Sprite):
    def __init__(self, on_click, i, text, font, image, *groups):
        super().__init__(image, *groups)
        self.i = i
        self.clickable = Clickable(on_click, self.i)
        self.sign = TextView(text, font)
        self.view = pygame.sprite.GroupSingle(self.sign)
        self.draw()

    def draw(self):
        self.sign.rect.center = self.rect.w // 2, self.rect.h // 2
        self.view.draw(self.image)

    def set_text(self, text):
        self.sign.set_text(text)
        self.redraw()
        self.draw()

    def update(self):
        self.clickable.update(self.rect)


class Container(pygame.sprite.Group):
    def __init__(self, image, x, y):
        super().__init__()
        self.background = pygame.sprite.GroupSingle()
        self.sprite = Sprite(image, self.background)
        self.sprite.rect.x, self.sprite.rect.y = x, y

    @abstractmethod
    def calc(self):
        return

    def update(self):
        super().update()
        self.calc()

    def draw(self, surface):
        self.background.draw(surface)
        super().draw(surface)


class LinearLayout(Container):
    def calc(self):
        y = self.sprite.rect.y + (self.sprite.rect.h - sum(map(lambda x: x.rect.h + 8, self.sprites())) - 8) // 2
        for sprite in self.sprites():
            sprite.rect.centerx, sprite.rect.y = self.sprite.rect.centerx, y
            y += sprite.rect.h + 8


def load(path):
    image = pygame.image.load(path).convert_alpha()
    w, h = image.get_size()
    image = pygame.transform.scale(image, (settings.k * w, settings.k * h))
    return image


def font(size):
    return pygame.font.SysFont('arialblack', int(settings.k * size))
