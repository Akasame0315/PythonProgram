import socket
# import pyautogui
import time
from threading import Timer
from cProfile import run
from json import load
from turtle import left
import pygame
# import random
import os
# import json
from ClientPlayers import Player
from ClientPlayers import Enemy

#遊戲參數
FPS = 60    #一秒內遊戲更新的次數
WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
mx = 0
sx = 0
sy = 0

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
plane01_img = pygame.image.load(os.path.join("image", "plane01.png")).convert()
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

def send(msg):
    global sx, sy
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
    sx = newMsg[0]
    sy = newMsg[1]

    return(newMsg)
    
def gmaeRun():
    run = True
    global x0, y0  #背景1初始位置
    global x1, y1  #背景2初始位置
    global sx, sy  #serverPos

    pos = pygame.mouse.get_pos()
    send(f"{pos[0]}, {pos[1]}")
    while run:
        clock.tick(FPS)  #一秒內最多的執行次數

        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                run = False
        
        time.sleep(0.01) #隔0.01秒再傳
        all_sprites = pygame.sprite.Group()
        player = Player()
        enemy = Enemy(int(sx), int(sy))
        player_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        player_group.add(player)
        enemy_group.add(enemy)
        all_sprites.add(player) #把物件放進group裡
        all_sprites.add(enemy) #把物件放進group裡


        pos = pygame.mouse.get_pos()
        #更新遊戲
        # all_sprites.update()    #groups裡所有物件update
        # Player.animate(player, pos[0], pos[1])  #角色移動動畫
        player.update()
        enemy.update(int(sx), int(sy))
        
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
        write_text(screen, "serverPosx: " + str(sx) , 22, 100, 70)
        write_text(screen, "serverPosy: " + str(sy) , 22, 100, 90)
        pygame.display.flip()
        pygame.display.update()
        send(f"{pos[0]}, {pos[1]}")
    
    pygame.quit()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(client.recv(HEADER).decode(FORMAT))
gmaeRun()