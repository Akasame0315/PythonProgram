# region import
import socket
from threading import Timer
from cProfile import run
from json import load
from turtle import left
import pygame
from ClientPlayers import Player
from ClientPlayers import Enemy
from PrintOnScreen import write_text
import Globals
import Tk_window
import bullet
#endregion

Globals.initial()
sx = 0
sy = 0
# 連線參數
HEADER = 1024
PORT = 888
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = ""
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
shoot = "FALSE"
serverShoot = "FALSE"
# endregion

clock = pygame.time.Clock() #管理遊戲的時間
#初始化&創建視窗
pygame.init()
screen = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))   #設定視窗大小
pygame.display.set_caption("ClientWindow")   #視窗名稱

# region 載入背景圖片
background_img = Globals.background_img
background02_img = Globals.background_img
background_size = background_img.get_size()
background_rect = background_img.get_rect()
x0, y0 = 0, 0   #背景1初始位置
x1, y1 = 1600, 0  #背景2初始位置
sx, sy = 0, 0
# endregion

#region sprite群組 可以放進sprite的物件
all_sprites = pygame.sprite.Group()
player = Player(Globals.ClientX, 70)
player_bullets = pygame.sprite.Group()
enemy = Enemy(int(sx), int(sy))
enemy_bullets = pygame.sprite.Group()
all_sprites.add(player) #把物件放進group裡
all_sprites.add(enemy) #把物件放進group裡 
# endregion

#client傳送
def send(msg):
    global sx, sy, serverShoot
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    servermsg = client.recv(HEADER).decode(FORMAT)

    newMsg = servermsg.split(',')
    print("Serverpos:" , newMsg)
    print("type", type(newMsg))
    
    sx = newMsg[0]
    sy = newMsg[1]
    serverShoot = newMsg[2]
    
def gmaeRun():
    global sx, sy  #serverPos
    global x0, x1, y0, y1 #背景初始位置
    global shoot, serverShoot

    send(f"250,70,{shoot}") #遊戲前傳送一次座標(預設位置)
    
    #遊戲迴圈
    run = True
    while run:
        clock.tick(Globals.FPS)  #一秒內最多的執行次數

        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot = 'TRUE'
                    player_bullet = bullet.Bullet(planex, planey, 10)
                    all_sprites.add(player_bullet)
                    player_bullets.add(player_bullet)
                    
        pos = pygame.mouse.get_pos()
        print(pos[0], pos[1])
        #更新遊戲
        if(pos[0] != 0 or pos[1] != 0):
            player.update(pos[0], pos[1])
            player.animate(pygame.mouse.get_rel()[0])
        enemy.update(int(sx), int(sy))
        enemy.animate(int(sx), int(sy))
        
        if serverShoot == 'TRUE':
            enemy_bullet = bullet.Bullet(int(sx), int(sy), -10)
            enemy_bullets.add(enemy_bullet)
            all_sprites.add(enemy_bullet)
        
        planex = player.rect.centerx
        planey = player.rect.centery
        player_bullets.update()
        enemy_bullets.update()

        #背景移動
        x0 -= 0.7
        x1 -= 0.7
        screen.blit(pygame.transform.scale(background_img, (1600, 900)), (x0, y0))
        screen.blit(pygame.transform.scale(background_img, (1600, 900)), (x1, y1))
        if x0 < -1600:    x0 = 1600
        if x1 < -1600:    x1 = 1600

        all_sprites.draw(screen)    #把sprites的東西都畫到screen上
        write_text(screen, "mx: " + str(planex) + " my: " + str(planey), 22, 50, 20)
        write_text(screen, "serverPosx: " + str(sx) + " serverPosy: " + str(sy), 22, 50, 40)
        write_text(screen,"GlobalSX:" + str(Globals.ClientEnemy), 22, 50, 60)
        write_text(screen,"GlobalCX:" + str(Globals.ClientX), 22, 50, 80)
        write_text(screen,"serverIP:" + str(Tk_window.serverIP), 22, 50, 100)
        write_text(screen,"key:" + str(shoot), 22, 50, 120)
        write_text(screen,"ServerKey:" + str(serverShoot), 22, 50, 140)
        
        pygame.display.flip()
        pygame.display.update()
        send(f"{planex},{planey},{shoot}") #遊戲內持續傳送

        
        shoot = 'FALSE'

    pygame.quit()
    send("!DISCONNECT")

#IP setting
Tk_window.TK_connect()
if Tk_window.serverIP != "":
    SERVER = Tk_window.serverIP
    ADDR = (SERVER, PORT)
else:
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(client.recv(HEADER).decode(FORMAT))
gmaeRun()