#initialize the screen
import pygame, math, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1024, 768))
#GAME CLOCK
clock = pygame.time.Clock()
font = pygame.font.Font(None, 75)
win_condition = None

class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 10
    ACCELERATION = 2
    TURN_SPEED = 10

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
    
    def update(self, deltat):
        #SIMULATION
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < -self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED
        self.direction += (self.k_right + self.k_left)
        x, y = (self.position)
        rad = self.direction * math.pi / 180
        x += -self.speed*math.sin(rad)
        y += -self.speed*math.cos(rad)
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

class PadSprite(pygame.sprite.Sprite):
    normal = pygame.image.load('race_pads.png')
    hit = pygame.image.load('collision.png')
    def __init__(self, position):
        super(PadSprite, self).__init__()
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
    def update(self, hit_list):
        if self in hit_list: self.image = self.hit
        else: self.image = self.normal
pads = [
    PadSprite((0, 10)),
    PadSprite((600, 10)),
    PadSprite((1100, 10)),
    PadSprite((100, 150)),
    PadSprite((600, 150)),
    PadSprite((200, 300)),
    PadSprite((800, 300)),
    PadSprite((300, 450)),
    PadSprite((700, 450)),
    PadSprite((200, 600)),
    PadSprite((900, 600)),
    PadSprite((400, 750)),
    PadSprite((800, 750)),
]
pad_group = pygame.sprite.RenderPlain(*pads)

class Trophy(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('trophy.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
    def draw(self, screen):
        screen.blit(self.image, self.rect)

trophies = [Trophy((285,0))]
trophy_group = pygame.sprite.RenderPlain(*trophies)


# trophy = Trophy((300, 300), 'trophy.png')
# trophy_group = pygame.sprite.RenderPlain(trophy)
#ATTEMPT TO CREATE A PAD RECT


# CREATE A CAR AND RUN
rect = screen.get_rect()
car = CarSprite('car.png', (10, 730))
car_group = pygame.sprite.RenderPlain(car)

while win_condition == None:
    #USER INPUT
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN  
        if event.key == K_RIGHT: car.k_right = down * -5
        elif event.key == K_LEFT: car.k_left = down * 5
        elif event.key == K_UP: car.k_up = down * 2
        elif event.key == K_DOWN: car.k_down = down * -2 
        elif event.key == K_ESCAPE: sys.exit(0) # quit the game
    
    #COUNTDOWN TIMER
    seconds = (20000 - pygame.time.get_ticks())/1000
    timer_text = font.render(str(seconds), True, (255,255,0))
    if seconds <= 0:
        seconds = 0
        timer_text = font.render("You Lose!", True, (255,0,0))
 
    #RENDERING
    screen.fill((0,0,0))
    car_group.update(deltat)
    collisions = pygame.sprite.groupcollide(car_group, pad_group, False, False, collided = None)
    if collisions != {}:
        timer_text = font.render("You Lose!", True, (255,0,0))
        car.MAX_FORWARD_SPEED = 0
        car.MAX_REVERSE_SPEED = 0
        win_condition = False

    trophy_collision = pygame.sprite.groupcollide(car_group, trophy_group, False, True)
    if trophy_collision != {}:
        timer_text = font.render("You Win!", True, (0,255,0))
        car.MAX_FORWARD_SPEED = 0
        car.MAX_REVERSE_SPEED = 0
        car.TURN_SPEED = 0
        win_condition = True
        
        
    pad_group.update(collisions)
    pad_group.draw(screen)
    car_group.draw(screen)
    trophy_group.draw(screen)
    #Counter Render
    screen.blit(timer_text, (30,60))
    pygame.display.flip()

else:
    if win_condition == True:
        print "got to line 140"
        timer_text = font.render("You Win!", True, (0,255,0))
        car.MAX_FORWARD_SPEED = 0
        car.MAX_REVERSE_SPEED = 0
        car.TURN_SPEED = 0
        pad_group.update(collisions)
        pad_group.draw(screen)
        car_group.draw(screen)
        trophy_group.draw(screen)
        #Counter Render
        screen.blit(timer_text, (30,60))
        pygame.display.flip()
    else:
        print "got to line 146"
        timer_text = font.render("You Lose!", True, (255,0,0))
        pad_group.update(collisions)
        pad_group.draw(screen)
        car_group.draw(screen)
        trophy_group.draw(screen)
        #Counter Render
        screen.blit(timer_text, (30,60))
        pygame.display.flip()

