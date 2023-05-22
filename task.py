import pygame
import settings
from hud import Button

BOX_SIZE = 40


class Task:
    def __init__(self, data, answer, screen):
        self.answer = answer
        self.screen = screen

        self.boxes = pygame.sprite.Group()
        self.x, self.xn = settings.WIDTH * 0.97, max(map(len, data['expressions']))
        self.y, self.yn = settings.HEIGHT * 0.1, len(data['expressions'])
        for i, text in enumerate(data['expressions']):
            for j, char in enumerate(text):
                TaskSprite(char, self.callback, self.x - BOX_SIZE * (len(text) - j),
                           self.y + i * (BOX_SIZE + (2 if i != self.yn - 1 else 4)), self.boxes)

        self.answers = data['answers']
        self.selected = None

    def callback(self, char):
        if char in self.answers.keys():
            self.selected = char
            self.select()

    def open(self, char):
        end = True
        for box in self.boxes.sprites():
            if box.char == char:
                box.char = str(self.answers[char])
            elif end and box.char in self.answers.keys():
                end = False
        return end

    def select(self):
        for box in self.boxes.sprites():
            box.active = self.selected is not None and box.char == self.selected

    def keyboard(self, key):
        if self.selected is not None:
            if self.answers[self.selected] == key:
                self.answer(True, self.open(self.selected))
            else:
                self.answer(False, False)
            self.selected = None
            self.select()

    def update(self):
        pygame.draw.rect(self.screen, pygame.Color('royalblue'),
                         (self.x - self.xn * BOX_SIZE - 24, self.y - 4,
                          self.xn * BOX_SIZE + 28, self.yn * (BOX_SIZE + 2) + 12), 0)
        self.boxes.update()
        self.boxes.draw(self.screen)
        cx, cy = self.x - self.xn * BOX_SIZE - 21, self.y + (self.yn - 1) / 2 * (BOX_SIZE + 2) - 11
        pygame.draw.line(self.screen, pygame.Color('white'), (cx + 10, cy), (cx + 10, cy + 20), 2)
        pygame.draw.line(self.screen, pygame.Color('white'), (cx, cy + 10), (cx + 20, cy + 10), 2)
        ly = self.y + (self.yn - 1) * (BOX_SIZE + 2)
        pygame.draw.line(self.screen, pygame.Color('white'), (cx, ly), (self.x, ly), 2)


class TaskSprite(Button):
    def __init__(self, char, callback, x, y, group):
        super().__init__(lambda: callback(self.char), pygame.Surface((BOX_SIZE, BOX_SIZE)), x, y, group)
        self.char = char
        self.active = False

    def update(self):
        super().update()
        self.image.fill(pygame.Color('dodgerblue4' if self.active else 'dodgerblue'))
        pygame.draw.rect(self.image, pygame.Color('white'), (0, 0, BOX_SIZE, BOX_SIZE), 1)
        self.set_text(self.char, 28, 'white')
