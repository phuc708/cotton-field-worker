from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, char_img, x, y, w, h, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(char_img),(w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 10, 20, 20)
        list_bullet.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.y = 0   

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()    

font.init()
font1 = font.Font(None, 80)  

win_width = 700
win_height = 500
missed = 0
score = 0

win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
background = GameSprite('galaxy.jpg', 0,0,win_width,win_height,0)
player = Player("rocket.png", 200, win_height -50, 50, 50,100)



list_bullet = sprite.Group()

list_enemies = sprite.Group() 
for i in range(6):
    random_X = randint(0, win_width)
    alien = Enemy("ufo.png", random_X, 0, 100, 100, 2)
    list_enemies.add(alien)


finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if not finish:
        background.reset()
        player.update()
        player.reset()
        list_enemies.update()
        list_enemies.draw(window)
        list_bullet.update()
        list_bullet.draw(window)

        font2 = font.Font(None, 20)
        score_text = font2.render("Score: "+ str(score), False, (255, 255,255))
        missed_text = font2.render("Missed: " + str(missed), False, (255, 255,255))
        window.blit(score_text, (50, 100))
        window.blit(missed_text, (50, 200))

        if sprite.spritecollide(player, list_enemies, False):
            finish = True
            window.blit(lose, (win_width/2, win_height/2))


        if sprite.groupcollide(list_bullet, list_enemies, True, True):
            score += 1
            random_X = randint(0, win_width)
            alien = Enemy("ufo.png", random_X, 0, 100, 100, 2)
            list_enemies.add(alien)

            if score >= 20:
                finish = True
                window.blit(win, (win_width/2, win_height/2))

    display.update()
    time.delay(50)