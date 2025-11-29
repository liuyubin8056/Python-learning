import sys 
import pygame
from time import sleep

from settings import Settings
from game_stats import Gamestats
from ship import Ship
from bullet import Bullet
from alien import Alien
 
class AlienInvasion: 
    """管理游戏资源和行为的类""" 

    def __init__(self): 
        """初始化游戏并创建游戏资源""" 
        pygame.init() 
        self.settings = Settings()
        self.stats=Gamestats(self)
        self.clock = pygame.time.Clock()
        self.game_active=True

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
 
    def run_game(self): 
        """开始游戏的主循环""" 
        while True: 
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_screen()       
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
        if not self.aliens:
            #删除现有的子弹并创建一个新的外星舰队
            self.bullets.empty()
            self._creat_fleet()

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
                self._ship_hit
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
    
    def _update_screen(self):
        #更新图像
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.darw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()
 
    def _quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__': 
    # 创建游戏实例并运行游戏 
    ai = AlienInvasion() 
    ai.run_game()