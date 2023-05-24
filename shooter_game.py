import pygame
from random import randint

lost = 0
pygame.font.init()
font2 = pygame.font.Font(None,36)


W, H = 1000, 700
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Шутер')
clock = pygame.time.Clock()
FPS = 100
run = True
finish = False


def game():
    pass


class gamesprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,  size_x, size_y, player_speed = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))


class Enemy(gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > W:
            self.rect.x = randint(80, W - 80)
            self.rect.y = 0
            lost = lost + 1
        is_catch= pygame.sprite.spritecollide(self,bullets,True)
        if is_catch:
            self.kill()

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(gamesprite):
    def __init__(self, player_image, player_x, player_y,  size_x, size_y, player_speed = 0):
        gamesprite.__init__(self, player_image, player_x, player_y,  size_x, size_y, player_speed = 10)
        self.life=5
        self.lvl = 1
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < W -80:
            self.rect.x += self.speed
        is_hit= pygame.sprite.spritecollide(self,monsters, True)
        if is_hit:
            self.life -= 1
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(gamesprite):
    def __init__(self, player_image, player_x, player_y,  size_x, size_y, player_speed = 0):
        gamesprite.__init__(self, player_image, player_x, player_y,  size_x, size_y, player_speed = 10)
        self.life=5
    def update(self):
        if self.rect.y > 0:
            self.rect.y -= 10
        else: 
            self.kill()

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Lifes(gamesprite):
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

img_enemy = "ufo.png"
img_back = "kosmos.png"
img_hero = "ro.png"
img_helse = "life.png"


ship = Player("ro.png", W//2, H-110, 100, 100, 10)
helse_img=pygame.transform.scale(pygame.image.load("life.png"),(80,80))
helse_rect=helse_img.get_rect()
background = pygame.transform.scale(pygame.image.load(img_back) ,(W,H))
monsters = pygame.sprite.Group()

bullets = pygame.sprite.Group()

for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, W - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE and len(bullets) <3:
            bullets.add(Bullet("roket.png",ship.rect.center[0]-11,ship.rect.center[1]-80,25,60))
            bullets.add(Bullet("bullet.png",ship.rect.center[0]-37,ship.rect.center[1]-5,10,30))
            bullets.add(Bullet("bullet.png",ship.rect.center[0]+28,ship.rect.center[1]-5,10,30))



    if not finish:
        win.blit(background, (0, 0))
        text = font2.render('пропущено:' + str(lost), 1, (250, 0, 0))
        win.blit(text, (800, 30))

        ship.update()
        bullets.update()
        ship.reset()
        monsters.update()
        monsters.draw(win)
        ship.draw(win)
        bullets.draw(win)
        for i in range(ship.life):
            win.blit(helse_img,(10+i*80,10))

    pygame.display.update()
    clock.tick(60)
