import pygame
import settings
from hud import Button

BOX_SIZE = 35


class Task:
    def __init__(self, data, answer, screen):
        self.answer = answer
        self.screen = screen

        self.boxes = pygame.sprite.Group()
        sizes = (len(data['first']), len(data['second']), len(data['sum']))
        self.x = (settings.WIDTH + max(sizes) * BOX_SIZE) // 2
        self.y = settings.HEIGHT * 0.7
        self.add(data['first'], self.x - sizes[0] * BOX_SIZE, self.y)
        self.add(data['second'], self.x - sizes[1] * BOX_SIZE, self.y + BOX_SIZE + 5)
        self.add(data['sum'], self.x - sizes[2] * BOX_SIZE, self.y + 2 * BOX_SIZE + 15)

        self.answers = data['answers']
        self.selected = None

    def add(self, text, x, y):
        for i, char in enumerate(text):
            TaskSprite(char, self.callback, x + (i * BOX_SIZE), y, self.boxes)

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
        self.boxes.update()
        self.boxes.draw(self.screen)
        cx, cy = settings.WIDTH - self.x + 10, self.y + BOX_SIZE - 10
        pygame.draw.line(self.screen, pygame.Color('white'), (cx + 10, cy), (cx + 10, cy + 20), 2)
        pygame.draw.line(self.screen, pygame.Color('white'), (cx, cy + 10), (cx + 20, cy + 10), 2)
        ly = self.y + 2 * BOX_SIZE + 10
        pygame.draw.line(self.screen, pygame.Color('white'), (settings.WIDTH - self.x, ly), (self.x, ly), 2)


class TaskSprite(Button):
    def __init__(self, char, callback, x, y, group):
        super().__init__(lambda: callback(self.char), pygame.Surface((BOX_SIZE, BOX_SIZE)), x, y, group)
        self.char = char
        self.active = False

    def update(self):
        super().update()
        self.image.fill(pygame.Color('dodgerblue4' if self.active else 'dodgerblue'))
        pygame.draw.rect(self.image, pygame.Color('white'), (0, 0, BOX_SIZE, BOX_SIZE), 1)
        self.set_text(self.char, 22, 'white')
