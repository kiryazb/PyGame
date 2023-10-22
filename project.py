import pygame
import random
import os
import sys

WIDTH = 1080
HEIGHT = 720
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TerraKnight")
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png')).convert()
sky_img = pygame.image.load(os.path.join(img_folder, '123.png')).convert()
snow_img = pygame.image.load(os.path.join(img_folder, 'snow.png')).convert()
sword_right_img = pygame.image.load(os.path.join(img_folder, 'sword1.png')).convert()
sword_left_img = pygame.image.load(os.path.join(img_folder, 'sword2.png')).convert()
enemy_img = pygame.image.load(os.path.join(img_folder, 'flyFly1.png')).convert()
agr_img = pygame.image.load(os.path.join(img_folder, 'agr.png')).convert()
hp_img = pygame.image.load(os.path.join(img_folder, 'hp.png')).convert()
attack_sword_img = pygame.image.load(os.path.join(img_folder, 'attack_sword.png')).convert()

x, y = WIDTH / 2, HEIGHT - 230
x1, y1 = WIDTH / 2, HEIGHT - 600
x2, y2 = 150, 20
x3, y3 = 150, 20
x_attack_swords, y_attack_swords = x + 37, y - 40
x_attack_swords1, y_attack_swords1 = x - 37, y + 40
n = 9
enemy_heart_count = 9
swords_equip = False
win = False
game_over = False


class Player(pygame.sprite.Sprite):
    global attack_sword

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.center = (WIDTH / 2, HEIGHT - 100)

    def update(self):
        i = 0
        global x, y, sword_right, sword_left, hp, x2, n, swords_equip, attack_sword
        attack_sword = Attack_sword()
        enemy_attack_sword = Enemy_Attack_sword()
        x2 = 15
        sword_right = Sword_right()
        sword_left = Sword_left()
        x, y = self.rect.x, self.rect.y
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        mousestate = pygame.mouse.get_pressed()
        if keystate[pygame.K_x]:
            all_sprites.add(sword_right)
            all_sprites.add(sword_left)
            swords_equip = True
        if swords_equip:
            all_sprites.add(sword_right)
            all_sprites.add(sword_left)
        if mousestate[0] and swords_equip:
            all_sprites.add(attack_sword)
            all_sprites.add(enemy_attack_sword)
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        while i <= n:
            hp = HPbar()
            all_sprites.add(hp)
            i += 1
            x2 += 30


class Snow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = snow_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (WIDTH - 300, HEIGHT + 360)


class Sword_right(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sword_right_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (x + 100, y + 20)


class Sword_left(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sword_left_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (x - 37, y + 25)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        self.flag = False
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.center = (WIDTH / 2, HEIGHT - 600)

    def update(self):
        i = 0
        global x1, y1, agr, x3, enemy_heart_count, win, game_over
        count = 0
        x1, y1 = self.rect.x, self.rect.y
        x3 = 800
        self.speedy, self.speedx = 0, 0
        self.speedy, self.speedx = random.randint(-1, 2), random.randint(-1, 2)
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        agr = Provocation()
        if y - y1 < 100 and abs(x - x1) < 200:
            all_sprites.add(agr)
        if (x1 > x_attack_swords - 40 and x1 < x_attack_swords + 40) \
                and (y1 > y_attack_swords - 40 and y1 < y_attack_swords + 40):
            win = True
        if (x > x_attack_swords1 - 40 and x < x_attack_swords1 + 40) \
                and (y > y_attack_swords1 - 40 and y < y_attack_swords1 + 40):
            game_over = False
        print(game_over)
        for i in range(enemy_heart_count):
            hp1 = EnemyHPbar()
            all_sprites.add(hp1)
            x3 += 30
            i += 1

    def coords_enemy(self):
        return x1, y1


class Attack_sword(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = attack_sword_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (x + 37, y - 40)

    def update(self):
        global x_attack_swords, y_attack_swords
        x_attack_swords, y_attack_swords = self.rect.x, self.rect.y
        self.rect.x += 8
        self.rect.y -= 8

class Enemy_Attack_sword(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = attack_sword_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (x1 - 37, y1 + 40)

    def update(self):
        global x_attack_swords1, y_attack_swords1
        x_attack_swords1, y_attack_swords1 = self.rect.x, self.rect.y
        self.rect.x -= 8
        self.rect.y += 8



class Provocation(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = agr_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        coords = []
        for i in enemy.coords_enemy():
            coords.append(i)
        self.rect.center = (coords[0] + 40, coords[1] - 30)


class HPbar(pygame.sprite.Sprite):
    global x2, y2

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = hp_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (x2, y2)

class EnemyHPbar(pygame.sprite.Sprite):
    global x3, y3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = hp_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (x3, y3)


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
snow = Snow()
all_sprites.add(snow)
enemy = Enemy()
all_sprites.add(enemy)

if __name__ == '__main__':
    screen.fill((255, 255, 255))
    f1 = pygame.font.Font(None, 36)
    text1 = f1.render('Начать игру', True,
                      (0, 0, 0))
    f1 = pygame.font.Font(None, 36)
    text2 = f1.render('Выход', True,
                      (0, 0, 0))
    f1 = pygame.font.Font(None, 36)
    text3 = f1.render('X - экипировать оружие', True,
                      (0, 0, 0))
    f1 = pygame.font.Font(None, 36)
    text4 = f1.render('ЛКМ - атаковать', True,
                      (0, 0, 0))
    f1 = pygame.font.Font(None, 36)
    text5 = f1.render('D - ходить вправо', True,
                      (0, 0, 0))
    f1 = pygame.font.Font(None, 36)
    text6 = f1.render('A - ходить влево', True,
                      (0, 0, 0))
    screen.blit(text1, (WIDTH // 2 - 80, HEIGHT // 2 - 100))
    screen.blit(text2, (WIDTH // 2 - 50, HEIGHT // 2))
    screen.blit(text3, (WIDTH - 300, 100))
    screen.blit(text4, (WIDTH - 300, 150))
    screen.blit(text5, (WIDTH - 300, 200))
    screen.blit(text6, (WIDTH - 300, 250))
    pygame.display.update()
    start = False
    running = True
    while running:
        if not start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (pygame.mouse.get_pos()[0] > (WIDTH // 2 - 80)) \
                            and (pygame.mouse.get_pos()[0] < (WIDTH // 2 + 80)) \
                            and (pygame.mouse.get_pos()[1] > (HEIGHT // 2 - 100)) \
                            and (pygame.mouse.get_pos()[1] < (HEIGHT // 2 - 60)):
                        start = True
                    if (pygame.mouse.get_pos()[0] > (WIDTH // 2 - 80)) \
                            and (pygame.mouse.get_pos()[0] < (WIDTH // 2 + 80)) \
                            and (pygame.mouse.get_pos()[1] > (HEIGHT // 2)) \
                            and (pygame.mouse.get_pos()[1] < (HEIGHT // 2 + 40)):
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()
        else:
            if not win:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                all_sprites.update()
                screen.blit(sky_img, (0, 0))
                all_sprites.draw(screen)
                pygame.display.flip()
                sword_right.kill()
                sword_left.kill()
                agr.kill()
                hp.kill()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if win:
                        screen.fill((WHITE))
                        f1 = pygame.font.Font(None, 36)
                        text6 = f1.render('YOU WIN!!', True,
                                          (0, 0, 0))
                        screen.blit(text6, (WIDTH // 2 - 80, HEIGHT // 2 - 100))
                        pygame.display.flip()

    pygame.quit()