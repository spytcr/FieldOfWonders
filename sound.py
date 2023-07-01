import pygame
import settings


class SoundManager:
    def __init__(self):
        self.winner = pygame.mixer.Sound(settings.sound + 'winner.mp3')
        self.start = pygame.mixer.Sound(settings.sound + 'start.mp3')
        self.end = pygame.mixer.Sound(settings.sound + 'end.mp3')
        self.spin = pygame.mixer.Sound(settings.sound + 'spin.mp3')
        self.correct = pygame.mixer.Sound(settings.sound + 'correct.mp3')
        self.incorrect = pygame.mixer.Sound(settings.sound + 'incorrect.mp3')
        self.option_p = pygame.mixer.Sound(settings.sound + 'option_p.mp3')
        self.option_b = pygame.mixer.Sound(settings.sound + 'option_b.mp3')
        self.option_0 = pygame.mixer.Sound(settings.sound + 'option_0.mp3')
        self.option_x2 = pygame.mixer.Sound(settings.sound + 'option_x2.mp3')
