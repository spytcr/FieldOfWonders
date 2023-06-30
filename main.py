import sys, os
import pygame
import settings
from manager import Manager


if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

pygame.init()
pygame.display.set_caption('Поле математических чудес')
pygame.display.set_icon(pygame.image.load(settings.wheel))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
settings.k = screen.get_width() / 1920
clock = pygame.time.Clock()
running = True
game = Manager(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            running = False
        else:
            game.event(event)
    screen.fill(0)
    game.update(clock.tick())
    pygame.display.flip()
pygame.quit()
