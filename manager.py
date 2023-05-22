import pygame
import settings
from menu import StartMenu, EndMenu
from game import Game
import json
from random import sample


class Manager:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load(settings.background)

        with open(settings.questions, 'r', encoding='utf8') as f:
            self.data = json.load(f)
        self.menu = StartMenu(self.game_start, self.screen)
        self.game = None
        self.end = None

    def menu_start(self):
        self.end = None
        self.menu = StartMenu(self.game_start, self.screen)

    def game_start(self, commands):
        self.menu = None
        self.game = Game(commands, sample(self.data, min(len(self.data), settings.rounds)), self.game_end, self.screen)

    def game_end(self, winner):
        self.game = None
        self.end = EndMenu(*winner, self.menu_start, self.screen)

    def update(self, tick):
        self.screen.blit(self.background, (0, 0))
        if self.menu is not None:
            self.menu.update()
        if self.game is not None:
            self.game.update(tick)
        if self.end is not None:
            self.end.update()

    def event(self, event):
        if event.type == pygame.KEYUP:
            if self.menu is not None:
                self.menu.keyboard(None if event.key == pygame.K_BACKSPACE else event.unicode)
            if self.game is not None:
                if pygame.K_0 <= event.key <= pygame.K_9 and self.game.reward is not None:
                    self.game.task.keyboard(event.key - pygame.K_0)
