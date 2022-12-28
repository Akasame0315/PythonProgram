# region import
from time import sleep, time
import pygame
import socket
import threading
from ServerPlayers import Player
from ServerPlayers import Enemy
from PrintOnScreen import write_text, center_line
import Globals
import bullet
from Explosion import Explosion
import handIdentify
import os
import time as T
import random
from Power import Power
# endregion

Globals.initial()
Globals.cameraNum = 0
# region 參數
DISCONNECT_MESSAGE = "!DISCONNECT"
Globals.serverIP = Globals.SERVER
shoot = "FALSE"
clientShoot = "FALSE"
leftHandText = "none"
rightHandText = "none"
planex, planey = int(Globals.WIDTH/2), 700
connected = True
player_power = 'Null'
TimeStamp = 0
clientpower = 'Null'
#endregion

clock = pygame.time.Clock() #管理遊戲的時間
#初始化&創建視窗
pygame.init()
screen = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))   #設定視窗大小
pygame.display.set_caption("ServerGame")   #視窗名稱

# region 載入背景圖片
background_img = Globals.background_img
background_size = background_img.get_size()
background_rect = background_img.get_rect()
x0, y0 = 0, 0   #背景1初始位置
x1, y1 = 1280, 0    #背景2初始位置
cx, cy = 0, 0
# endregion

# region sprite群組 可以放進sprite的物件
all_sprites = pygame.sprite.Group()
player = Player(planex, planey)
player_bullets = pygame.sprite.Group()
enemy = Enemy(cx, cy)
enemy_bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
power_sprites = pygame.sprite.Group()
all_sprites.add(player) #把物件放進group裡
all_sprites.add(enemy) #把物件放進group裡
# endregion

#server傳送
def handle_client(conn, addr):
    global cx, cy, shoot, clientShoot, connected, clientpower
    print(f"-----[NEW CONNECTION] {addr} connected.-----")
    conn.send(f"-----{addr}Connect success-----".encode(Globals.FORMAT))

    connected = True
    while connected:
        msg_length = conn.recv(Globals.HEADER).decode(Globals.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(Globals.FORMAT)
            print("msg:", msg)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print("client unconnect.")

            else:
                newMsg = msg.split(',')
                cx = int(newMsg[0])
                cy = int(newMsg[1])
                clientShoot = newMsg[2]
                clientpower = newMsg[3]
                conn.send(f"{planex},{planey},{shoot},{player_power},{Globals.lineRect}".encode(Globals.FORMAT))
    
    conn.close()

def start():
    global cx, cy #clientPos
    global x0, y0, x1, y1,planex, planey
    global shoot, clientShoot #射擊判定
    global leftHandText, rightHandText #手勢辨識結果
    global connected, player_power, TimeStamp
    
    threads = []    #執行緒陣列(多個子執行緒)
    shoot = "FALSE"
    beHit = "FALSE"
    clientBeHit = "FALSE"
    
    server.listen()
    print(f"[LISTENING] Server is listening on {Globals.PORT}")
    
    #等待連線畫面
    screen.blit(pygame.transform.scale(Globals.loading_img, (Globals.WIDTH, Globals.HEIGHT)), (x0, y0))
    write_text(screen,"WAITTING FOR CONNECT...", 100, 70, 570, Globals.YELLOW)
    write_text(screen,"YOUR ROOM ADDRESS IS: " + f"[{Globals.serverIP}]", 70, 50, Globals.HEIGHT-150, Globals.RED)
    pygame.display.flip()
    pygame.display.update()
    
    conn, addr = server.accept()
    severConn = threading.Thread(target=handle_client, args=(conn, addr))   #server執行緒
    handsIdentify = threading.Thread(target=handIdentify.handIdentify)  #手勢辨識執行緒(未完成)
    threads.append(severConn)
    threads.append(handsIdentify)
    for i in range(len(threads)):
        threads[i].start()   #執行緒依序開始
    # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    
    #遊戲迴圈
    if connected:
        running = True
    else:   running = False
    while running:
        beHit = "FALSE"
        clientBeHit = "FALSE"
        shoot = "FALSE"
        leftHandText = handIdentify.Ltext
        rightHandText = handIdentify.Rtext
        clock.tick(Globals.FPS)  #一秒內最多的執行次數
        time = pygame.time.get_ticks()
        now = T.localtime(T.time())
        now = T.strftime('%S', now)

        #更新遊戲
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                running = False
            # if event.type == pygame.KEYDOWN:    #判斷鍵盤按鍵
                # if event.key == pygame.K_SPACE: #按下空白鍵發射子彈
        if leftHandText == "7" and time%5 == 0:
            shoot = 'TRUE'
            if player_power == 'gun':
                player_bullet1 = bullet.Bullet(planex+15 , planey, -10)
                all_sprites.add(player_bullet1)
                player_bullets.add(player_bullet1)
                player_bullet2 = bullet.Bullet(planex-15, planey, -10)
                all_sprites.add(player_bullet2)
                player_bullets.add(player_bullet2)
            else:
                player_bullet = bullet.Bullet(planex, planey, -10)
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
        enemy.update(cx, cy)
        enemy.animate(cx, cy, clientpower) 

        planex = player.rect.centerx
        planey = player.rect.centery

        #判斷對手發射子彈
        if clientShoot == 'TRUE':
            if clientpower == 'gun':
                enemy_bullet1 = bullet.Bullet(cx+15 , cy, 10)
                all_sprites.add(enemy_bullet1)
                enemy_bullets.add(enemy_bullet1)
                enemy_bullet2 = bullet.Bullet(cx-15, cy, 10)
                all_sprites.add(enemy_bullet2)
                enemy_bullets.add(enemy_bullet2)
            else:
                print("client shoot!")
                enemy_bullet = bullet.Bullet(cx, cy, 10)
                enemy_bullets.add(enemy_bullet)
                all_sprites.add(enemy_bullet)
                clientShoot = "FALSE"

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
                print("server plane be hit.")
                beHit = "TRUE"
                all_sprites.remove(enemy_bullet)
                enemy_bullet.kill()
                Globals.lineRect += 10
        #判斷子彈跟敵人碰撞
        if clientpower == 'shield': #敵人有盾牌
            enemy_hits = pygame.sprite.spritecollide(enemy, player_bullets, True, pygame.sprite.collide_circle)
            for hit in enemy_hits:
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                power_sprites.add(expl)
                all_sprites.remove(player_bullet)
                enemy_bullet.kill()
        else:
            enemy_hits = pygame.sprite.spritecollide(enemy, player_bullets, True, pygame.sprite.collide_circle)
            if enemy_hits:
                for hit in enemy_hits:
                    # 寶物掉落
                    if random.random() < 0.9:
                        pow = Power(hit.rect.center, +3)
                        all_sprites.add(pow)
                        power_sprites.add(pow)
                        powers.add(pow)
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprites.add(expl)
                    power_sprites.add(expl)
                    print("client plane be hit.")
                    clientBeHit = "TRUE"
                    all_sprites.remove(player_bullet)
                    player_bullet.kill()
                    Globals.lineRect -= 10
        
        power_sprites.update()
        #背景移動
        x0 -= 0.7
        x1 -= 0.7
        screen.blit(pygame.transform.scale(background_img, (1280, 800)), (x0, y0))
        screen.blit(pygame.transform.scale(background_img, (1280, 800)), (x1, y1))
        if x0 < -1280:    x0 = 1280
        if x1 < -1280:    x1 = 1280

        all_sprites.draw(screen)    #把sprites的東西都畫到screen上
        
        write_text(screen, "mx:" + str(planex) + " my:" + str(planey), 22, 50, 20)
        write_text(screen, "ClientPosX:" + str(cx) + " ClientPosY:" + str(cy), 22, 50, 40)
        # write_text(screen, "serverIP:" + str(Globals.serverIP), 22, 50, 60)
        write_text(screen, "shoot:" + str(shoot), 22, 50, 60)
        write_text(screen, "BeHit:" + str(beHit), 22, 50, 80)
        write_text(screen, "clientBeHit:" + str(clientBeHit), 22, 50, 100)
        write_text(screen, f"handsText:{leftHandText},{rightHandText}", 22, 50, 120)
        # write_text(screen, f"handsSign:{LHSign},{RHSign}", 22, 50, 140)
        write_text(screen, f"line: {Globals.lineRect}", 22, 50, 140)
        write_text(screen, f"RPos {handIdentify.RPos} LPos {handIdentify.LPos}", 22, 50, 160)
        write_text(screen, f"playerPower:{player_power}", 22, 50, 180)
        center_line(screen, Globals.lineRect)
        
        pygame.display.flip()
        pygame.display.update()
        sleep(0.001)

        if Globals.lineRect <= 140:
            screen.blit(pygame.transform.scale(Globals.winImg, (1280, 800)), (0, 0))
            pygame.display.flip()
            pygame.display.update()
            sleep(1)
            if rightHandText == 'ok':
                conn.send("!DISCONNECT".encode(Globals.FORMAT))
                for thread in threads:
                    thread._delete()   #執行緒依序結束
                running = False
        
        elif Globals.lineRect >= 660:
            screen.blit(pygame.transform.scale(Globals.loseImg, (1280, 800)), (0, 0))
            pygame.display.flip()
            pygame.display.update()
            sleep(1)
            if rightHandText == 'ok':
                conn.send("!DISCONNECT".encode(Globals.FORMAT))
                for thread in threads:
                    thread._delete()   #執行緒依序結束
                running = False
            # conn.close()
    
    pygame.quit()
    os.system(".\start.py")
        
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(Globals.ADDR)
print("ADDR:", Globals.ADDR)
print("[STARTING] server is starting...")
start()