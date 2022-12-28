import pygame
import os
import random
import Globals

WIDTH = 1280
HEIGHT = 800

# 建立遊戲視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)

WHITE = (255,255,255)
BLACK = (0,0,0)

# 載入圖片
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("image",'DEF.png')).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("image",'atk.png')).convert()
power_imgs['shield'].set_colorkey(WHITE)
power_imgs['gun'].set_colorkey(WHITE)
power_imgs['shield'] = pygame.transform.scale(power_imgs['shield'], (50, 50))
power_imgs['gun'] = pygame.transform.scale(power_imgs['gun'], (50, 50))

class Power(pygame.sprite.Sprite):
    def __init__(self, center, speed):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.radius = 25
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.kill()
        elif self.rect.bottom <= 0:
            self.kill()