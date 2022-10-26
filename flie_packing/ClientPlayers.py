import pygame
import os

WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#初始化&創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #設定視窗大小

plane01_img = pygame.image.load(os.path.join("image",'plane03.png')).convert()
enemy_img = pygame.image.load(os.path.join("image",'plane01.png')).convert()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        self.image = pygame.transform.scale(plane01_img, (200, 120)) #調整圖片大小
        self.image.set_colorkey(WHITE)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = x
        self.rect.centery = y
        self.radius = 35   #圓型碰撞範圍半徑
        pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)    #畫出圓形
        self.speedx = 7    #圖片移動速度

    def update(self, x, y):
        self.image = pygame.transform.scale(plane01_img, (200, 120)) #調整圖片大小
        self.image.set_colorkey(WHITE)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = x
        self.rect.centery = y
        # 防止飛船超出視窗
        if self.rect.centerx < 0:
            self.rect.centerx = 0.1
        if self.rect.centerx >= WIDTH:
            self.rect.centerx = WIDTH
        if self.rect.centery < 0:
            self.rect.centery = 0.1
        if self.rect.centery >= HEIGHT:
            self.rect.centery = HEIGHT
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (140,100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 8

    def update(self, x,  y):
        self.image = pygame.transform.scale(enemy_img, (140,100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        # 防止飛船超出視窗
        if self.rect.centerx <= 0:
            self.rect.centerx = 0
        if self.rect.centerx >= WIDTH:
            self.rect.centerx = WIDTH
        if self.rect.centery <= 0:
            self.rect.centery = 0
        if self.rect.centery >= HEIGHT:
            self.rect.centery = HEIGHT