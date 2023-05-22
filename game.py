import pygame
import settings
from hud import Hud
from task import Task
from wheel import Wheel
from random import shuffle


class Game:
    def __init__(self, commands, data, callback, screen):
        self.data = data
        self.callback = callback
        self.screen = screen

        self.round = 0
        self.command = 0
        self.reward = None
        shuffle(commands)
        self.score = [[name, 0] for name in commands]

        self.wheel = Wheel(self.select, self.screen)

        self.task = Task(data[self.round], self.answer, self.screen)

        self.hud = Hud(self.wheel.rotate, self.screen)
        self.hud.set_round(f'Раунд {self.round + 1}')
        self.hud.set_score(self.score)
        self.hud.set_alert(f'Первый ход делает команда "{commands[0]}"')

    def select(self, option):
        if option in ('p', 'b'):
            if option == 'p':
                self.score[self.command][1] += 500
                text = f'"{self.score[self.command][0]}" + 500. '
            else:
                self.score[self.command][1] = 0
                text = f'"{self.score[self.command][0]}" теряет очки. '
            self.command = (self.command + 1) % len(self.score)
            text += f'Ход переходит "{self.score[self.command][0]}".'
            self.hud.set_alert(text)
            self.hud.set_score(self.score)
        else:
            self.reward = option

    def next(self):
        self.round += 1
        if len(self.data) == self.round:
            self.callback(self.score[self.command])
        else:
            self.hud.set_round('Финал' if len(self.data) == self.round + 1 else f'Раунд {self.round + 1}')
            self.command = 0
            self.task = Task(self.data[self.round], self.answer, self.screen)
            self.hud.callback = self.wheel.rotate
            self.hud.set_alert(f'Ходит команда "{self.score[self.command][0]}"')

    def answer(self, correct, end):
        if end:
            self.hud.callback = self.next
        if correct:
            if self.reward == '*2':
                self.score[self.command][1] *= 2
                self.hud.set_alert(f'Верно. "{self.score[self.command][0]}" удваивает очки.')
            else:
                self.score[self.command][1] += int(self.reward)
                self.hud.set_alert(f'Верно. "{self.score[self.command][0]}" +{self.reward}.')
            self.hud.set_score(self.score)
        else:
            self.command = (self.command + 1) % len(self.score)
            self.hud.set_alert(f'Неверно. Ход переходит "{self.score[self.command][0]}".')
        self.reward = None

    def update(self, tick):
        self.wheel.update(tick)
        self.task.update()
        self.hud.update()
