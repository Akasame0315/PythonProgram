import os
import pygame
import handIdentify
import threading
import Globals
import time

Globals.initial()
pygame.init()
screen = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))   #設定視窗大小
pygame.display.set_caption("modeswitch")   #視窗名稱creen = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))   #設定視窗大小

runnning = True
chooseMode = 0

def main():
    global runnning, chooseMode
    
    screen.blit(pygame.transform.scale(Globals.tutorial_img, (Globals.WIDTH, Globals.HEIGHT)), (0, 0))
    pygame.display.flip()
    pygame.display.update()
    # Globals.cameraNum = 1
    handControl = threading.Thread(target=handIdentify.modeswitch)
    handControl.start()
    while runnning:
        print("RText " + handIdentify.Rtext)
        print("LText " + handIdentify.Ltext)
        if handIdentify.Rtext == '1':   #單人模式
            chooseMode = 1
        #    print("單人模式")
            screen.blit(pygame.transform.scale(Globals.tutorial2_img, (Globals.WIDTH, Globals.HEIGHT)), (0, 0))
            pygame.display.flip()
            pygame.display.update()
        if chooseMode == 1:
            if handIdentify.Rtext == '3':
                Globals.controlMode = 3
                pygame.quit()
                os.system(".\OnePerson\Level_1.py")
                return 0
            elif handIdentify.Rtext == '4':
                Globals.controlMode = 4
                pygame.quit()
                os.system(".\OnePerson\Level_1_body.py")
                return 0
        elif handIdentify.Rtext == '2': #連線模式
            chooseMode = 2
            screen.blit(pygame.transform.scale(Globals.tutorial3_img, (Globals.WIDTH, Globals.HEIGHT)), (0, 0))
            pygame.display.flip()
            pygame.display.update()
        if chooseMode == 2:
            if handIdentify.Rtext == '3' and handIdentify.Ltext == '3': #連線模式建立房間
                Globals.controlMode = 3
                pygame.quit()
                os.system(".\server.py")
                runnning = False
                return 0
            elif handIdentify.Rtext == '3' and handIdentify.Ltext == '4':
                Globals.controlMode = 3
                pygame.quit()
                os.system(".\client.py")
                runnning = False
                return 0
            elif handIdentify.Rtext == '4' and handIdentify.Ltext == '3': #連線模式加入房間
                Globals.controlMode = 4
                pygame.quit()
                print(".\serverBody!")
                runnning = False
                return 0
            elif handIdentify.Rtext == '4' and handIdentify.Ltext == '4':
                Globals.controlMode = 4
                pygame.quit()
                os.system(".\clientBody.py")
                runnning = False
                return 0
        elif handIdentify.Rtext == '8':
            runnning = False
            # break
            return 0

        time.sleep(0.001)
main()