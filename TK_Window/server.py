# region import
from ast import Global
from cProfile import run
from ctypes import memset, sizeof
from json import load
from pickle import FALSE, TRUE
from time import sleep, time
from turtle import left, pos
import pygame
import socket
import threading
from threading import Timer
from ServerPlayers import Player
from ServerPlayers import Enemy
from PrintOnScreen import write_text
import GlobalValue
# endregion

GlobalValue.initial()
# region 參數
cx = 0
cy = 0
# 連線參數
HEADER = 1024
PORT = 888
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
GlobalValue.serverIP = SERVER
shoot = "FALSE"
clientShoot = "FALSE"
#endregion

clock = pygame.time.Clock() #管理遊戲的時間
#初始化&創建視窗
pygame.init()
screen = pygame.display.set_mode((GlobalValue.WIDTH, GlobalValue.HEIGHT))   #設定視窗大小
pygame.display.set_caption("ServerGame")   #視窗名稱

# region 載入背景圖片
background_img = GlobalValue.background_img
background_size = background_img.get_size()
background_rect = background_img.get_rect()
x0, y0 = 0, 0   #背景1初始位置
x1, y1 = 1600, 0    #背景2初始位置
# endregion

# region sprite群組 可以放進sprite的物件
all_sprites = pygame.sprite.Group()
player = Player(GlobalValue.WIDTH/2, 850)
enemy = Enemy(int(cx), int(cy))
all_sprites.add(player) #把物件放進group裡
all_sprites.add(enemy) #把物件放進group裡
# endregion

#server傳送
def handle_client(conn, addr):
    global cx, cy, shoot, clientShoot
    print(f"-----[NEW CONNECTION] {addr} connected.-----")
    conn.send(f"-----{addr}Connect success-----".encode(FORMAT))

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        planex = player.rect.centerx
        planey = player.rect.centery
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print("client unconnect.")

            else:
                newMsg = msg.split(',')
                print("Clientpos:" , newMsg)
                print("type", type(newMsg))

            conn.send(f"{planex} , {planey}, {shoot}".encode(FORMAT))
            cx = newMsg[0]
            cy = newMsg[1]
            clientShoot = newMsg[2]

        sleep(0.01) #0.01傳送一次
    
    conn.close()

def start():
    global cx, cy #clientPos
    global x0, y0, x1, y1 #背景初始位置
    global shoot #射擊判定
    
    server.listen()
    print(f"[LISTENING] Server is listening on {PORT}")
    
    #等待連線畫面
    screen.blit(pygame.transform.scale(GlobalValue.loading_img, (GlobalValue.WIDTH, GlobalValue.HEIGHT)), (x0, y0))
    write_text(screen,"WAITTING FOR CONNECT...", 100, 70, 600, GlobalValue.YELLOW, TRUE)
    write_text(screen,"YOUR ROOM ADDRESS IS: " + f"[{GlobalValue.serverIP}]", 70, 70, GlobalValue.HEIGHT-150, GlobalValue.RED, TRUE)
    pygame.display.flip()
    pygame.display.update()
    
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    #遊戲迴圈
    running = True
    while running:
        clock.tick(GlobalValue.FPS)  #一秒內最多的執行次數

        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot = 'TRUE'
                

        pos = pygame.mouse.get_pos()
        print(pos[0], pos[1])
        #更新遊戲
        if(pos[0] != 0 or pos[1] != 0):
            player.update(pos[0], pos[1])
            player.animate(pygame.mouse.get_rel()[0])

        enemy.update(int(cx), int(cy))
        enemy.animate(int(cx), int(cy))
        planex = player.rect.centerx
        planey = player.rect.centery

        #背景移動
        x0 -= 0.7
        x1 -= 0.7
        screen.blit(pygame.transform.scale(background_img, (1600, 900)), (x0, y0))
        screen.blit(pygame.transform.scale(background_img, (1600, 900)), (x1, y1))
        if x0 < -1600:    x0 = 1600
        if x1 < -1600:    x1 = 1600

        all_sprites.draw(screen)    #把sprites的東西都畫到screen上
        write_text(screen, "mx: " + str(planex) + " my: " + str(planey), 22, 50, 20)
        write_text(screen,"ClientPosx:" + str(cx) + " ClientPosy:" + str(cy), 22, 50, 40)
        write_text(screen,"GlobalSX:" + str(GlobalValue.ServerX), 22, 50, 60)
        write_text(screen,"GlobalCX:" + str(GlobalValue.ServerEnemy), 22, 50, 80)
        write_text(screen,"serverIP:" + str(GlobalValue.serverIP), 22, 50, 100)
        write_text(screen,"key:" + str(shoot), 22, 50, 120)
        write_text(screen,"clientKey:" + str(clientShoot), 22, 50, 140)
        
        pygame.display.flip()
        pygame.display.update()
        shoot = 'FALSE'
        
    pygame.quit()
        
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print("ADDR:", ADDR)
print("[STARTING] server is starting...")
start()