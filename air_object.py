import pygame
import math

class AirObject:
    """模拟飞行物力学特征的类"""

    def __init__(self,ai_game):
        """初始化飞行物的属性"""
        #图像属性
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.image = pygame.image.load('images/ship.bmp') 
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        #动力学特性
        self.mass=1.0
        #self.velocity=Vector2.from_angle(0)*0.0
    def update_position(self, dt):
        """根据受力更新加速度、速度和位置"""
        
        self.rect.x=self.x/10
        self.rect.y=self.y/10
    def update_forces(self):
        """计算合力"""
