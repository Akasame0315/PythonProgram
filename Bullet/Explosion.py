import Globals
import pygame
import time

class Explosion(pygame.sprite.Sprite):
    def __init__(self, centerx, centery ):
        pygame.sprite.Sprite.__init__(self)
        self.image = Globals.expolose2_img
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.centerx  = centerx
        self.rect.centery  = centery
        # self.frame = 0  #更新到第幾張圖片
        # self.last_update = pygame.time.get_ticks()  #紀錄最後更新圖片的時間
        # self.frame_rate = 50  #經過幾毫秒更新圖片

    def update(self):
        self.kill()
    # def update(self):
    #     now = pygame.time.get_ticks()
    #     if now - self.last_update > self.frame_rate:
    #         self.last_update = now
    #         self.frame += 1
    #         if self.frame == len(expl_anim[self.size]):
    #             self.kill()
    #         else:
    #             self.image = expl_anim[self.size][self.frame]
    #             center = self.rect.center
    #             self.rect = self.image.get_rect()
    #             self.rect.center = center