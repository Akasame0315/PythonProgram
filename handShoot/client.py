# region import
import socket
import threading
from threading import Timer
from cProfile import run
from json import load
from time import sleep
from turtle import left
import pygame
from ClientPlayers import Player
from ClientPlayers import Enemy
from PrintOnScreen import write_text, center_line
import Globals
import Tk_window
import bullet
import os
#endregion

Globals.initial()
Globals.cameraNum = 1
import handIdentify

#region 連線參數
DISCONNECT_MESSAGE = "!DISCONNECT"
shoot = "FALSE"
serverShoot = "FALSE"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
x1, y1 = 1280, 0  #背景2初始位置
sx, sy = 0, 0
ready = False
leftHandText = "none"
rightHandText = "none"
LHSign = "none"
RHSign = "none"
move = 0
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
    print("servermsg:", servermsg)
    
    newMsg = servermsg.split(',')
    sx = int(newMsg[0])
    sy = int(newMsg[1])
    serverShoot = newMsg[2]
    
def gmaeRun():
    print(client.recv(Globals.HEADER).decode(Globals.FORMAT))

    global sx, sy  #serverPos
    global x0, x1, y0, y1 #背景初始位置
    global shoot, serverShoot #射擊判定
    global RHSign, LHSign, rightHandText, leftHandText, ready
    global move

    # send("250,70,FALSE") #遊戲前傳送一次座標(預設位置)
    planex = 250
    planey = 70

    handID = threading.Thread(target=handIdentify.handIdentify)
    handID.start()

    #遊戲迴圈
    run = True

    while run:
        shoot = "FALSE"
        beHit = "FALSE"
        serverBeHit = "FALSE"
        clock.tick(Globals.FPS)  #一秒內最多的執行次數
        # leftHandText = handIdentify.Ltext
        # rightHandText = handIdentify.Rtext
        time = pygame.time.get_ticks()

        # if(leftHandText == "0" and rightHandText == "0"):   #雙手握拳才開始偵測移動
        #     ready = True
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                run = False
            # if event.type == pygame.KEYDOWN:    #判斷鍵盤按鍵
            #     if event.key == pygame.K_SPACE: #按下空白鍵發射子彈
            #         shoot = 'TRUE'
            #         player_bullet = bullet.Bullet(planex, planey, 10)
            #         all_sprites.add(player_bullet)
            #         player_bullets.add(player_bullet)
        if leftHandText == "7" and time%5 == 0:
            shoot = 'TRUE'
            player_bullet = bullet.Bullet(planex, planey, 10)
            all_sprites.add(player_bullet)
            player_bullets.add(player_bullet)
        # pos = pygame.mouse.get_pos()
        # print("clientPos:",pos[0], pos[1])
        #更新遊戲
        # if(pos[0] != 0 or pos[1] != 0):
        #     player.update(pos[0], pos[1])
        #     player.animate(pygame.mouse.get_rel()[0])
        player.animate(handIdentify.RPos[0])
        enemy.update(sx, sy)
        enemy.animate(sx, sy)

        planex = player.rect.centerx
        planey = player.rect.centery
        
        #判斷對手發射子彈
        if serverShoot == 'TRUE':
            print("server shoot!")
            enemy_bullet = bullet.Bullet(sx, sy, -10)
            enemy_bullets.add(enemy_bullet)
            all_sprites.add(enemy_bullet)
            serverShoot = "FALSE"
        
        player_bullets.update()
        enemy_bullets.update()

        #判斷子彈跟玩家碰撞
        player_hits = pygame.sprite.spritecollide(player, enemy_bullets, False, pygame.sprite.collide_circle)  # False：不要刪掉 player
        if player_hits:
            print("client plane be hit.")
            beHit = "TRUE"
            all_sprites.remove(enemy_bullet)
            enemy_bullet.kill()
            move -= 10
            # expl = Explosion.Explosion(cx, cy)
            # all_sprites.add(expl)
        enemy_hits = pygame.sprite.spritecollide(enemy, player_bullets, False, pygame.sprite.collide_circle)  # False：不要刪掉 player
        if enemy_hits:
            print("server plane be hit.")
            serverBeHit = "TRUE"
            all_sprites.remove(player_bullet)
            player_bullet.kill()
            move += 10

        #背景移動
        x0 -= 0.7
        x1 -= 0.7
        screen.blit(pygame.transform.scale(background_img, (1280, 800)), (x0, y0))
        screen.blit(pygame.transform.scale(background_img, (1280, 800)), (x1, y1))
        if x0 < -1280:    x0 = 1280
        if x1 < -1280:    x1 = 1280

        all_sprites.draw(screen)    #把sprites的東西都畫到screen上
        
        # if ready == False:
        #     write_text(screen,"clenched hands TO BE READY", 50, 50, Globals.HEIGHT/2, Globals.YELLOW)
        write_text(screen, "mx: " + str(planex) + " my: " + str(planey), 22, 50, 20)
        write_text(screen, "serverPosX: " + str(sx) + " serverPosY: " + str(sy), 22, 50, 40)
        write_text(screen,"serverIP:" + str(Tk_window.serverIP), 22, 50, 60)
        write_text(screen,"key:" + str(shoot), 22, 50, 100)
        write_text(screen,"BeHit:" + str(beHit), 22, 50, 120)
        write_text(screen,"serverBeHit:" + str(serverBeHit), 22, 50, 140)
        write_text(screen, f"RPos {handIdentify.RPos} LPos {handIdentify.LPos}", 22, 50, 160)
        write_text(screen, f"line: {Globals.lineRect}", 22, 50, 200)
        center_line(screen, move)
        
        pygame.display.flip()
        pygame.display.update()
        send(f"{planex},{planey},{shoot}") #遊戲內持續傳送
        sleep(0.001)

        if Globals.lineRect <= 140 or Globals.lineRect >= 660:
            run = False
            screen.blit(pygame.transform.scale(Globals.tutorial_img, (1280, 800)), (0, 0))
            pygame.display.flip()
            pygame.display.update()
            sleep(5)

    pygame.quit()
    send("!DISCONNECT")
    os.system(".\start.py")

#IP setting
# try:
Tk_window.TK_connect()
if Tk_window.serverIP != "":
    SERVER = Tk_window.serverIP
    ADDR = (SERVER, Globals.PORT)
else:
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, Globals.PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
gmaeRun()
# finally:
#     print("連線失敗，請確認輸入的IP位置是否正確!")
#     pygame.quit()
    # os.system(".\start.py")