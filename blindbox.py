import pygame
from pygame.sprite import Sprite

class Blindbox(Sprite):
    """掉落盲盒"""

    def __init__(self,ai_game):
        super().__init__()
        self.settings=ai_game.settings
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        #加载盲盒图像,调整大小并设置其 rect 属性
        self.image = pygame.image.load('images/blindbox.jpg')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        #每个盲盒最初都在屏幕的左上角附近
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
    
    def strengthen(self):
        """幸运盲盒"""
        self.settings.ship_speed+=1
        self.settings.bullets_allowed+=2
    def weaken(self):
        """不幸盲盒"""
        if self.settings.ship_speed>1.5:
            self.settings.ship_speed-=1
        if self.settings.bullets_allowed>1:
            self.settings.bullets_allowed-=1