import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite
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
        self.mass=1000
        self.drag_coefficient=0.47  #阻力系数
        self.area=0.1  #迎风面积，m^2
        self.max_g=10.0  #最大承受过载，g
        #初始状态
        self.position=Vector2(0,300)
        self.velocity=Vector2.from_angle(0)*0.0
        self.acceleration=Vector2.from_angle(0)*0.0
        self.forces=Vector2.from_angle(0)*0.0
        self.angle_deg=0.0  #飞行物朝向角度，度
        self.attack_angle_deg=0.0  #迎角，度

    def update_position(self, dt):
        """根据受力更新加速度、速度和位置"""
        self.update_forces()
        self.acceleration=self.forces/self.mass
        self.velocity+=self.acceleration*dt
        self.position+=self.velocity*dt
        self.rect.x=self.position.x/10
        self.rect.y=self.position.y/10
    def update_forces(self):
        """计算合力"""
        air_density=1.225  #空气密度 kg/m^3
        v_mag=self.velocity.length()
        self.attack_angle_deg=self.angle_diff_deg(self.angle_deg,self.velocity.angle_to(Vector2(1,0))) if v_mag>0 else 0.0
        #阻力
        if v_mag>0:
            drag_magnitude=0.5*air_density*self.drag_coefficient*self.area*v_mag**2
            drag_direction=-self.velocity.normalize()
            drag=drag_direction*drag_magnitude
        else:
            drag=Vector2(0,0)
        #升力（简化模型，仅与迎角相关）
        lift_coefficient=2*math.pi*self.deg_to_rad(abs(self.attack_angle_deg))  #小迎角近似
        lift_magnitude=0.5*air_density*lift_coefficient*self.area*v_mag**2
        if v_mag>0 and self.attack_angle_deg>0:
            lift_direction=Vector2(-self.velocity.y, self.velocity.x).normalize()
        elif v_mag>0 and self.attack_angle_deg<0:
            lift_direction=Vector2(self.velocity.y, -self.velocity.x).normalize()
        else:
            lift_direction=Vector2(0,0)
        lift=lift_direction*lift_magnitude
        #合力
        self.forces=drag+lift


    #--- 以下为辅助函数，用于角度计算 ---
    def normalize_angle_deg(self,angle_deg):
        """将角度规整到[-180, 180]度范围"""
        angle_deg = angle_deg % 360
        if angle_deg > 180:
            angle_deg -= 360
        return angle_deg
    def angle_diff_deg(self, a, b):
        """计算两个角度（度）之间的最小差值"""
        diff = self.normalize_angle_deg(a - b)
        return diff
    def deg_to_rad(self, deg):
        return deg * math.pi / 180.0
    def rad_to_deg(self, rad):
        return rad * 180.0 / math.pi