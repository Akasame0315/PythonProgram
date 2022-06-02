from cProfile import run
from json import load
from turtle import left
import pygame
import random
import os
import json

FPS = 60    #一秒內遊戲更新的次數
WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock() #管理遊戲的時間
#初始化&創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #設定視窗大小
pygame.display.set_caption("JetGame")   #視窗名稱

#載入背景圖片
background_img = pygame.image.load(os.path.join("image", "background.png")).convert()    #convert轉換成pygame容易讀取的格式
background02_img = pygame.image.load(os.path.join("image", "background.png")).convert()
background_size = background_img.get_size()
background_rect = background_img.get_rect()
x0, y0 = 0, 0   #背景1初始位置
x1, y1 = 0, -700    #背景2初始位置

#載入物件圖片
rock_img = pygame.image.load(os.path.join("image", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("image", "bullet.png")).convert()
bullet02_img = pygame.image.load(os.path.join("image", "bullet02.png")).convert()
plane01_img = pygame.image.load(os.path.join("image", "plane01(1).png")).convert()
plane01R_img = pygame.image.load(os.path.join("image", "plane01_R30.png")).convert()
plane01L_img = pygame.image.load(os.path.join("image", "plane01_L30.png")).convert()
enmies_img = pygame.image.load(os.path.join("image", "plane03.png")).convert()

#載入字體
font_name = pygame.font.match_font('arial')

#印出分數
def write_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)    #True是代表要用反鋸齒
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)  #畫出文字

#印出生命數
def draw_lifes(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)    #True是代表要用反鋸齒
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)  #畫出文字

#def newRock():
#    rock = Rock()
#    all_sprites.add(rock)   #刪除石頭後要再增加新的石頭並加回群組
#    rocks.add(rock)    

def newEnmies():
    enmy = Enmies()
    all_sprites.add(enmy)
    enmies.add(enmy) 

#玩家
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        #self.image = pygame.Surface((70, 120))   #顯示的圖片
        #self.image.fill((100, 100, 100))      
        self.direction = 0
        self.image = pygame.transform.scale(plane01_img, (120, 100)) #調整圖片大小
        self.image.set_colorkey(BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.radius = 35   #圓型碰撞範圍半徑
        pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)    #畫出圓形
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50
        self.speedx = 7                         #圖片移動速度
        self.lifes = 5

    def animate(self):
        if self.direction == -1:    #向左
            self.image = pygame.transform.scale(plane01L_img, (120, 100))
            self.image.set_colorkey(BLACK)
            #self.rect = self.image.get_rect()
        elif self.direction == 1:   #向右
            self.image = pygame.transform.scale(plane01R_img, (120, 100))
            self.image.set_colorkey(BLACK)
            #self.rect = self.image.get_rect()
        else:
            self.image = pygame.transform.scale(plane01_img, (120, 100))
            self.image.set_colorkey(BLACK)
            #self.rect = self.image.get_rect()

    def update(self):
        #wasd移動圖片
        self.image = pygame.transform.scale(plane01_img, (120, 100))
        self.direction = 0

        key_pressed = pygame.key.get_pressed()  #判斷鍵盤有沒有被按下
        if key_pressed[pygame.K_d]:            #按下d的話圖片往右移
            self.direction = 1
            self.rect.x += self.speedx
            if self.rect.centerx > WIDTH:         #如果圖片碰到邊緣就不再往右
                self.rect.centerx = WIDTH

        if key_pressed[pygame.K_a]:       
            self.direction = -1
            self.rect.x -= self.speedx
            if self.rect.centerx < 0:
                self.rect.centerx = 0;

        if key_pressed[pygame.K_w]:             
            self.rect.y -= self.speedx
            if self.rect.top < 0:
                self.rect.top = 0;

        if key_pressed[pygame.K_s]:             
            self.rect.y += self.speedx
            if self.rect.bottom - 10 > HEIGHT:
                self.rect.bottom= HEIGHT + 10 ;
    
    #子彈發射
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top + 30)
        all_sprites.add(bullet) 
        bullets.add(bullet) 

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        #self.image = pygame.Surface((30, 30))   #顯示的圖片
        #self.image.fill((0, 0, 0))      
        self.image = pygame.transform.scale(rock_img, (40, 40)) #調整圖片大小
        self.image.set_colorkey(BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.radius = 15   #圓型碰撞範圍半徑
        #pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)    #畫出圓形
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)  #初始x座標用隨機設定(範圍設在視窗內)
        self.rect.y = random.randrange(-150, -100)    #初始y座標用隨機設定(範圍設在視窗外)
        self.speedy = random.randrange(3, 7)    #圖片移動速度
        self.speedx = random.randrange(-3, 3)

    def update(self):
        #石頭移動 
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        #石頭超出視窗就重設初始位置
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Enmies(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        #self.image = pygame.Surface((30, 30))   #顯示的圖片
        #self.image.fill((0, 0, 0))      
        self.image = pygame.transform.scale(enmies_img, (80, 60)) #調整圖片大小
        self.image.set_colorkey(WHITE)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.radius = 18   #圓型碰撞範圍半徑
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)    #畫出圓形
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)  #初始x座標用隨機設定(範圍設在視窗內)
        #self.rect.y = random.randrange(-150, -100)    #初始y座標用隨機設定(範圍設在視窗外)
        self.rect.y = 70
        self.speedy = random.randrange(3, 7)    #圖片移動速度
        self.speedx = random.randrange(-3, 3)

    def update(self):
        #移動 
        #self.rect.y += self.speedy
        self.rect.x += self.speedx

        #超出視窗就重設初始位置
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            #self.rect.y = random.randrange(-150, -40)
            #self.speedy = random.randrange(2, 10)
            self.rect.y = 70
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        #self.image = pygame.Surface((10, 30))   #顯示的圖片
        #self.image.fill((200, 200, 0))      
        self.image = pygame.transform.scale(bullet_img, (30, 40)) #調整圖片大小
        self.image.set_colorkey(0, 255)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = x
        self.rect.bottom = y    #初始y座標用隨機設定(範圍設在視窗外)
        self.speedy = 10
        
    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()     #把物件從所有群組中刪除

 #sprite群組 可以放進sprite的物件
all_sprites = pygame.sprite.Group()
#rocks = pygame.sprite.Group()
enmies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
all_sprites.add(player) #把物件放進group裡
#for i in range(7):  #生成數個石頭
#    newRock()

for i in range(7):
    newEnmies()

score = 0   #分數
#lifes = 5   #生命數

#遊戲迴圈
running = True

while running:
    clock.tick(FPS)  #一秒內最多的執行次數

    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #關閉視窗
            running = False

        elif event.type == pygame.KEYDOWN:  #判斷鍵盤按下
            if event.key == pygame.K_SPACE:
                player.shoot()

    #更新遊戲
    all_sprites.update()    #groups裡所有物件update
    Player.animate(player)  #角色移動動畫
    hits = pygame.sprite.groupcollide(enmies, bullets, True, True)  #判斷碰撞以及是否刪除物件
    for hit in hits:    
        score += 30
        #newRock()
        #newEnmies()
        if score == 210:    running = False
    
    hits = pygame.sprite.spritecollide(player, enmies, True, pygame.sprite.collide_circle)  #判斷飛船跟石頭碰撞
    for hit in hits:    #碰到石頭就扣一條命
        player.lifes -= 1
        if player.lifes <= 0:  running = False
        #newRock()
        newEnmies

    y1 += 5 #背景移動
    y0 += 5 #背景移動
    screen.blit(pygame.transform.scale(background_img, (500, 700)), (x0, y0))
    screen.blit(pygame.transform.scale(background_img, (500, 700)), (x1, y1))
    if y0 > 700:    y0 = -700   #圖片到底就重新放回上方
    if y1 > 700:    y1 = -700

    all_sprites.draw(screen)    #把sprites的東西都畫到screen上
    write_text(screen, "score: " + str(score), 22, 70, 30)
    draw_lifes(screen, "lifes: " + str(player.lifes), 22, 70, 650)

    pygame.display.flip()
    pygame.display.update()
    

pygame.quit()

