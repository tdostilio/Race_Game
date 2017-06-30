import pygame, sys, math
from pygame.locals import *


def end_game():
    while 1:
        pygame.init()
        screen = pygame.display.set_mode((1024, 768))
        win_font = pygame.font.Font(None, 70)
        win_text = win_font.render('Congratulations! Thanks for Playing!', True, (0,255,0))
        screen.blit(win_text, (60, 384))
        pygame.display.flip()
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            if event.key == K_ESCAPE: sys.exit(0) # quit the game

