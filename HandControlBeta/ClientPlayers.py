import pygame
import Globals

Globals.initial()
originx = Globals.ClientX
enemyx = Globals.ClientEnemy

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global originx
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        self.image = pygame.transform.scale(Globals.plane03_img, (Globals.planesize_large)) #調整圖片大小
        self.image.set_colorkey(Globals.WHITE)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = originx
        self.rect.centery = y
        self.radius = 20   #圓型碰撞範圍半徑
        # pygame.draw.circle(self.image, Globals.WHITE, self.rect.center, self.radius)    #畫出圓形
        self.speedx = 7    #圖片移動速度
        
    def animate(self, move, x, y, power):
        if power == 'shield':
            if move-self.rect.centerx > 0:
                self.image = pygame.transform.scale(Globals.plan03LSH_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背

            elif move-self.rect.centerx < 0:
                self.image = pygame.transform.scale(Globals.plane03RSH_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背
            else:   
                self.image = pygame.transform.scale(Globals.plane03SH_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背
        else:
            if move-self.rect.centerx > 0:
                self.image = pygame.transform.scale(Globals.plan03L_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背

            elif move-self.rect.centerx < 0:
                self.image = pygame.transform.scale(Globals.plane03R_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背
            else:   
                self.image = pygame.transform.scale(Globals.plane03_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背
        
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
        if self.rect.bottom >= Globals.lineRect:
            self.rect.bottom = Globals.lineRect
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Globals.plane04_img, (Globals.planesize_large))
        self.image.set_colorkey(Globals.BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 7

    def update(self, x,  y):
        self.image = pygame.transform.scale(Globals.plane04_img, (Globals.planesize_large))
        self.image.set_colorkey(Globals.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def animate(self, x, y, power):
        global enemyx
        if power == 'shield':
            if(x > enemyx):
                self.image = pygame.transform.scale(Globals.plane04RSH_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背
            elif(x < enemyx):
                self.image = pygame.transform.scale(Globals.plan04LSH_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背
            else:
                self.image = pygame.transform.scale(Globals.plane04SH_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背
        else:
            if(x > enemyx):
                self.image = pygame.transform.scale(Globals.plane04R_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背
            elif(x < enemyx):
                self.image = pygame.transform.scale(Globals.plan04L_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.WHITE)    #圖片去背
            else:
                self.image = pygame.transform.scale(Globals.plane04_img, (Globals.planesize_large)) #調整圖片大小
                self.image.set_colorkey(Globals.BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = x
        self.rect.centery = y
        enemyx = x
        Globals.ClientEnemy = enemyx