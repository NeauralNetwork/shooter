from pygame import *
from random import *
from time import time as timer

window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(700,500))

clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
kick = mixer.Sound('fire.ogg')
mixer.music.set_volume(0.3)
#kick.play()



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,w,h):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
    

bullets = sprite.Group()
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top,15,15,20)
        bullets.add(bullet)
        if self.rect.y < 0:
            bullet.kill()

lost = 0
kill = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(0,660)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(0,660)


asteroids = sprite.Group()
monsters = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png',randint(0,660),-50,randint(1,2),60,40)
    monsters.add(monster)

for i in range(3):
    asteroid = Asteroid('asteroid.png',randint(0,660),-50,randint(1,2),60,40)
    asteroids.add(asteroid)

rocket = Player('rocket.png',300,420,10,60,80)
game = True
finish = False
font.init()
font1 = font.SysFont('Arial',30)
font2 = font.SysFont('Arial',70)
fire_sound = mixer.Sound('fire.ogg')
num_fire = 0
rel_time = False
while game:  
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    rocket.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire >= 7 and rel_time == False:
                    rel_time = True
                    start = timer()
    
    if finish != True:
        window.blit(background,(0,0))
        rocket.update()
        rocket.reset()
        monsters.update()
        monsters.draw(window)
        text_lose = font1.render('Пропущено: '+str(lost),1,(255,255,255))
        window.blit(text_lose,(0,0))
        text_kill = font1.render('Убито: '+str(kill),1,(255,255,255))
        window.blit(text_kill,(0,40))
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        sprites_list = sprite.groupcollide(monsters,bullets,True,True)
        if rel_time == True:
            new_time = timer()
            if new_time - start < 3:
                text_win = font1.render('идет перезарядка',1,(255,255,0))
                window.blit(text_win,(270,450))
            if new_time - start >= 3:                
                rel_time = False
                num_fire = 0
        for monster in sprites_list:
            kill += 1
            monster = Enemy('ufo.png',randint(0,660),-50,randint(1,3),60,40)
            monsters.add(monster)
        if kill >= 10:
            text_win = font2.render('ВЫ ВЫИГРАЛИ',1,(255,255,0))
            window.blit(text_win,(215,230))
            finish = True
        if lost >= 6 or sprite.spritecollide(rocket,monsters,False) or sprite.spritecollide(rocket,asteroids,False):
            textlose = font2.render('ВЫ ПРОИГРАЛИ',1,(255,255,0))
            window.blit(textlose,(160,230))
            finish = True


    display.update()
    clock.tick(FPS)