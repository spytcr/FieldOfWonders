from hud import Hud
from task import Task
from wheel import Wheel


class Game:
    def __init__(self, score, data, callback, sound, screen):
        self.score = score
        self.data = data
        self.callback = callback
        self.sound = sound
        self.screen = screen

        self.command = 0
        self.reward = None

        self.wheel = Wheel(self.select, self.screen)
        self.task = Task(data, self.answer, self.screen)
        self.hud = Hud(self.rotate, self.screen)
        self.update_score()
        self.hud.set_text(self.hud.button, ['Вращайте', 'барабан'])

    def update_score(self):
        text = ['Счет'] + [f'{el[0]}: {el[1]}' for el in self.score]
        self.hud.set_text(self.hud.score, text, active=self.command + 1)

    def rotate(self):
        self.sound.spin.play(-1)
        self.wheel.wheel.sprite.rotate()

    def select(self, option):
        self.sound.spin.stop()
        if option in ('b', 'p', '0'):
            if option == 'b':
                self.sound.option_b.play()
                self.score[self.command][1] = 0
                t = self.score[self.command][0]
                self.command = (self.command + 1) % len(self.score)
                self.hud.set_text(self.hud.alert,
                                  [f'"{t}"', 'теряет очки', 'Ход переходит',  f'"{self.score[self.command][0]}"'])
                self.update_score()
                self.hud.active = True
            elif option == '0':
                self.sound.option_0.play()
                self.command = (self.command + 1) % len(self.score)
                self.hud.set_text(self.hud.alert,
                                  ['Ход переходит', 'команде', f'"{self.score[self.command][0]}"'])
                self.update_score()
                self.hud.active = True
            elif option == 'p':
                def callback(get):
                    if get and len(self.score) > 1:
                        self.hud.set_text(self.hud.alert,
                                          ['Команда', f'"{self.score[self.command][0]}"', 'выбывает'])
                        del self.score[self.command]
                        self.command %= len(self.score)
                    else:
                        self.hud.set_text(self.hud.alert,
                                          ['Команда', f'"{self.score[self.command][0]}"', 'получает 500 очков'])
                        self.score[self.command][1] += 500
                    self.hud.prize = None
                    self.update_score()
                    self.hud.active = True
                self.sound.option_p.play()
                self.hud.set_prize(callback)
        else:
            self.hud.set_text(self.hud.alert, ['Сектор', f'"{option}"', 'на барабане.'])
            self.reward = option

    def answer(self, correct, end):
        self.hud.active = True
        if end:
            self.hud.set_text(self.hud.button, ['Продолжить', 'игру'])
            self.hud.clickable.on_click = lambda: self.callback(self.score[self.command])
            self.sound.end.play()
        if correct:
            self.sound.correct.play()
            if self.reward == '*2':
                self.sound.option_x2.play()
                self.hud.set_text(self.hud.alert,
                                  ['Верно.', 'Команда', f'"{self.score[self.command][0]}"', 'удваивает очки'])
                self.score[self.command][1] *= 2
            else:
                self.hud.set_text(self.hud.alert,
                                  ['Верно.', 'Команда', f'"{self.score[self.command][0]}"', f'+{self.reward}'])
                self.score[self.command][1] += int(self.reward)
        else:
            self.sound.incorrect.play()
            self.command = (self.command + 1) % len(self.score)
            self.hud.set_text(self.hud.alert,
                              ['Неверно.', 'Ход переходит', 'команде', f'"{self.score[self.command][0]}"'])
        self.update_score()
        self.reward = None

    def update(self, tick):
        self.wheel.update(tick)
        self.task.update()
        self.hud.update()
