import pygame
import json
import settings
from game import Game
from menu import StartMenu, EndMenu


class Manager:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load(settings.background), screen.get_size())

        with open(settings.questions, 'r', encoding='utf8') as f:
            self.data = json.load(f)
        self.round = 0
        self.winners = [[] for _ in range(len(self.data) - 1)]

        self.menu = None
        self.game = None
        self.menu_start()

    def menu_start(self):
        self.game = None
        self.round += 1
        if self.round == len(self.data):
            self.menu = StartMenu('Финал', self.game_start, self.screen, commands=[el[0] for el in self.winners])
        else:
            self.menu = StartMenu(f'Раунд {self.round}', self.game_start, self.screen)

    def game_start(self, commands):
        self.menu = None
        self.game = Game(self.winners if self.round == len(self.data) else [[el, 0] for el in commands],
                         self.data[self.round - 1], self.game_end, self.screen)

    def game_end(self, winner):
        if self.round == len(self.data):
            self.round = 0
            self.game = None
            self.menu = EndMenu(winner, self.menu_start, self.screen)
        else:
            self.winners[self.round - 1] = winner
            self.menu_start()

    def update(self, tick):
        self.screen.blit(self.background, (0, 0))
        if self.menu is not None:
            self.menu.update()
        if self.game is not None:
            self.game.update(tick)

    def event(self, event):
        if event.type == pygame.KEYUP:
            if self.menu is not None:
                self.menu.keyboard(None if event.key == pygame.K_BACKSPACE else event.unicode)
            if self.game is not None:
                if pygame.K_0 <= event.key <= pygame.K_9 and self.game.reward is not None:
                    self.game.task.keyboard(event.key - pygame.K_0)
