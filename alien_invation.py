import sys 
import pygame
from time import sleep

from settings import Settings
from game_stats import Gamestats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button,Play_Button,Settings_Button
from scoreboard import Scoreboard
 
class AlienInvasion: 
    """管理游戏资源和行为的类""" 

    def __init__(self): 
        """初始化游戏并创建游戏资源""" 
        pygame.init() 
        self.settings = Settings()
        self.stats=Gamestats(self)
        self.clock = pygame.time.Clock()
        #游戏一开始处于非活动状态
        self.game_active=False
        self.game_firstTime=True

        # 先创建屏幕
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width 
        self.settings.screen_height = self.screen.get_rect().height 
        
        pygame.display.set_caption("Alien Invasion")
        
        # 然后创建需要屏幕的对象
        self.ship = Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._creat_fleet()

        self.play_button=Button(self,"Play")
        self.settings_button=Button(self,"Settings")
        
        self.play_button.creat_rect("Play")
        self.settings_button.creat_rect("Settings")
        self.play_button.rect.y+=self.play_button.height+10
        self.settings_button.rect.y-=self.settings_button.height+10
        
        self.sb=Scoreboard(self)
 
    def run_game(self): 
        """开始游戏的主循环""" 
        while True: 
            self._check_events()
            self._update_screen()
            if self.game_active and self.game_firstTime:
                sleep(1.0)
                self.game_firstTime=False
                self.update_objects()
            elif self.game_active and not self.game_firstTime:
                self.update_objects()
            self.clock.tick(240)
    
    def _check_events(self):
        # 侦听键盘和鼠标事件 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                self._quit_game()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    def _check_keydown_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_ESCAPE:
            self._quit_game()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        if event.key==pygame.K_LEFT: 
            self.ship.moving_left=False
    def _check_play_button(self,mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            #重置游戏的统计信息
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active=True
            #清空外星人和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            #创建一个新的外星舰队，并将飞船放置在屏幕底部中央
            self._creat_fleet()
            self.ship.center_ship()
            #隐藏光标
            pygame.mouse.set_visible(False)
    def _check_Settings_button(self,mouse_pos):
        """在玩家单击Settings按钮时显示设置页面"""
        button_clicked=self.settings_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #显示设置页面的代码待添加
            pass

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowde:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹位置并删除已消失的子弹"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisiong()
        
    def _check_bullet_alien_collisiong(self):
        """响应子弹和外星人的碰撞"""
        #检查是否有子弹击中了敌人，如果是，删除子弹和外星人
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #删除现有的子弹并创建一个新的外星舰队
            self.bullets.empty()
            self._creat_fleet()
            self.settings.increase_speed()
            #提高等级
            self.stats.level+=1
            self.sb.prep_level()

    def _creat_fleet(self):
        """创建一个外星人舰队"""
        #创建一个外星人，再不断添加，直到没有空间添加外星人为止
        #外星人的间距为外星人的宽度和高度
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        current_x,current_y=alien_width,alien_height
        while current_y < (self.settings.screen_height - 3*alien_height):
            while current_x < (self.settings.screen_width - 2*alien_width):
                self._creat_alien(current_x,current_y)
                current_x+=2*alien_width
            current_x=alien_width
            current_y+=2*alien_height
    def _creat_alien(self,x_position,y_position):
        """创建一个外星人并将其加入外星舰队"""
        new_alien=Alien(self)
        new_alien.x=x_position
        new_alien.rect.x=x_position
        new_alien.rect.y=y_position
        self.aliens.add(new_alien)
    
    def _check_fleet_edges(self):
        """在所有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_driection()
                break
    def _change_fleet_driection(self):
        """将整个舰队向下移动，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新外形舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        #检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
            print("Man!")
        #检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()
    
    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left>1:
            #剩余飞船-1
            self.stats.ships_left-=1
            self.sb.prep_ships()
            #清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            #创建一个新的外星舰队，并将飞船放置在屏幕底部中央
            self._creat_fleet()
            self.ship.center_ship()
            #暂停
            sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)
    
    def _update_screen(self):
        """更新图像"""
        self.screen.fill(self.settings.bg_color)
        if not self.game_active:
            self.play_button.drow_button()
            self.settings_button.drow_button()
        else:
            self.draw_objects()
        pygame.display.flip()

    def draw_objects(self):
        """绘制游戏中的对象"""
        for bullet in self.bullets.sprites():
            bullet.darw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()

    def update_objects(self):
        """更新游戏中的对象"""
        self.ship.update()
        self._update_bullets()
        self._update_aliens()   
 
    def _quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__': 
    # 创建游戏实例并运行游戏 
    ai = AlienInvasion() 
    ai.run_game()