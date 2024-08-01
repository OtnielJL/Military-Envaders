#importing libraries
import sys
import pygame
import random
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    MOUSEBUTTONDOWN,
    )

#initialise pygame
pygame.init()
pygame.font.init()

#enemy class
numEnemies = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        global numEnemies
        super(Enemy, self).__init__()
        #imports the enemy image
        self.surf = pygame.image.load("rocket.png").convert_alpha()
        self.surf.set_colorkey((0,0,0))
         #setting spawn loaction to a random location
        self.rect = self.surf.get_rect(
            center = (random.randint(sw + 20, sw + 100), random.randint(0,sh)))
        #setting the movement speed
        self.speed = 10
        
#update method that moves image
    def update(self):
        global score
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
            score += 1
    #        
    def slow(self):
        self.setSpeed()
        pygame.time.set_timer(ADDENEMY, 100000)
        pygame.time.set_timer(RESET, 5000)
        pygame.time.set_timer(ADDPOINT, 2000)
        
    def setSpeed(self):
        self.speed = speed
#health class to increase health  
class Health(pygame.sprite.Sprite):
    def __init__(self):
        super(Health, self).__init__()
        #imports the medkit image
        self.surf = pygame.image.load("medkit.png").convert_alpha()
        self.surf.set_colorkey((0,0,0))
        #setting spawn location to a random location
        self.rect = self.surf.get_rect(
            center = (random.randint(sw + 20, sw + 100), random.randint(0,sh)))
        #setting movement speed
        self.speed = 8
    #update method that allows the image to move    
    def update(self):
        global score
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
            score += 1

class Drone(pygame.sprite.Sprite):
    def __init__(self):
        super(Drone, self).__init__()
        #imports the drone image
        self.surf = pygame.image.load("drone1.png").convert_alpha()
        self.surf.set_colorkey((0,0,0))
        #setting spawn location to a random location
        self.rect = self.surf.get_rect(
            center = (random.randint(sw + 20, sw + 100), random.randint(0,sh)))
        #setting movement speed
        self.speed = 8
    #update method that allows the image to move    
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
            
#player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #import player image
        self.surf = pygame.image.load("plane.png").convert_alpha()
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect()
        
    #allows the player the move based on keys pressed
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-20)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0,20)
        elif pressed_keys[K_LEFT]:
            self.rect.move_ip(-20,0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(20,0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > sw:
            self.rect.right = sw
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > sh:
            self.rect.bottom = sh

#initialising screen size       
sw = 1280
sh = 720
score = 10
#initialising clock
clock = pygame.time.Clock()
#initialising lives 
lives = 3

#Initialise mixer and load music
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.1)
#setting the music to loop
pygame.mixer.music.play(loops=-1)

#setting game scree
screen = pygame.display.set_mode([sw,sh])

#importing heart image
life = pygame.image.load("heart.png").convert_alpha()
ADDENEMY = pygame.USEREVENT + 1
#setting spawn time for enemy class
pygame.time.set_timer(ADDENEMY, 500)

ADDHEALTH = pygame.USEREVENT + 2
#setting spawn time for heart
pygame.time.set_timer(ADDHEALTH, 8000)

ADDDRONE = pygame.USEREVENT + 3
#setting spawn time for drone
pygame.time.set_timer(ADDDRONE, 10000)

RESET = pygame.USEREVENT + 4

ADDPOINT = pygame.USEREVENT + 5
#setting end game font size and text
my_font = pygame.font.SysFont('Arial', 30)
gs_font = pygame.font.SysFont('Arial', 40)
bs = pygame.Surface((150,50))
fs = pygame.Surface((150,50))
t = my_font.render("Yes", True, (255,255,255))
f = my_font.render("No", True, (255,255,255))
g = gs_font.render("Game Over", True, (0,0,0))

#setting button locations on end game screen
tc = t.get_rect(center=(bs.get_width()/2, bs.get_height()/2))
fc = f.get_rect(center=(fs.get_width()/2 , fs.get_height()/2))

#creating player
player = Player()

#creating sprite groups
enemies = pygame.sprite.Group()
health = pygame.sprite.Group()
drone = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
#importing sky image for background on the game screen
bg = pygame.image.load("sky.jpg").convert()


while running:
    screen.blit(bg, (0,0))
    #if lives are 0 them import the game over screen and buttons to the game screen
    if lives <= 0:
        bg = pygame.image.load("crash.jpg").convert()
        screen.blit(g, (sw/2 - 100 , sh/3))
        screen.blit(bs, (sw/2 - fs.get_width() - 100,sh/2))
        bs.blit(t,tc)
        screen.blit(fs, (sw/2 + 50 ,sh/2))
        fs.blit(f,fc)

        #checking mouse position
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            #if the Yes button is clicked the game starts over
            if event.type == MOUSEBUTTONDOWN:
                if sw/2 - fs.get_width()-100 <= mouse[0] <= sw/2 and sh/2 <=mouse[1] <= sh/2 + 150:          
                    lives = 3
                    score = 0
                    #kill all enemies when screen loads
                    for entity in enemies:
                        entity.kill()
                    bg = pygame.image.load("sky.jpg").convert()
                #if the No button is clicked the game closes
                elif sw/2 <= mouse[0] <= sw/2+150 and sh/2 <= mouse[1] <= sh/2+150:
                    pygame.quit()
                    sys.exit()
                    
    else:
        for event in pygame.event.get():
            #if the escape key or exit button is pressed game screen exits
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            
            elif event.type == pygame.QUIT:
                running = False

            # adding multiple enemies
            elif event.type == ADDENEMY:
                new_enemy = Enemy(speed)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                
            #adding multiple health powerups
            elif event.type == ADDHEALTH:
                new_health = Health()
                health.add(new_health)
                all_sprites.add(new_health)
            #adding multiple drone poewrups
            elif event.type == ADDDRONE:
                new_drone = Drone()
                drone.add(new_drone)
                all_sprites.add(new_drone)
            #resetting drone speed
            elif event.type == RESET:
                speed = 10
                pygame.time.set_timer(ADDENEMY, 500)
                pygame.time.set_timer(ADDPOINT,800000000)
                for entity in enemies:
                    entity.setSpeed()
            elif event.type == ADDPOINT:
                score += 10
        pressed_keys = pygame.key.get_pressed()
        #updating all classes
        player.update(pressed_keys)
        enemies.update()
        health.update()
        drone.update()

        #creating all sprites
        for en in all_sprites:
            screen.blit(en.surf, en.rect)
    
        for i in range(lives):
            screen.blit(life, (sw - 70 * (i+1),60))

        for entity in enemies:
         #if the player collides with a missile the health is decreased by 1
            if pygame.sprite.spritecollideany(player,enemies):
               lives -= 1
               entity.hit()
               entity.kill()       
            
        #if player collides with a heart life and score are increnemted
        if pygame.sprite.spritecollideany(player,health):            
            lives += 1
            score += 10
            for entity in health:
                entity.kill()

        #if player collides with a drone enemies are frozen    
        for entity in drone:
            if pygame.sprite.spritecollideany(player,drone):            
                entity.kill()
                speed = 0
                for entity in enemies:
                    entity.slow()        
    #display score
    text_surface = my_font.render(str(score), False, (255, 255, 255))
    screen.blit(text_surface, (sw-50,10))
    
    pygame.display.flip()
    #set clock 60 frames per second
    clock.tick(60)

pygame.quit()
