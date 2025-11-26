import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船所发射子弹的类"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen 
        self.settings = ai_game.settings 
        self.color = self.settings.bullet_color
        #(0,0)创建一个表示子弹的矩形
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop
        #用浮点数表示子弹的位置
        self.y=float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        self.y-=self.settings.bullet_speed
        self.rect.y=self.y
    
    def darw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)