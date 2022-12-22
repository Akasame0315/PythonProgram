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
import Globals
import bullet
import Explosion
import handIdentify
import autopy
# endregion

Globals.initial()
# region 參數
DISCONNECT_MESSAGE = "!DISCONNECT"
Globals.serverIP = Globals.SERVER
shoot = "FALSE"
clientShoot = "FALSE"
leftHandText = "none"
rightHandText = "none"
LHSign = "none"
RHSign = "none"
planex, planey = Globals.WIDTH/2, 850
ready = False
connected = True
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
player = Player(Globals.WIDTH/2, 850)
player_bullets = pygame.sprite.Group()
enemy = Enemy(cx, cy)
enemy_bullets = pygame.sprite.Group()
all_sprites.add(player) #把物件放進group裡
all_sprites.add(enemy) #把物件放進group裡
# endregion

#server傳送
def handle_client(conn, addr):
    global cx, cy, shoot, clientShoot, connected
    print(f"-----[NEW CONNECTION] {addr} connected.-----")
    conn.send(f"-----{addr}Connect success-----".encode(Globals.FORMAT))

    connected = True
    while connected:
        msg_length = conn.recv(Globals.HEADER).decode(Globals.FORMAT)
        planex = player.rect.centerx
        planey = player.rect.centery
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

            # conn.send(f"{planex},{planey},{shoot}".encode(Globals.FORMAT))
    
    conn.close()

def start():
    global cx, cy #clientPos
    global x0, y0, x1, y1, planex, planey, ready
    global shoot, clientShoot #射擊判定
    global leftHandText, rightHandText, LHSign, RHSign #手勢辨識結果
    global connected
    
    threads = []    #執行緒陣列(多個子執行緒)

    shoot = "FALSE"
    beHit = "FALSE"
    clientBeHit = "FALSE"
    
    server.listen()
    print(f"[LISTENING] Server is listening on {Globals.PORT}")
    
    #等待連線畫面
    screen.blit(pygame.transform.scale(Globals.loading_img, (Globals.WIDTH, Globals.HEIGHT)), (x0, y0))
    write_text(screen,"WAITTING FOR CONNECT...", 100, 70, 600, Globals.YELLOW, TRUE)
    write_text(screen,"YOUR ROOM ADDRESS IS: " + f"[{Globals.serverIP}]", 70, 70, Globals.HEIGHT-150, Globals.RED, TRUE)
    pygame.display.flip()
    pygame.display.update()
    
    conn, addr = server.accept()
    severConn = threading.Thread(target=handle_client, args=(conn, addr))   #server執行緒
    handsIdentify = threading.Thread(target=handIdentify.handIdentify)  #手勢辨識執行緒(未完成)
    # mouse = threading.Thread(target=handIdentify.mouseMove, args=(handIdentify.RPos[0], handIdentify.RPos[1]))
    # mouse.start()
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
        LHSign = handIdentify.LSign
        RHSign = handIdentify.RSign
        clock.tick(Globals.FPS)  #一秒內最多的執行次數
        pos = pygame.mouse.get_pos()    #滑鼠位置
        time = pygame.time.get_ticks()
        # autopy.mouse.move(handIdentify.RPos[0] , handIdentify.RPos[1]) # 平滑移动鼠标
        # print("severPos:",pos[0], pos[1])

        #更新遊戲
        print(f"serverLeftHand:{leftHandText}, serverRightHand:{rightHandText}")
        print(f"LHSign:{LHSign}, RHSigh:{RHSign}, READY:{ready}")
        if(leftHandText == "0" and rightHandText == "0"):   #雙手握拳才開始偵測移動
            ready = True

        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                running = False
            # if event.type == pygame.KEYDOWN:    #判斷鍵盤按鍵
                # if event.key == pygame.K_SPACE: #按下空白鍵發射子彈
        if rightHandText == "7" and time%6 == 0:
            shoot = 'TRUE'
            player_bullet = bullet.Bullet(planex, planey, -10)
            all_sprites.add(player_bullet)
            player_bullets.add(player_bullet)

        if ready and rightHandText == '5':
            planex = pos[0]
            planey = pos[1]
            player.update()
            player.animate(planex, planey, pygame.mouse.get_rel()[0])
        # if(pos[0] != 0 or pos[1] != 0):
        #     player.update(pos[0], pos[1])
        #     player.animate(pygame.mouse.get_rel()[0])
        # planex = player.rect.centerx
        # planey = player.rect.centery
        enemy.update(cx, cy)
        enemy.animate(cx, cy) 

        #判斷對手發射子彈
        if clientShoot == 'TRUE':
            print("client shoot!")
            enemy_bullet = bullet.Bullet(cx, cy, 10)
            enemy_bullets.add(enemy_bullet)
            all_sprites.add(enemy_bullet)
            clientShoot = "FALSE"

        
        player_bullets.update()
        enemy_bullets.update()
        

        #判斷子彈跟玩家碰撞
        player_hits = pygame.sprite.spritecollide(player, enemy_bullets, False, pygame.sprite.collide_circle)  # False：不要刪掉 player
        if player_hits:
            print("server plane be hit.")
            beHit = "TRUE"
            all_sprites.remove(enemy_bullet)
            enemy_bullet.kill()
            # expl = Explosion.Explosion((planex, planey), "lg")
            # all_sprites.add(expl)
            # expl.update()
            # if expl.frame >= len(Globals.expl_anim[expl.size]):
            #     expl.kill()
            #     all_sprites.remove(expl)

        enemy_hits = pygame.sprite.spritecollide(enemy, player_bullets, False, pygame.sprite.collide_circle)  # False：不要刪掉 player
        if enemy_hits:
            print("client plane be hit.")
            clientBeHit = "TRUE"
            all_sprites.remove(player_bullet)
            player_bullet.kill()
        
        #背景移動
        x0 -= 0.7
        x1 -= 0.7
        screen.blit(pygame.transform.scale(background_img, (1600, 900)), (x0, y0))
        screen.blit(pygame.transform.scale(background_img, (1600, 900)), (x1, y1))
        if x0 < -1600:    x0 = 1600
        if x1 < -1600:    x1 = 1600

        all_sprites.draw(screen)    #把sprites的東西都畫到screen上
        # leftHandText = handIdentify.Ltext
        # rightHandText = handIdentify.Rtext
        # LHSign = handIdentify.LSign
        # RHSign = handIdentify.RSign
        
        if ready == False:
            write_text(screen,"clenched hands TO BE READY", 50, 50, Globals.HEIGHT/2, Globals.YELLOW, TRUE)
        write_text(screen, "mx:" + str(planex) + " my:" + str(planey), 22, 50, 20)
        write_text(screen, "ClientPosX:" + str(cx) + " ClientPosY:" + str(cy), 22, 50, 40)
        write_text(screen, "serverIP:" + str(Globals.serverIP), 22, 50, 60)
        write_text(screen, "key:" + str(shoot), 22, 50, 80)
        write_text(screen, "BeHit:" + str(beHit), 22, 50, 120)
        write_text(screen, "clientBeHit:" + str(clientBeHit), 22, 50, 140)
        write_text(screen, f"handsText:{leftHandText},{rightHandText}", 22, 50, 160)
        write_text(screen, f"handsSign:{LHSign},{RHSign}", 22, 50, 180)
        write_text(screen, f"ready:{ready} {time} {int(time)}", 22, 50, 200)
        write_text(screen, f"RPos {handIdentify.RPos} LPos {handIdentify.LPos}", 22, 50, 220)
        
        pygame.display.flip()
        pygame.display.update()
        conn.send(f"{planex},{planey},{shoot}".encode(Globals.FORMAT))
        sleep(0.001)
        
    pygame.quit()
        
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(Globals.ADDR)
print("ADDR:", Globals.ADDR)
print("[STARTING] server is starting...")
start()