# region import
import socket
from threading import Timer
from cProfile import run
from json import load
from time import sleep
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
# 連線參數
DISCONNECT_MESSAGE = "!DISCONNECT"
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
enemy = Enemy(sx, sx)
enemy_bullets = pygame.sprite.Group()
all_sprites.add(player) #把物件放進group裡
all_sprites.add(enemy) #把物件放進group裡 
# endregion

#client傳送
def send(msg):
    global sx, sy, serverShoot
    message = msg.encode(Globals.FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(Globals.FORMAT)
    send_length += b' ' * (Globals.HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    servermsg = client.recv(Globals.HEADER).decode(Globals.FORMAT)

    newMsg = servermsg.split(',')
    print("Serverpos:" , newMsg)
    # print("type", type(newMsg))
    
    sx = int(newMsg[0])
    sy = int(newMsg[1])
    serverShoot = newMsg[2]
    
def gmaeRun():
    global sx, sy  #serverPos
    global x0, x1, y0, y1 #背景初始位置
    global shoot, serverShoot #射擊判定

    send(f"250,70,{shoot}") #遊戲前傳送一次座標(預設位置)
    
    #遊戲迴圈
    run = True
    while run:
        clock.tick(Globals.FPS)  #一秒內最多的執行次數

        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                run = False
            if event.type == pygame.KEYDOWN:    #判斷鍵盤按鍵
                if event.key == pygame.K_SPACE: #按下空白鍵發射子彈
                    shoot = 'TRUE'
                    player_bullet = bullet.Bullet(planex, planey, 10)
                    all_sprites.add(player_bullet)
                    player_bullets.add(player_bullet)
                    
        pos = pygame.mouse.get_pos()
        print("clientPos:",pos[0], pos[1])
        #更新遊戲
        if(pos[0] != 0 or pos[1] != 0):
            player.update(pos[0], pos[1])
            player.animate(pygame.mouse.get_rel()[0])
        enemy.update(sx, sy)
        enemy.animate(sx, sy)
        
        #判斷對手發射子彈
        if serverShoot == 'TRUE':
            enemy_bullet = bullet.Bullet(sx, sy, -10)
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
        write_text(screen, "serverPosX: " + str(sx) + " serverPosY: " + str(sy), 22, 50, 40)
        write_text(screen,"serverIP:" + str(Tk_window.serverIP), 22, 50, 60)
        write_text(screen,"ServerKey:" + str(serverShoot), 22, 50, 80)
        write_text(screen,"key:" + str(shoot), 22, 50, 100)
        
        pygame.display.flip()
        pygame.display.update()
        send(f"{planex},{planey},{shoot}") #遊戲內持續傳送
        shoot = 'FALSE'
        sleep(0.001)

    pygame.quit()
    send("!DISCONNECT")

#IP setting
Tk_window.TK_connect()
if Tk_window.serverIP != "":
    SERVER = Tk_window.serverIP
    ADDR = (SERVER, Globals.PORT)
else:
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, Globals.PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(client.recv(Globals.HEADER).decode(Globals.FORMAT))
gmaeRun()