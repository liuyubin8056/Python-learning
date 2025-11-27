class Settings: 
    """存储游戏《外星人入侵》中所有设置的类""" 
    def __init__(self): 
        """初始化游戏的设置""" 
        # 屏幕设置 
        self.screen_width = 1200 
        self.screen_height = 800 
        self.bg_color = (30, 120, 200)
        self.bullets_allowde=3
        self.ship_speed=1.5
         # 子弹设置
        self.bullet_speed = 2.0 
        self.bullet_width = 3 
        self.bullet_height = 15 
        self.bullet_color = (60, 60, 60)