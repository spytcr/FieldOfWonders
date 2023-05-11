import pygame
import settings
from wheel import Wheel
from task import Task
from hud import ScoreManager
from random import choice


class Game:
    def __init__(self, commands, data, end, screen):
        self.data = data
        self.end = end
        self.screen = screen

        self.wheel = Wheel(self.select, self.screen)

        self.task = Task(data.pop(), self.answer, self.screen)

        self.manager = ScoreManager(commands, self.screen)

        self.reward = 0
        self.wheel.rotate()

    def select(self, option):
        if option[0] == '+':
            self.reward = int(option[1:])

    def answer(self, correct, end):
        if correct:
            self.manager.commands[self.manager.command][0] += self.reward
        self.reward = 0
        if end:
            if len(self.data) == 0:
                self.end(max(self.manager.commands))
            else:
                self.manager.command = 0
                self.task = Task(self.data.pop(), self.answer, self.screen)
        else:
            self.manager.command = (self.manager.command + 1) % len(self.manager.commands)
            self.wheel.rotate()

    def update(self, tick):
        self.wheel.update(tick)
        self.task.update()
        self.manager.update()
