from telnetlib import IP
import pygame
import os

def initial():
    global serverIP
    serverIP = ""
    
    global FPS, WIDTH, HEIGHT, WHITE, BLACK, RED, planesize_middle, planesize_large, screen
    FPS = 60 
    WIDTH = 1440
    HEIGHT = 900
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    planesize_middle = (200, 150)
    planesize_large = (250, 150)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))   #設定視窗大小

    global background_img
    background_img = pygame.image.load(os.path.join("image", "background03.png")).convert()

    global server01_img, server01R_img, server01L_img, server02_img, server02L_img, server02R_img
    server01_img = pygame.image.load(os.path.join("image", "plane01.png")).convert()
    server01R_img = pygame.image.load(os.path.join("image", "plane01_R30.png")).convert()
    server01L_img = pygame.image.load(os.path.join("image", "plane01_L30.png")).convert()
    server02_img = pygame.image.load(os.path.join("image",'plane03.png')).convert()
    server02L_img = pygame.image.load(os.path.join("image",'plane03_L30.png')).convert()
    server02R_img = pygame.image.load(os.path.join("image",'plane03_R30.png')).convert()

    global client01_img, client01R_img, client01L_img, client02_img, client02R_img, client02L_img
    client01_img = pygame.image.load(os.path.join("image",'plane03.png')).convert()
    client01R_img = pygame.image.load(os.path.join("image", "plane03_R30.png")).convert()
    client01L_img = pygame.image.load(os.path.join("image", "plane03_L30.png")).convert()
    client02_img = pygame.image.load(os.path.join("image",'plane01.png')).convert()
    client02L_img = pygame.image.load(os.path.join("image",'plane01_L30.png')).convert()
    client02R_img = pygame.image.load(os.path.join("image",'plane01_R30.png')).convert()
    
    global ServerX, ClientX, ServerEnemy, ClientEnemy
    ServerX = WIDTH/2
    ServerEnemy = WIDTH/2
    ClientX = WIDTH/2
    ClientEnemy = WIDTH/2