import pygame
from pygame.sprite import Sprite

class Ship(Sprite): 
    """管理飞船的类""" 
    def __init__(self, ai_game): 
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.setting=ai_game.settings
        self.screen = ai_game.screen 
        self.screen_rect = ai_game.screen.get_rect()
        # 加载飞船图像、调整大小并获取其外接矩形 
        self.image = pygame.image.load('images/ship.bmp') 
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.x=float(self.rect.x)
        # 每艘新飞船都放在屏幕底部的中央 
        self.rect.midbottom = self.screen_rect.midbottom
        #移动标志
        self.moving_right=False
        self.moving_left=False

    def center_ship(self):
        """将飞船放置在底部中央"""
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)

    def update(self):
        #根据移动标志调整飞船位置
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x+=self.setting.ship_speed
        if self.moving_left and self.rect.left > 0:
            if self.setting.ship_speed-int(self.setting.ship_speed)==0:
                self.rect.x-=self.setting.ship_speed
            else:
                self.rect.x-=self.setting.ship_speed+1
            
    def blitme(self): 
        """在指定位置绘制飞船""" 
        self.screen.blit(self.image, self.rect)