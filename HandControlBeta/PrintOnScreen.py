from asyncio.windows_events import NULL
import pygame
import Globals

WHITE = (255, 255, 255)

# font_name = pygame.font.match_font('arial')

#印出分數
def write_text(surf, text, size, x, y, color = WHITE):
    font = pygame.font.Font(Globals.font_name, size)
    text_surface = font.render(text, True, color)    #True是代表要用反鋸齒
    text_rect = text_surface.get_rect()
    text_rect.left = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)  #畫出文字

def center_line(surf, move):
    # line_y = Globals.HEIGHT/2 + move # y軸位置
    line_y = move
    if line_y <= 140: line_y = 140
    elif line_y >= 660: line_y = 660
    line_rect = pygame.Rect(0, line_y, Globals.WIDTH, 2)    # 界線位置
    # line_rect_player = pygame.Rect(0, 660, 40, 20)
    # line_rect_enemy = pygame.Rect(Globals.WIDTH-40, 120, 40, 20)
    # 畫出來
    pygame.draw.rect(surf, Globals.RED, line_rect)
    Globals.lineRect = line_y
    # pygame.draw.rect(surf, Globals.ROSE, line_rect_player)
    # pygame.draw.rect(surf, Globals.ROSE, line_rect_enemy)