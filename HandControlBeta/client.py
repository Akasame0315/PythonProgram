# region import
import socket
import threading
from time import sleep
import pygame
from ClientPlayers import Player
from ClientPlayers import Enemy
from PrintOnScreen import write_text, center_line
import Globals
import Tk_window
import bullet
import os
import cv2
from Explosion import Explosion
import random
from Power import Power
import time as T
#endregion

Globals.initial()

import handIdentify
handIdentify.cap = cv2.VideoCapture(1)

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

#等待連線畫面
screen.blit(pygame.transform.scale(Globals.loading_img, (Globals.WIDTH, Globals.HEIGHT)), (0, 0))
write_text(screen,"WAITTING FOR CONNECT...", 100, 70, 570, Globals.YELLOW)
write_text(screen,"ENTRY YOUR ROMM ADDRESS TO JOIN THE GAME", 70, 40, Globals.HEIGHT-150, Globals.RED)
pygame.display.flip()
pygame.display.update()

# region 載入背景圖片
background_img = Globals.background_img
background02_img = Globals.background_img
background_size = background_img.get_size()
background_rect = background_img.get_rect()
x0, y0 = 0, 0   #背景1初始位置
x1, y1 = 1280, 0  #背景2初始位置
sx, sy = 0, 0
running = True
leftHandText = "none"
rightHandText = "none"
LHSign = "none"
RHSign = "none"
player_power = 'Null'
TimeStamp = 0
servermsg = ""
serverPower = 'Null'
TimeStamp = 0
lineRect = Globals.HEIGHT/2
# endregion

#region sprite群組 可以放進sprite的物件
all_sprites = pygame.sprite.Group()
player = Player(Globals.WIDTH/2, 70)
player_bullets = pygame.sprite.Group()
enemy = Enemy(sx, sx)
enemy_bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
power_sprites = pygame.sprite.Group()
all_sprites.add(player) #把物件放進group裡
all_sprites.add(enemy) #把物件放進group裡 
# endregion

#client傳送
def send(msg):
    global sx, sy, serverShoot, servermsg, serverPower, lineRect
    message = msg.encode(Globals.FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(Globals.FORMAT)
    send_length += b' ' * (Globals.HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    servermsg = client.recv(Globals.HEADER).decode(Globals.FORMAT)
    print("servermsg:", servermsg)
    if not servermsg == DISCONNECT_MESSAGE:
        newMsg = servermsg.split(',')
        sx = int(newMsg[0])
        sy = int(newMsg[1])
        serverShoot = newMsg[2]
        serverPower = newMsg[3]
        lineRect = int(newMsg[4])

    
def gmaeRun():
    print(client.recv(Globals.HEADER).decode(Globals.FORMAT))

    global sx, sy  #serverPos
    global x0, x1, y0, y1 #背景初始位置
    global shoot, serverShoot #射擊判定
    global RHSign, LHSign, rightHandText, leftHandText
    global running, serverPower, TimeStamp, player_power, lineRect

    # send("250,70,FALSE") #遊戲前傳送一次座標(預設位置)
    planex = 250
    planey = 70

    handID = threading.Thread(target=handIdentify.handIdentify)
    handID.start()

    #遊戲迴圈
    running = True

    while running:
        shoot = "FALSE"
        beHit = "FALSE"
        serverBeHit = "FALSE"
        clock.tick(Globals.FPS)  #一秒內最多的執行次數
        leftHandText = handIdentify.Ltext
        rightHandText = handIdentify.Rtext
        time = pygame.time.get_ticks()
        now = T.localtime(T.time())
        now = T.strftime('%S', now)

        # if(leftHandText == "0" and rightHandText == "0"):   #雙手握拳才開始偵測移動
        #     ready = True
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                running = False
            # if event.type == pygame.KEYDOWN:    #判斷鍵盤按鍵
            #     if event.key == pygame.K_SPACE: #按下空白鍵發射子彈
            #         shoot = 'TRUE'
            #         player_bullet = bullet.Bullet(planex, planey, 10)
            #         all_sprites.add(player_bullet)
            #         player_bullets.add(player_bullet)
        if leftHandText == "7" and time%5 == 0:
            shoot = 'TRUE'
            if player_power == 'gun':
                player_bullet1 = bullet.Bullet(planex+15 , planey, 10)
                all_sprites.add(player_bullet1)
                player_bullets.add(player_bullet1)
                player_bullet2 = bullet.Bullet(planex-15, planey, 10)
                all_sprites.add(player_bullet2)
                player_bullets.add(player_bullet2)
            else:
                player_bullet = bullet.Bullet(planex, planey, 10)
                all_sprites.add(player_bullet)
                player_bullets.add(player_bullet)

        # 寶物倒數
        # enemy_power = 'gun'
        # enemy_power = 'shield'
        if int(TimeStamp) - int(now) > 3 or int(now) - int(TimeStamp) > 3:
            Timestamp_Power = False
            player_power = 'Null'
        # 玩家吃到寶物
        player_power_hits = pygame.sprite.spritecollide(player, powers, True, pygame.sprite.collide_circle)
        for hit in player_power_hits:
            if hit.type == 'gun' and Timestamp_Power == False:
                TimeStamp = now
                player_power = 'gun'
                Timestamp_Power = True
            if hit.type == 'shield' and Timestamp_Power == False:
                TimeStamp = now
                player_power = 'shield'
            Timestamp_Power = True
        
        player.animate(handIdentify.RPos[0], handIdentify.RPos[0], handIdentify.RPos[1], player_power)
        enemy.update(sx, sy)
        enemy.animate(sx, sy, serverPower)
        
        planex = player.rect.centerx
        planey = player.rect.centery

        #判斷對手發射子彈
        if serverShoot == 'TRUE':
            if serverPower == 'gun':
                enemy_bullet1 = bullet.Bullet(sx+15 , sy, -10)
                all_sprites.add(enemy_bullet1)
                enemy_bullets.add(enemy_bullet1)
                enemy_bullet2 = bullet.Bullet(sx-15, sy, -10)
                all_sprites.add(enemy_bullet2)
                enemy_bullets.add(enemy_bullet2)
            else:
                print("server shoot!")
                enemy_bullet = bullet.Bullet(sx, sy, -10)
                enemy_bullets.add(enemy_bullet)
                all_sprites.add(enemy_bullet)
                serverShoot = "FALSE"
        
        player_bullets.update()
        enemy_bullets.update()

        #判斷子彈跟玩家碰撞
        if player_power == 'shield':    #玩家有盾牌
            player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_circle)  # False：不要刪掉 player
            for hit in player_hits:
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                power_sprites.add(expl)
                all_sprites.remove(enemy_bullet)
                enemy_bullet.kill()
        else:
            player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True,pygame.sprite.collide_circle)  # False：不要刪掉 player
            for hit in player_hits:
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                power_sprites.add(expl)
                print("client plane be hit.")
                beHit = "TRUE"
                all_sprites.remove(enemy_bullet)
                enemy_bullet.kill()
        #判斷子彈跟敵人碰撞
        if serverPower == 'shield': #敵人有盾牌
            enemy_hits = pygame.sprite.spritecollide(enemy, player_bullets, True, pygame.sprite.collide_circle)
            for hit in enemy_hits:
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                power_sprites.add(expl)
                all_sprites.remove(player_bullet)
                enemy_bullet.kill()
        else:
            enemy_hits = pygame.sprite.spritecollide(enemy, player_bullets, True, pygame.sprite.collide_circle)
            for hit in enemy_hits:
                # 寶物掉落
                if random.random() < 0.9:
                    pow = Power(hit.rect.center, -3)
                    all_sprites.add(pow)
                    power_sprites.add(pow)
                    powers.add(pow)
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                power_sprites.add(expl)
                print("server plane be hit.")
                serverBeHit = "TRUE"
                all_sprites.remove(player_bullet)
                player_bullet.kill()

        power_sprites.update()
        
        #背景移動
        x0 -= 0.7
        x1 -= 0.7
        screen.blit(pygame.transform.scale(background_img, (1280, 800)), (x0, y0))
        screen.blit(pygame.transform.scale(background_img, (1280, 800)), (x1, y1))
        if x0 < -1280:    x0 = 1280
        if x1 < -1280:    x1 = 1280

        all_sprites.draw(screen)    #把sprites的東西都畫到screen上
        
        write_text(screen, "mx: " + str(planex) + " my: " + str(planey), 22, 50, 20)
        write_text(screen, "serverPosX: " + str(sx) + " serverPosY: " + str(sy), 22, 50, 40)
        # write_text(screen,"serverIP:" + str(Tk_window.serverIP), 22, 50, 60)
        write_text(screen,"shoot:" + str(shoot), 22, 50, 60)
        write_text(screen,"BeHit:" + str(beHit), 22, 50, 80)
        write_text(screen,"serverBeHit:" + str(serverBeHit), 22, 50, 100)
        write_text(screen, f"handsText:{leftHandText},{rightHandText}", 22, 50, 120)
        write_text(screen, f"line: {lineRect}", 22, 50, 140)
        write_text(screen, f"RPos {handIdentify.RPos} LPos {handIdentify.LPos}", 22, 50, 160)
        write_text(screen, f"playerPower:{player_power}", 22, 50, 180)
        center_line(screen, lineRect)
        
        pygame.display.flip()
        pygame.display.update()
        
        if servermsg == DISCONNECT_MESSAGE:
            send("!DISCONNECT")
        else:   send(f"{planex},{planey},{shoot},{player_power}") #遊戲內持續傳送
        sleep(0.001)

        if lineRect <= 140:
            screen.blit(pygame.transform.scale(Globals.loseImg, (1280, 800)), (0, 0))
            pygame.display.flip()
            pygame.display.update()
            sleep(1)
            if rightHandText == 'ok':
                send("!DISCONNECT")
                handID._delete()
                running = False
        elif lineRect >= 660:
            screen.blit(pygame.transform.scale(Globals.winImg, (1280, 800)), (0, 0))
            pygame.display.flip()
            pygame.display.update()
            sleep(1)
            if rightHandText == 'ok':
                send("!DISCONNECT")
                handID._delete()
                running = False

    pygame.quit()
    send("!DISCONNECT")
    os.system(".\start.py")

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
gmaeRun()