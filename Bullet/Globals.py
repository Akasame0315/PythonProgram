from telnetlib import IP
import pygame
import os
import socket

def initial():
    #連線參數
    global HEADER, PORT, SERVER, ADDR, FORMAT, serverIP
    HEADER = 1024
    PORT = 888
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    serverIP = socket.gethostbyname(socket.gethostname())
    
    #遊戲參數
    global FPS, WIDTH, HEIGHT, WHITE, BLACK, RED, YELLOW, planesize_middle, planesize_large, screen
    FPS = 60 
    WIDTH = 1200
    HEIGHT = 900
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    planesize_middle = (200, 150)
    planesize_large = (250, 150)

    #遊戲初始化
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))   #設定視窗大小

    #背景
    global background_img
    background_img = pygame.image.load(os.path.join("image", "background04.png")).convert()
    #loading畫面
    global loading_img 
    loading_img = pygame.image.load(os.path.join("image", "loading.jpg")).convert()
    #子彈圖片
    global bullet_img, bullet2_img
    bullet_img = pygame.image.load(os.path.join("image", "bullet2.png")).convert()
    bullet2_img = pygame.image.load(os.path.join("image", "bullet2.png")).convert()
    #爆炸圖片
    global expolose2_img
    expolose2_img = pygame.image.load(os.path.join("image", "expl2.png")).convert()
    #字體字型
    global font_2, font_name, fontSize
    fontSize = 70
    font_2 = pygame.font.Font('Azurite.ttf', fontSize)
    font_name = pygame.font.match_font('arial')

    #飛機圖片
    global plane03_img, plan03L_img, plane03R_img, plane04_img, plan04L_img, plane04R_img
    plane03_img = pygame.image.load(os.path.join("image",'plane03.png')).convert()
    plan03L_img = pygame.image.load(os.path.join("image",'plane03_L30.png')).convert()
    plane03R_img = pygame.image.load(os.path.join("image",'plane03_R30.png')).convert()
    plane04_img = pygame.image.load(os.path.join("image", "plane04.png")).convert()
    plan04L_img = pygame.image.load(os.path.join("image", "plane04_L30.png")).convert()
    plane04R_img = pygame.image.load(os.path.join("image", "plane04_R30.png")).convert()

    global ServerX, ClientX, ServerEnemy, ClientEnemy
    ServerX = WIDTH/2
    ServerEnemy = WIDTH/2
    ClientX = WIDTH/2
    ClientEnemy = WIDTH/2


def getHit(player, enemy_bullets):
    
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, False, pygame.sprite.collide_circle)  # False：不要刪掉 player

    if player_hits: print("now is hitting")
    # for i in range(enemy_number):
    #     if i == 0:
    #         enemy_hits = pygame.sprite.spritecollide(enemy[i], player_bullets, True, pygame.sprite.collide_circle)
    #     else: enemy_hits += pygame.sprite.spritecollide(enemy[i], player_bullets, True, pygame.sprite.collide_circle)

    # IsBreak = False
    # if score[0] == 0 or (score[1] == 0 and score[2] == 0 and score[3] == 0):
    #     IsBreak = True

    ## 分數
    # for hit in player_hits:
    #     if IsBreak: break
    #     score[0] -= deduction
    #     expl = Explosion(hit.rect.center, 'sm')
    #     all_sprites.add(expl)
    # if enemy_is_exist[0]: 
    #     enemy0_hits = pygame.sprite.spritecollide(enemy[0], player_bullets, True, pygame.sprite.collide_circle)
    #     for hit in enemy0_hits:
    #         if IsBreak: break
    #         score[1] -= deduction
    #         expl = Explosion(hit.rect.center, 'sm')
    #         all_sprites.add(expl)

    # # 使分數不小於 0
    # for i in range(enemy_number + 1):
    #     if score[i] <= 0:
    #         score[i] = 0

    # return score