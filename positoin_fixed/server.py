
from ast import Global
from cProfile import run
from ctypes import memset, sizeof
from json import load
from turtle import left, pos
import pygame
import random
import os
import json
import pyautogui
import socket
import threading
import time
from threading import Timer

FPS = 60    #一秒內遊戲更新的次數
WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
mx = 0
cx = 0
cy = 0

HEADER = 1024
PORT = 888
# SERVER = ""
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

clock = pygame.time.Clock() #管理遊戲的時間
#初始化&創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #設定視窗大小
pygame.display.set_caption("ServerGame")   #視窗名稱

#載入背景圖片
background_img = pygame.image.load(os.path.join("image", "background.png")).convert()    #convert轉換成pygame容易讀取的格式
background02_img = pygame.image.load(os.path.join("image", "background.png")).convert()
background_size = background_img.get_size()
background_rect = background_img.get_rect()
x0, y0 = 0, 0   #背景1初始位置
x1, y1 = 0, -700    #背景2初始位置

#載入物件圖片
plane01_img = pygame.image.load(os.path.join("image", "plane03.png")).convert()
enemy_img = pygame.image.load(os.path.join("image",'plane01.png')).convert()

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
        self.image = pygame.transform.scale(plane01_img, (200, 120)) #調整圖片大小
        self.image.set_colorkey(WHITE)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.radius = 35   #圓型碰撞範圍半徑
        pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)    #畫出圓形
        self.rect.centerx = pyautogui.position().x
        self.rect.bottom = pyautogui.position().y-50
        self.speedx = 7                         #圖片移動速度
        self.lifes = 5

    def update(self):
        #wasd移動圖片
        self.image = pygame.transform.scale(plane01_img, (200, 120)) #調整圖片大小
        self.image.set_colorkey(WHITE)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        ServerPos = pygame.mouse.get_pos()
        positionx = ServerPos[0]
        positiony = ServerPos[1]
        self.rect.centerx = positionx
        self.rect.centery = positiony
        # 防止飛船超出視窗
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (120,100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 8

    def update(self, x,  y):
        self.image = pygame.transform.scale(enemy_img, (120,100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        # 防止飛船超出視窗
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

 #sprite群組 可以放進sprite的物件
all_sprites = pygame.sprite.Group()
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
all_sprites.add(player) #把物件放進group裡
enemy = Enemy(int(cx), int(cy))
enemy_group = pygame.sprite.Group()
all_sprites.add(enemy) #把物件放進group裡

def handle_client(conn, addr):
    global cx
    global cy
    print(f"-----[NEW CONNECTION] {addr} connected.-----")
    conn.send(f"-----{addr}Connect success-----".encode(FORMAT))

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        ServerPos = pygame.mouse.get_pos()
        ServerX = ServerPos[0]
        ServerY = ServerPos[1]
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg != DISCONNECT_MESSAGE:
                print(f"client msg: {msg}")
                print("type", type(msg))

                newMsg = msg.split(',')
                print("Clientpos:" , newMsg)
                print("type", type(newMsg))

                conn.send(f"{ServerX} , {ServerY}".encode(FORMAT))
                cx = newMsg[0]
                cy = newMsg[1]
                
            else:
                print(f"{msg} {addr} Stop \n")
                conn.send(f"StopMsg received.".encode(FORMAT))
                connected = False
    
    conn.close()

def start():
    global cx, cy #clientPos
    global x0, x1, y0, y1 #背景初始位置
    server.listen()
    print(f"[LISTENING] Server is listening on {PORT}")
    while True:   
        conn, addr = server.accept()     
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

        #遊戲迴圈
        running = True
        while running:
            clock.tick(FPS)  #一秒內最多的執行次數

            #取得輸入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   #關閉視窗
                    running = False

            pos = pygame.mouse.get_pos()
            #更新遊戲
            # Player.update()    #groups裡所有物件update
            # Player.animate(player)  #角色移動動畫
            player.update()
            enemy.update(int(cx), int(cy))

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
            write_text(screen,"ClientPosx:" + str(cx), 22, 100, 70)
            write_text(screen,"ClientPosy:" + str(cy), 22, 100, 90)
            pygame.display.flip()
            pygame.display.update()
            
        pygame.quit()
        
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print("ADDR:", ADDR)
print("[STARTING] server is starting...")
start()