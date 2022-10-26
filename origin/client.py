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
HEADER = 64
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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(client.recv(1024).decode(FORMAT))

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

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(1024).decode(FORMAT))


run = True
originTime = time.time()
while run:
    mx, my = pyautogui.position()
    localTime = time.time()
    runTime = localTime-originTime
    # print("(x:",mx, ",y:", my, "),runTime:", round(runTime,3))
    # send(f"(x:{mx}, y:{my}), runTime: {round(runTime,3)}")
    send(f"{mx},{my}")
    # time.sleep(0.5) #隔0.1秒再傳
    all_sprites = pygame.sprite.Group()
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)
    all_sprites.add(player) #把物件放進group裡

    #更新遊戲
    all_sprites.update()    #groups裡所有物件update
    Player.animate(player, mx, my)  #角色移動動畫
    x0, y0 = 0, 0   #背景1初始位置
    x1, y1 = 0, -700    #背景2初始位置
    #背景移動
    y1 += 5 
    y0 += 5 
    screen.blit(pygame.transform.scale(background_img, (500, 700)), (x0, y0))
    screen.blit(pygame.transform.scale(background_img, (500, 700)), (x1, y1))
    if y0 > 700:    y0 = -700   #圖片到底就重新放回上方
    if y1 > 700:    y1 = -700

    all_sprites.draw(screen)    #把sprites的東西都畫到screen上
    pygame.display.flip()
    pygame.display.update()
    # if(localTime-originTime>=5):
    #     print(DISCONNECT_MESSAGE)
    #     send(DISCONNECT_MESSAGE)
    #     break