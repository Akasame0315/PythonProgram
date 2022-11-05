from asyncio.windows_events import NULL
from pickle import FALSE, TRUE
import pygame
import Globals

WHITE = (255, 255, 255)

# font_name = pygame.font.match_font('arial')

#印出分數
def write_text(surf, text, size, x, y, color = WHITE, fontType = FALSE):
    if fontType == TRUE:    font = Globals.font_2
    else:   font = pygame.font.Font(Globals.font_name, size)
    text_surface = font.render(text, True, color)    #True是代表要用反鋸齒
    text_rect = text_surface.get_rect()
    text_rect.left = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)  #畫出文字