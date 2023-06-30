from hud import Hud
from task import Task
from wheel import Wheel


class Game:
    def __init__(self, score, data, callback, screen):
        self.score = score
        self.data = data
        self.callback = callback
        self.screen = screen

        self.command = 0
        self.reward = None

        self.wheel = Wheel(self.select, self.screen)
        self.task = Task(data, self.answer, self.screen)
        self.hud = Hud(self.wheel.rotate, self.screen)
        self.update_score()
        self.hud.set_text(self.hud.button, ['Вращайте', 'барабан'])

    def update_score(self):
        text = ['Счет'] + [f'{el[0]}: {el[1]}' for el in self.score]
        self.hud.set_text(self.hud.score, text)

    def select(self, option):
        if option in ('b', 'p'):
            if option == 'b':
                self.score[self.command][1] = 0
                t = self.score[self.command][0]
                self.command = (self.command + 1) % len(self.score)
                self.hud.set_text(self.hud.alert,
                                  [f'"{t}"', 'теряет очки', 'Ход переходит',  f'"{self.score[self.command][0]}"'])
                self.update_score()
            elif option == 'p':
                def callback(get):
                    if get:
                        self.hud.set_text(self.hud.alert,
                                          ['Команда', f'"{self.score[self.command][0]}"', 'выбывает'])
                        del self.score[self.command]
                        self.command %= len(self.score)
                    else:
                        self.hud.set_text(self.hud.alert,
                                          ['Команда', f'"{self.score[self.command][0]}"', 'получает 500 очков'])
                        self.score[self.command][1] += 500
                    self.update_score()
                    self.hud.prize = None
                self.hud.set_prize(callback)
            self.hud.active = True
        else:
            self.hud.set_text(self.hud.alert, ['Сектор', f'"{option}"', 'на барабане.'])
            self.reward = option

    def answer(self, correct, end):
        self.hud.active = True
        if end:
            self.hud.set_text(self.hud.button, ['Продолжить', 'игру'])
            self.hud.clickable.on_click = lambda: self.callback(self.score[self.command])
        if correct:
            if self.reward == '*2':
                self.hud.set_text(self.hud.alert,
                                  ['Верно.', 'Команда', f'"{self.score[self.command][0]}"', 'удваивает очки'])
                self.score[self.command][1] *= 2
            else:
                self.hud.set_text(self.hud.alert,
                                  ['Верно.', 'Команда', f'"{self.score[self.command][0]}"', f'+{self.reward}'])
                self.score[self.command][1] += int(self.reward)
            self.update_score()
        else:
            self.command = (self.command + 1) % len(self.score)
            self.hud.set_text(self.hud.alert,
                              ['Неверно.', 'Ход переходит', 'команде', f'"{self.score[self.command][0]}"'])
        self.reward = None

    def update(self, tick):
        self.wheel.update(tick)
        self.task.update()
        self.hud.update()
