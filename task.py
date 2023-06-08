import pygame
from collections import Counter
import settings
from ui import Button, Container

BOX_SIZE = 40


class Task:
    def __init__(self, data, callback, screen):
        self.callback = callback
        self.screen = screen

        self.card = TaskGroup(pygame.image.load(settings.card_md).convert_alpha(),
                              settings.WIDTH * 0.75, settings.HEIGHT * 0.1)
        for i, text in enumerate(data['expressions']):
            for char in text:
                TaskSprite(self.on_click, char, i, self.card)

        self.answers = data['answers']
        self.selected = None

    def on_click(self, char):
        if char in self.answers.keys():
            self.selected = char
            self.select()

    def open(self, char):
        end = True
        for box in self.card.sprites():
            if box.char == char:
                box.set_text(str(self.answers[char]))
            elif end and box.char in self.answers.keys():
                end = False
        return end

    def select(self):
        for box in self.card.sprites():
            box.set_active(self.selected is not None and box.char == self.selected)

    def keyboard(self, key):
        if self.selected is not None:
            if self.answers[self.selected] == key:
                self.callback(True, self.open(self.selected))
            else:
                self.callback(False, False)
            self.selected = None
            self.select()

    def update(self):
        self.card.update()
        self.card.draw(self.screen)


class TaskSprite(Button):
    def __init__(self, callback, char, layer, *groups):
        self.active = False
        super().__init__(callback, char, char, pygame.font.SysFont('arialblack', 30),
                         pygame.Surface((BOX_SIZE, BOX_SIZE)), *groups)
        self.char = char
        self._layer = layer

    def draw(self):
        self.image.fill(pygame.Color('lightgray' if self.active else 'white'))
        pygame.draw.rect(self.image, pygame.Color('black'), (0, 0, BOX_SIZE, BOX_SIZE), 1)
        super().draw()

    def set_active(self, active):
        if self.active != active:
            self.active = active
            self.draw()

    def set_text(self, text):
        super().set_text(text)
        self.char = text


class TaskGroup(Container):
    def calc(self):
        count = Counter([sprite.layer for sprite in self.sprites()])
        x = self.sprite.rect.x + (self.sprite.rect.w + max(count.values()) * BOX_SIZE) // 2
        y = self.sprite.rect.y + (self.sprite.rect.h - len(count) * (BOX_SIZE + 4)) // 2
        for sprite in self.sprites():
            sprite.rect.x = x - count[sprite.layer] * BOX_SIZE
            sprite.rect.y = y + sprite.layer * (BOX_SIZE + 4) + (4 if sprite.layer == len(count) - 1 else 0)
            count[sprite.layer] -= 1

        # Draw plus and line
        self.sprite.redraw()
        ly = (self.sprite.rect.h + len(count) * (BOX_SIZE + 4)) // 2 - BOX_SIZE - 5
        pygame.draw.line(self.sprite.image, pygame.Color('black'),
                         (self.sprite.rect.w * 0.05, ly), (self.sprite.rect.w * 0.95, ly), 2)
        cx, cy = self.sprite.rect.w * 0.05, (self.sprite.rect.h + BOX_SIZE + 4) // 2 - BOX_SIZE - 5
        pygame.draw.line(self.sprite.image, pygame.Color('black'), (cx + 10, cy - 10), (cx + 10, cy + 10), 2)
        pygame.draw.line(self.sprite.image, pygame.Color('black'), (cx, cy), (cx + 20, cy), 2)
