import socket
import pyautogui
import time
from threading import Timer
from cProfile import run
from json import load
from turtle import left
import pygame
import random
import os
import json

#遊戲參數
FPS = 60    #一秒內遊戲更新的次數
WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
mx = 0

#連線參數
HEADER = 1024
PORT = 888
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = ""
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

clock = pygame.time.Clock() #管理遊戲的時間
#初始化&創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #設定視窗大小
pygame.display.set_caption("ClientWindow")   #視窗名稱

#載入背景圖片
background_img = pygame.image.load(os.path.join("image", "background.png")).convert()    #convert轉換成pygame容易讀取的格式
background02_img = pygame.image.load(os.path.join("image", "background.png")).convert()
background_size = background_img.get_size()
background_rect = background_img.get_rect()
x0, y0 = 0, 0   #背景1初始位置
x1, y1 = 0, -700    #背景2初始位置

#載入物件圖片
plane01_img = pygame.image.load(os.path.join("image", "plane01(1).png")).convert()
enemy_img = pygame.image.load(os.path.join("image",'plane03.png')).convert()

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

#玩家
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        self.direction = 0
        self.image = pygame.transform.scale(plane01_img, (120, 100)) #調整圖片大小
        self.image.set_colorkey(BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.radius = 35   #圓型碰撞範圍半徑
        pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)    #畫出圓形
        self.rect.centerx = pyautogui.position().x
        self.rect.bottom = pyautogui.position().y-50
        self.speedx = 7                         #圖片移動速度
        self.lifes = 5

    def animate(self, positionx, positiony):
        self.image = pygame.transform.scale(plane01_img, (120, 100))

        self.image.set_colorkey(BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = positionx
        self.rect.centery = positiony

    def update(self):
        #wasd移動圖片
        self.image = pygame.transform.scale(plane01_img, (120, 100)) #調整圖片大小
        self.image.set_colorkey(BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        # return 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (150,120))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 8

    def update(self):
        # 防止飛船超出視窗
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        # if self.rect.bottom > HEIGHT/2:
        #     self.rect.bottom = HEIGHT/2

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    servermsg = client.recv(HEADER).decode(FORMAT)
    print("Serverpos:" + servermsg)
    print("type", type(servermsg))
    newMsg = servermsg.split(',')
    print("Serverpos:" , newMsg)
    print("type", type(newMsg))

    return(newMsg)
    

def gmaeRun():
    run = True
    x0, y0 = 0, 0   #背景1初始位置
    x1, y1 = 0, -700    #背景2初始位置

    pos = pygame.mouse.get_pos()
    print(send(f"{pos[0]}, {pos[1]}"))
    while run:
        clock.tick(FPS)  #一秒內最多的執行次數

        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                run = False
        
        # print("clientPos", pos[0], pos[1])
        time.sleep(0.01) #隔0.01秒再傳
        all_sprites = pygame.sprite.Group()
        player = Player()
        enemy = Enemy(int(send(f"{pos[0]}, {pos[1]}")[0]), int(send(f"{pos[0]}, {pos[1]}")[1]))
        player_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        player_group.add(player)
        enemy_group.add(enemy)
        all_sprites.add(player) #把物件放進group裡
        all_sprites.add(enemy) #把物件放進group裡


        pos = pygame.mouse.get_pos()
        # recive = send(f"{pos[0]}") + send(f"{pos[1]}")
        #更新遊戲
        all_sprites.update()    #groups裡所有物件update
        Player.animate(player, pos[0], pos[1])  #角色移動動畫
        enemy.update()
        
        #背景移動
        y1 += 5 
        y0 += 5 
        screen.blit(pygame.transform.scale(background_img, (500, 700)), (x0, y0))
        screen.blit(pygame.transform.scale(background_img, (500, 700)), (x1, y1))
        if y0 > 700:    y0 = -700   #圖片到底就重新放回上方
        if y1 > 700:    y1 = -700

        all_sprites.draw(screen)    #把sprites的東西都畫到screen上
        write_text(screen, "mx: " + str(pos[0]), 22, 70, 30)
        write_text(screen, "my: " + str(pos[1]), 22, 70, 50)
        write_text(screen, "serverPosx: " + str(send(f"{pos[0]}, {pos[1]}")[0]) , 22, 100, 70)
        write_text(screen, "serverPosy: " + str(send(f"{pos[0]}, {pos[1]}")[1]) , 22, 100, 90)
        pygame.display.flip()
        pygame.display.update()
    
    pygame.quit()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(client.recv(HEADER).decode(FORMAT))
gmaeRun()