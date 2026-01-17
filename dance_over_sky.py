import sys
import pygame
import time

from settings import Settings
from air_object import Air_Object

class Dance_over_sky:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        #先创建屏幕
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Dance Over Sky")
        #再创建需要屏幕的对象
        self.air_object=Air_Object(self)
        #判断状态
        self.game_active=False

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(self.settings.tick)

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_keydown_events(self, event):
        """响应按键按下"""
        if event.key==pygame.K_q:
            self.air_object.turn_left=True
        elif event.key==pygame.K_e:
            self.air_object.turn_right=True
    def _check_keyup_events(self, event):
        """响应按键松开"""
        if event.key==pygame.K_q:
            self.air_object.turn_left=False
        elif event.key==pygame.K_e:
            self.air_object.turn_right=False

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.air_object.update(1.0/self.settings.tick)
        self.air_object.draw()
        pygame.display.flip()
    
    def quit_game(self):
        """退出游戏"""
        pygame.quit()
        sys.exit()

if __name__ == '__main__': 
    # 创建游戏实例并运行游戏 
    ai = Dance_over_sky() 
    ai.run_game()