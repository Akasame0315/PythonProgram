import Globals
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        self.image = pygame.transform.scale(Globals.bullet_img, (30, 30)) #調整圖片大小
        self.image.set_colorkey(Globals.BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = x
        self.rect.centery = y
        self.radius = 15   #圓型碰撞範圍半徑
        pygame.draw.circle(self.image, Globals.WHITE, self.rect.center, self.radius)    #畫出圓形
        self.speedx = speed    #圖片移動速度

    def update(self):
        self.rect.centery += self.speedx

        #如果子彈超出螢幕視窗，就把該子彈刪掉
        if self.rect.bottom < 0:
            self.kill()