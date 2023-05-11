import sys, os
import pygame
import settings
from manager import Manager


if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
running = True
game = Manager(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            game.event(event)
    screen.fill(0)
    game.update(clock.tick())
    pygame.display.flip()
pygame.quit()
