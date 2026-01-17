import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite
import math

class Air_Object:
    """模拟飞行物力学特征的类"""

    def __init__(self,ai_game):
        """初始化飞行物的属性"""
        #图像属性
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.original_image = pygame.image.load('images/f-16.jpg') 
        self.original_image = pygame.transform.scale(self.original_image, (50, 30))
        self.image = self.original_image.copy()  # 保存原图，避免质量下降
        self.rect = self.image.get_rect()
        self.rect.left = self.screen_rect.left
        self.rect.centery = self.screen_rect.centery

        #动力学特性
        self.mass=10000
        self.drag_coefficient=0.47  #阻力系数
        self.area=1  #迎风面积，m^2
        self.max_g=10.0  #最大承受过载，g
        #初始状态
        self.position=Vector2(0,self.screen_rect.height*10/2)  #位置，单位：m
        self.velocity = Vector2(200.0, 0)  # 初始速度向右200m/s
        self.acceleration = Vector2(0, 0)
        self.forces = Vector2(0, 0)
        self.angle_deg=0.0  #飞行物朝向角度，度
        self.attack_angle_deg=0.0  #迎角，度
        #动作状态
        self.turn_left=False
        self.turn_right=False
   
    def update_angle(self):
        """根据当前速度方向更新飞行物朝向角度"""
        if self.turn_left:
            self.rotate(-2.0)
        if self.turn_right:
            self.rotate(2.0)
    def update_position(self, dt):
        """根据受力更新加速度、速度和位置"""
        self.update_forces()
        self.acceleration=self.forces/self.mass
        self.check_g_limit()
        self.velocity+=self.acceleration*dt
        self.position+=self.velocity*dt
        self.rect.x=self.position.x/10
        self.rect.y=self.position.y/10

    def update_forces(self):
        """计算合力"""
        air_density=0.660  #6000m海拔空气密度 kg/m^3
        v_mag=self.velocity.length()
        self.attack_angle_deg=self.angle_diff_deg(self.angle_deg,self.velocity.angle_to(Vector2(1,0))) if v_mag>0 else 0.0
        drag=self.get_drag(v_mag,air_density)
        lift=self.get_lift(v_mag,air_density)
        trust=self.get_trust(self.velocity.length())
        self.forces=drag+lift+trust
        
    def get_drag(self,v_mag,air_density):
        """计算阻力"""
        if v_mag>0:
            drag_magnitude=0.5*air_density*self.drag_coefficient*self.area*v_mag**2
            drag_direction=-self.velocity.normalize()
            drag=drag_direction*drag_magnitude
        else:
            drag=Vector2(0,0)
        return drag
    def get_lift(self,v_mag,air_density):
        """计算升力"""
        lift_coefficient=2*math.pi*self.deg_to_rad(abs(self.attack_angle_deg))  #小迎角近似
        lift_magnitude=0.5*air_density*lift_coefficient*self.area*v_mag**2
        if v_mag>0 and self.attack_angle_deg>0:
            lift_direction=Vector2(-self.velocity.y, self.velocity.x).normalize()
        elif v_mag>0 and self.attack_angle_deg<0:
            lift_direction=Vector2(self.velocity.y, -self.velocity.x).normalize()
        else:
            lift_direction=Vector2(0,0)
        lift=lift_direction*lift_magnitude
        return lift
    def get_trust(self,v):
        """获取推力向量"""
        thrust_magnitude=68646.55+102.34*v-0.125*v**2+2.12e-4*v**3-1.87e-7*v**4+4.92e-11*v**5
        thrust_direction=Vector2.from_polar((self.deg_to_rad(self.angle_deg),1))
        return thrust_direction*thrust_magnitude
    def check_g_limit(self):
        """检查最大过载，限制机动"""
        g_force=self.acceleration.length()/9.81
        if g_force>self.max_g:
            pass

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
    
    def rotate(self, delta_angle_deg):
        """旋转飞行物，改变其朝向角度"""
        self.angle_deg=self.normalize_angle_deg(self.angle_deg+delta_angle_deg)
        self.image = pygame.transform.rotate(self.original_image, -delta_angle_deg)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt):
        """更新飞行物状态"""
        self.update_angle()
        self.update_position(dt)
        print(f"Velocity: {self.velocity}, Acceleration: {self.acceleration}, Angle: {self.angle_deg}, Attack Angle: {self.attack_angle_deg}")
    def draw(self):
        """在屏幕上绘制飞行物"""
        self.screen.blit(self.image, self.rect)