from time import sleep
import pygame
import Globals

Globals.initial()
# originx = Globals.ServerX
enemyx = Globals.ServerEnemy

#玩家
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global originx
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        self.image = pygame.transform.scale(Globals.server01_img, (Globals.planesize_large)) #調整圖片大小
        self.image.set_colorkey(Globals.BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = x
        self.rect.centery = y
        self.radius = 35   #圓型碰撞範圍半徑
        pygame.draw.circle(self.image, Globals.WHITE, self.rect.center, self.radius)    #畫出圓形
        self.speedx = 7                         #圖片移動速度

    def update(self, x, y):
        global originx
        self.image = pygame.transform.scale(Globals.server01_img, (Globals.planesize_large)) #調整圖片大小
        self.image.set_colorkey(Globals.BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = x
        self.rect.centery = y
        # 防止飛船超出視窗
        if self.rect.centerx < 0:
            self.rect.centerx = 0.1
        if self.rect.centerx >= Globals.WIDTH:
            self.rect.centerx = Globals.WIDTH
        if self.rect.centery < 0:
            self.rect.centery = 0.1
        if self.rect.centery >= Globals.WIDTH:
            self.rect.centery = Globals.WIDTH 

    def animate(self, move):
        if move > 0:
            self.image = pygame.transform.scale(Globals.server01R_img, (Globals.planesize_large)) #調整圖片大小
            
        elif move < 0:
            self.image = pygame.transform.scale(Globals.server01L_img, (Globals.planesize_large)) #調整圖片大小
        
        self.image.set_colorkey(Globals.BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.center = pygame.mouse.get_pos()
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Globals.server02_img, (Globals.planesize_large))
        self.image.set_colorkey(Globals.WHITE)
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 8

    def update(self, x,  y):
        self.image = pygame.transform.scale(Globals.server02_img, (Globals.planesize_large))
        self.image.set_colorkey(Globals.WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        # 防止飛船超出視窗
        if self.rect.centerx <= 0:
            self.rect.centerx = 0
        if self.rect.centerx >= Globals.WIDTH:
            self.rect.centerx = Globals.WIDTH
        if self.rect.centery <= 0:
            self.rect.centery = 0
        if self.rect.centery >= Globals.WIDTH:
            self.rect.centery = Globals.WIDTH

    def animate(self, x, y):
        global enemyx
        if(x > enemyx):
            self.image = pygame.transform.scale(Globals.server02L_img, (Globals.planesize_large)) #調整圖片大小
            self.image.set_colorkey(Globals.BLACK)    #圖片去背
            self.rect = self.image.get_rect()       #圖片定位(外框)
            self.rect.centerx = x
            self.rect.centery = y
            enemyx = x
        elif(x < enemyx):
            self.image = pygame.transform.scale(Globals.server02R_img, (Globals.planesize_large)) #調整圖片大小
            self.image.set_colorkey(Globals.BLACK)    #圖片去背
            self.rect = self.image.get_rect()       #圖片定位(外框)
            self.rect.centerx = x
            self.rect.centery = y
            enemyx = x  
        Globals.ServerEnemy = enemyx