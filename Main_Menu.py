import pygame, math, sys, time, end, main
from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((1024, 768))
while 1:
    screen.fill((0,0,0))
    for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_SPACE: 
                    main.level1()
                elif event.key == K_ESCAPE: sys.exit(0)  
    img = pygame.image.load("images/main_menu_image.png")
    screen.blit(img,(0,0))
    pygame.display.flip()
