#initialize the screen
import pygame, math, sys, time, level3
from pygame.locals import *

def level2():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    #GAME CLOCK
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 75)
    win_condition = None
    pygame.mixer.music.load('My_Life_Be_Like.mp3')
    win_font = pygame.font.Font(None, 50)
    win_condition = None
    win_text = font.render('', True, (0, 255, 0))
    loss_text = font.render('', True, (255, 0, 0))
    t0 = time.time()



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
        normal = pygame.image.load('images/vertical_pads.png')
        def __init__(self, position):
            super(PadSprite, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = position
            self.image = self.normal

    class HorizontalPad(pygame.sprite.Sprite):
        normal = pygame.image.load('images/race_pads.png')
        def __init__(self, position):
            super(HorizontalPad, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = position
            self.image = self.normal

    class SmallHorizontalPad(pygame.sprite.Sprite):
        normal = pygame.image.load('images/small_horizontal.png')
        def __init__(self, position):
            super(SmallHorizontalPad, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = position
            self.image = self.normal

    class SmallVerticalPad(pygame.sprite.Sprite):
        normal = pygame.image.load('images/small_vertical.png')
        def __init__(self, position):
            super(SmallVerticalPad, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = position
            self.image = self.normal        

    #level design
    pads = [
        PadSprite((0, 200)),
        PadSprite((0, 400)),
        HorizontalPad((60, 0)),
        HorizontalPad((300, 0)),
        HorizontalPad((700, 0)),
        HorizontalPad((900, 0)),
        PadSprite((1024, 100)),
        PadSprite((1024, 550)),
        HorizontalPad((1024, 768)),
        HorizontalPad((624, 768)),
        HorizontalPad((224, 768)),
        PadSprite((200, 768)),
        PadSprite((200, 368)),
        HorizontalPad((450, 130)),
        HorizontalPad((550, 130)),
        PadSprite((800, 375)),
        SmallHorizontalPad((670, 615)),
        SmallHorizontalPad((470, 615)),
        SmallVerticalPad((350, 490)),
        SmallVerticalPad((350, 390)),
        SmallHorizontalPad((470, 270)),
        SmallVerticalPad((600, 390))
        # PadSprite((200, 368))
    
    
    ]
    pad_group = pygame.sprite.RenderPlain(*pads)

    class Trophy(pygame.sprite.Sprite):
        def __init__(self, position):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('images/trophy.png')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = position
        def draw(self, screen):
            screen.blit(self.image, self.rect)

    trophies = [Trophy((450,320))]
    trophy_group = pygame.sprite.RenderPlain(*trophies)

    # CREATE A CAR AND RUN
    rect = screen.get_rect()
    car = CarSprite('images/car.png', (30, 730))
    car_group = pygame.sprite.RenderPlain(car)

    #THE GAME LOOP
    while 1:
        t1 = time.time()
        dt = t1-t0
        #USER INPUT
        deltat = clock.tick(30)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN  
            if win_condition == None: 
                if event.key == K_RIGHT: car.k_right = down * -5 
                elif event.key == K_LEFT: car.k_left = down * 5
                elif event.key == K_UP: car.k_up = down * 2
                elif event.key == K_DOWN: car.k_down = down * -2 
                elif event.key == K_ESCAPE: sys.exit(0) # quit the game
            elif win_condition == True and event.key == K_SPACE: level3.level3()
            elif win_condition == False and event.key == K_SPACE: 
                level2()
                t0 = t1
            elif event.key == K_ESCAPE: sys.exit(0)    
        
        #COUNTDOWN TIMER
        seconds = round((20 - dt),2)
        if win_condition == None:
            timer_text = font.render(str(seconds), True, (255,255,0))
            if seconds <= 0:
                win_condition = False
                timer_text = font.render("Time!", True, (255,0,0))
                loss_text = win_font.render('Press Space to Retry', True, (255,0,0))
            
    
        #RENDERING
        screen.fill((0,0,0))
        car_group.update(deltat)
        collisions = pygame.sprite.groupcollide(car_group, pad_group, False, False, collided = None)
        if collisions != {}:
            win_condition = False
            timer_text = font.render("Crash!", True, (255,0,0))
            car.image = pygame.image.load('images/collision.png')
            loss_text = win_font.render('Press Space to Retry', True, (255,0,0))
            seconds = 0
            car.MAX_FORWARD_SPEED = 0
            car.MAX_REVERSE_SPEED = 0
            car.k_right = 0
            car.k_left = 0

        trophy_collision = pygame.sprite.groupcollide(car_group, trophy_group, False, True)
        if trophy_collision != {}:
            seconds = seconds
            timer_text = font.render("Finished!", True, (0,255,0))
            win_condition = True
            car.MAX_FORWARD_SPEED = 0
            car.MAX_REVERSE_SPEED = 0
            pygame.mixer.music.play(loops=0, start=0.0)
            win_text = win_font.render('Press Space to Advance', True, (0,255,0))
            if win_condition == True:
                car.k_right = -5

        pad_group.draw(screen)
        car_group.draw(screen)
        trophy_group.draw(screen)
        #Counter Render
        screen.blit(timer_text, (20,20))
        screen.blit(win_text, (250, 700))
        screen.blit(loss_text, (250, 700))
        pygame.display.flip()
        

