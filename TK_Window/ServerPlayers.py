from time import sleep
import pygame
import GlobalValue

GlobalValue.initial()
originx = GlobalValue.ServerX
enemyx = GlobalValue.ServerEnemy

#玩家
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global originx
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        self.image = pygame.transform.scale(GlobalValue.server01_img, (GlobalValue.planesize_large)) #調整圖片大小
        self.image.set_colorkey(GlobalValue.BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = originx
        self.rect.centery = y
        self.radius = 35   #圓型碰撞範圍半徑
        pygame.draw.circle(self.image, GlobalValue.WHITE, self.rect.center, self.radius)    #畫出圓形
        self.speedx = 7                         #圖片移動速度

    def update(self, x, y):
        global originx
        self.image = pygame.transform.scale(GlobalValue.server01_img, (GlobalValue.planesize_large)) #調整圖片大小
        self.image.set_colorkey(GlobalValue.BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = x
        self.rect.centery = y
        # 防止飛船超出視窗
        if self.rect.centerx < 0:
            self.rect.centerx = 0.1
        if self.rect.centerx >= GlobalValue.WIDTH:
            self.rect.centerx = GlobalValue.WIDTH
        if self.rect.centery < 0:
            self.rect.centery = 0.1
        if self.rect.centery >= GlobalValue.WIDTH:
            self.rect.centery = GlobalValue.WIDTH 

    def animate(self, move):
        if move > 0:
            self.image = pygame.transform.scale(GlobalValue.server01R_img, (GlobalValue.planesize_large)) #調整圖片大小
            
        elif move < 0:
            self.image = pygame.transform.scale(GlobalValue.server01L_img, (GlobalValue.planesize_large)) #調整圖片大小
        
        self.image.set_colorkey(GlobalValue.BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.center = pygame.mouse.get_pos()
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(GlobalValue.server02_img, (GlobalValue.planesize_large))
        self.image.set_colorkey(GlobalValue.WHITE)
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 8

    def update(self, x,  y):
        self.image = pygame.transform.scale(GlobalValue.server02_img, (GlobalValue.planesize_large))
        self.image.set_colorkey(GlobalValue.WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        # 防止飛船超出視窗
        if self.rect.centerx <= 0:
            self.rect.centerx = 0
        if self.rect.centerx >= GlobalValue.WIDTH:
            self.rect.centerx = GlobalValue.WIDTH
        if self.rect.centery <= 0:
            self.rect.centery = 0
        if self.rect.centery >= GlobalValue.WIDTH:
            self.rect.centery = GlobalValue.WIDTH

    def animate(self, x, y):
        global enemyx
        if(x > enemyx):
            self.image = pygame.transform.scale(GlobalValue.server02L_img, (GlobalValue.planesize_large)) #調整圖片大小
            self.image.set_colorkey(GlobalValue.BLACK)    #圖片去背
            self.rect = self.image.get_rect()       #圖片定位(外框)
            self.rect.centerx = x
            self.rect.centery = y
            enemyx = x
        elif(x < enemyx):
            self.image = pygame.transform.scale(GlobalValue.server02R_img, (GlobalValue.planesize_large)) #調整圖片大小
            self.image.set_colorkey(GlobalValue.BLACK)    #圖片去背
            self.rect = self.image.get_rect()       #圖片定位(外框)
            self.rect.centerx = x
            self.rect.centery = y
            enemyx = x  
        GlobalValue.ServerEnemy = enemyx