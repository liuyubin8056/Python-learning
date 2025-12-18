import sys 
import pygame
from time import sleep
import random

from settings import Settings
from game_stats import Gamestats
from ship import Ship
from bullet import Bullet
from alien import Alien
from blindbox import blindbox
from button import Button
from scoreboard import Scoreboard
 
class AlienInvasion: 
    """管理游戏资源和行为的类""" 

    def __init__(self): 
        """初始化游戏并创建游戏资源""" 
        pygame.init() 
        self.settings = Settings()
        self.stats=Gamestats(self)
        self.clock = pygame.time.Clock()
        #状态判断
        self.game_active=False
        self.game_firstTime=True
        self.open_settings=False
        self.custom=False

        # 先创建屏幕
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width 
        self.settings.screen_height = self.screen.get_rect().height 
        
        pygame.display.set_caption("Alien Invasion")
        
        # 然后创建需要屏幕的对象
        self._creat_buttons()
        self.ship = Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._creat_fleet()
        self.blindboxes=pygame.sprite.Group()
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
            elif event.type==pygame.MOUSEBUTTONDOWN and not self.game_active:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_Settings_button(mouse_pos)
                if self.open_settings:
                    self._check_low_difficulty_button(mouse_pos)
                    self._check_medium_difficulty_button(mouse_pos)
                    self._check_high_difficulty_button(mouse_pos)
                    self._check_custom_difficulty_button(mouse_pos)
                if self.custom:
                    self._check_alien_quantity_button(mouse_pos)
                    self._check_alien_speed_button(mouse_pos)
                    self._check_bullet_quantity_button(mouse_pos)
                    self._check_ship_speed_button(mouse_pos)
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
            self.open_settings=True
    def _check_low_difficulty_button(self,mouse_pos):
        """在玩家单击Low按钮时设置低难度"""
        button_clicked=self.low_difficulty_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.open_settings:
            self.custom=False
            self.settings.alien_quantity=16
            self.settings.ship_speed=2.0
            self.settings.alien_speed=0.5
            self.settings.bullets_allowed=5
            print("Low difficulty selected")
    def _check_medium_difficulty_button(self,mouse_pos):
        """在玩家单击Medium按钮时设置中等难度"""
        button_clicked=self.medium_difficulty_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.open_settings:
            self.custom=False
            self.settings.alien_quantity=24
            self.settings.ship_speed=1.5
            self.settings.alien_speed=1.0
            self.settings.bullets_allowed=4
            print("Medium difficulty selected")
    def _check_high_difficulty_button(self,mouse_pos):
        """在玩家单击High按钮时设置高难度"""
        button_clicked=self.high_difficulty_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.open_settings:
            self.custom=False
            self.settings.alien_quantity=32
            self.settings.ship_speed=1.0
            self.settings.alien_speed=1.5
            self.settings.bullets_allowed=3
            print("High difficulty selected")
    def _check_custom_difficulty_button(self,mouse_pos):
        """在玩家单击Custom按钮时设置自定义难度"""
        button_clicked=self.custom_difficulty_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.open_settings:
            self.custom = not self.custom
            if self.custom:
                print("Custom difficulty selected")
            else:
                print("Exited custom difficulty")
    def _check_alien_quantity_button(self,mouse_pos):
        """单击外星人数量按钮时更改外星人数量"""
        button_clicked=self.alien_quantity_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.custom:
            self.settings.alien_quantity+=4
            if self.settings.alien_quantity>32:
                self.settings.alien_quantity=8
            self.alien_quantity_button._prep_msg(f"Alien Quantity : {self.settings.alien_quantity}")
            print(f"Alien Quantity set to {self.settings.alien_quantity}")
    def _check_alien_speed_button(self,mouse_pos):
        """单击外星人速度按钮时更改外星人速度"""
        button_clicked=self.alien_speed_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.custom:
            self.settings.alien_speed+=0.5
            if self.settings.alien_speed>3.0:
                self.settings.alien_speed=0.5
            self.alien_speed_button._prep_msg(f"Alien Speed : {self.settings.alien_speed}")
            print(f"Alien Speed set to {self.settings.alien_speed}")
    def _check_bullet_quantity_button(self,mouse_pos):
        """单击子弹数量按钮时更改子弹数量"""
        button_clicked=self.bullet_quantity_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.custom:
            self.settings.bullets_allowed+=1
            if self.settings.bullets_allowed>6:
                self.settings.bullets_allowed=3
            self.bullet_quantity_button._prep_msg(f"Bullet Quantity : {self.settings.bullets_allowed}")
            print(f"Bullet Quantity set to {self.settings.bullets_allowed}")
    def _check_ship_speed_button(self,mouse_pos):
        """单击飞船速度按钮时更改飞船速度"""
        button_clicked=self.ship_speed_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.custom:
            self.settings.ship_speed+=0.5
            if self.settings.ship_speed>3.0:
                self.settings.ship_speed=1.0
            self.ship_speed_button._prep_msg(f"Ship Speed : {self.settings.ship_speed}")
            print(f"Ship Speed set to {self.settings.ship_speed}")
            

    def _creat_buttons(self):
        """创建所有按钮实例"""
        self.play_button=Button(self,"Play")
        self.settings_button=Button(self,"Settings")
        self.low_difficulty_button=Button(self,"Low")
        self.medium_difficulty_button=Button(self,"Medium")
        self.high_difficulty_button=Button(self,"High")
        self.custom_difficulty_button=Button(self,"Custom")
        self.alien_quantity_button=Button(self,f"Alien Quantity : {self.settings.alien_quantity}")
        self.alien_speed_button=Button(self,f"Alien Speed : {self.settings.alien_speed}")
        self.bullet_quantity_button=Button(self,f"Bullet Quantity : {self.settings.bullets_allowed}")
        self.ship_speed_button=Button(self,f"Ship Speed : {self.settings.ship_speed}")
        #调整按钮位置
        self.play_button.rect.y+=self.play_button.height+10
        self.settings_button.rect.y-=self.settings_button.height+10
        self.low_difficulty_button.rect.x-=self.low_difficulty_button.width+30
        self.medium_difficulty_button.rect.x-=self.medium_difficulty_button.width+30
        self.high_difficulty_button.rect.x-=self.high_difficulty_button.width+30
        self.custom_difficulty_button.rect.x-=self.custom_difficulty_button.width+30

        self.alien_quantity_button.rect.x+=self.alien_quantity_button.width+30
        self.alien_speed_button.rect.x+=self.alien_speed_button.width+30
        self.bullet_quantity_button.rect.x+=self.bullet_quantity_button.width+30
        self.ship_speed_button.rect.x+=self.ship_speed_button.width+30

        self.low_difficulty_button.rect.y-=self.low_difficulty_button.height*2+30
        self.medium_difficulty_button.rect.y-=self.medium_difficulty_button.height
        self.high_difficulty_button.rect.y+=self.high_difficulty_button.height
        self.custom_difficulty_button.rect.y+=self.custom_difficulty_button.height*2+30

        self.alien_quantity_button.rect.y-=self.alien_quantity_button.height*2+30
        self.alien_speed_button.rect.y-=self.alien_speed_button.height
        self.bullet_quantity_button.rect.y+=self.bullet_quantity_button.height
        self.ship_speed_button.rect.y+=self.ship_speed_button.height*2+30
        #自定义选项按钮加宽
        self.alien_quantity_button.rect.width=400
        self.alien_speed_button.rect.width=400
        self.bullet_quantity_button.rect.width=400
        self.ship_speed_button.rect.width=400
        #重新渲染按钮文本以适应新位置
        self.play_button._prep_msg("Play")
        self.settings_button._prep_msg("Settings")
        self.low_difficulty_button._prep_msg("Low")
        self.medium_difficulty_button._prep_msg("Medium")
        self.high_difficulty_button._prep_msg("High")
        self.custom_difficulty_button._prep_msg("Custom")
        self.alien_quantity_button._prep_msg(f"Alien Quantity : {self.settings.alien_quantity}")
        self.alien_speed_button._prep_msg(f"Alien Speed : {self.settings.alien_speed}")
        self.bullet_quantity_button._prep_msg(f"Bullet Quantity : {self.settings.bullets_allowed}")
        self.ship_speed_button._prep_msg(f"Ship Speed : {self.settings.ship_speed}")

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
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
            if random.random() < self.settings.blindbox_rate:
                new_blindbox=blindbox(self)
                new_blindbox.rect.x=collisions[list(collisions.keys())[0]][0].rect.x
                new_blindbox.rect.y=collisions[list(collisions.keys())[0]][0].rect.y
                self.blindboxes.add(new_blindbox)
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
    
    def _check_ship_blindbox_collision(self):
        """响应飞船和盲盒的碰撞"""
        collisions=pygame.sprite.spritecollide(self.ship,self.blindboxes,True)
        if collisions:
            if random.random() < 0.5:
                self.strenghten()
            else:
                self.weaken()

    def _creat_fleet(self):
        """创建一个外星人舰队"""
        #创建一个外星人，再不断添加，直到没有空间添加外星人为止
        #外星人的间距为外星人的宽度和高度
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        current_x,current_y=alien_width,alien_height
        while current_y < (self.settings.screen_height - 3*alien_height):
            while current_x < (self.settings.screen_width - 2*alien_width):
                if len(self.aliens)<self.settings.alien_quantity:
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
    
    def _update_blindboxes(self):
        """更新盲盒位置"""
        for blindbox in self.blindboxes.sprites():
            if blindbox.rect.bottom <= self.settings.screen_height:
                blindbox.rect.y += self.settings.blindbox_speed
        self._check_ship_blindbox_collision()
    
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
            sleep(1.0)
            self.game_active=False
            self.game_firstTime=True
            self.open_settings=False
            self.custom=False
            pygame.mouse.set_visible(True)
    
    def _update_screen(self):
        """更新图像"""
        self.screen.fill(self.settings.bg_color)
        if not self.game_active and not self.open_settings:
            self.play_button.drow_button()
            self.settings_button.drow_button()
        elif not self.game_active and self.open_settings and not self.custom:
            self.draw_definied_options()
            self.play_button.drow_button()
        elif not self.game_active and self.open_settings and self.custom:
            self.draw_definied_options()
            self.draw_custom_options()
            self.play_button.drow_button()
        else:
            self.draw_objects()
        pygame.display.flip()

    def draw_definied_options(self):
        """绘制难度选项"""
        self.low_difficulty_button.drow_button()
        self.medium_difficulty_button.drow_button()
        self.high_difficulty_button.drow_button()
        self.custom_difficulty_button.drow_button()
    def draw_custom_options(self):
        """绘制自定义选项"""
        self.alien_quantity_button.drow_button()
        self.alien_speed_button.drow_button()
        self.bullet_quantity_button.drow_button()
        self.ship_speed_button.drow_button()

    def draw_objects(self):
        """绘制游戏中的对象"""
        for bullet in self.bullets.sprites():
            bullet.darw_bullet()
        for blindbox in self.blindboxes.sprites():
            blindbox.screen.blit(blindbox.image, blindbox.rect)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()

    def update_objects(self):
        """更新游戏中的对象"""
        self.ship.update()
        self._update_bullets()
        self._update_aliens()
        self._update_blindboxes() 
 
    def _quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__': 
    # 创建游戏实例并运行游戏 
    ai = AlienInvasion() 
    ai.run_game()