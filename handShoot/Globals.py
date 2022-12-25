from telnetlib import IP
import pygame
import os
import socket

#辨識
cameraNum = 0

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
    global FPS, WIDTH, HEIGHT, WHITE, BLACK, RED, YELLOW, ROSE, planesize_middle, planesize_large, screen, controlMode
    FPS = 60 
    WIDTH = 1280
    HEIGHT = 800
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    ROSE = (255,248,220)
    planesize_middle = (200, 150)
    planesize_large = (250, 150)
    controlMode = 3

    global lineRect
    lineRect = HEIGHT/2

    #遊戲初始化
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))   #設定視窗大小

    #背景
    global background_img, tutorial_img, tutorial2_img, tutorial3_img
    background_img = pygame.image.load(os.path.join("image", "background04(no cir).png")).convert()
    tutorial_img = pygame.image.load(os.path.join("image", "tutorial.png")).convert()
    tutorial2_img = pygame.image.load(os.path.join("image", "tutorial2.png")).convert()
    tutorial3_img = pygame.image.load(os.path.join("image", "tutorial3.png")).convert()
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
    font_name = pygame.font.match_font('SimHei')
    # font_name = pygame.font.SysFont('SimHei',32)

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

    # 爆炸圖片
    global expl_anim, expl_anim_lg, expl_anim_sm
    expl_anim = {}
    expl_anim_lg = []
    expl_anim_sm = []

    def expl_anim():
        for i in range(9):
            expl_img = pygame.image.load(os.path.join("image", f'expl{i}.png')).convert()
            expl_img.set_colorkey(BLACK)
            expl_anim_lg.append(pygame.transform.scale(expl_img, (75, 75)))
            expl_anim_sm.append(pygame.transform.scale(expl_img, (40, 40)))

