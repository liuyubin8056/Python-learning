import pygame.font 
 
class Button: 
    """为游戏创建按钮的类""" 
 
    def __init__(self, ai_game, msg): 
        """初始化按钮的属性""" 
        self.screen = ai_game.screen 
        self.screen_rect = self.screen.get_rect() 
        # 设置按钮的尺寸和其他属性 
        self.width, self.height = 200, 50 
        self.button_color = (0, 135, 0) 
        self.text_color = (255, 255, 255) 
        self.font = pygame.font.SysFont(None, 48)

    def creat_rect(self, msg):
        """创建按钮的 rect 对象，并使其居中"""
        self.rect = pygame.Rect(0, 0, self.width, self.height) 
        self.rect.center = self.screen_rect.center 
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center

    def drow_button(self):
        """绘制一个用颜色填充的按钮，再填充文本"""
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

class Play_Button(Button):
    """开始游戏按钮"""
    def __init__(self,ai_game,msg):
        super().__init__(ai_game,msg)
        self.creat_rect(msg)
        self.rect.y+=self.height+10
        
       
class Settings_Button(Button):
    """设置按钮"""
    def __init__(self,ai_game,msg):
        super().__init__(ai_game,msg)
        self.creat_rect(msg)
        self.rect.y+=self.height-10
        

class Low_Difficulty_Button(Button):
    """低难度按钮"""
    def __init__(self,ai_game,msg):
        super().__init__(ai_game,msg)
        self.rect.x-=self.width+30
        self.rect.y-=self.height+10
        self.creat_rect(msg)
class Medium_Difficulty_Button(Button):
    """中等难度按钮"""
    def __init__(self,ai_game,msg):
        super().__init__(ai_game,msg)
        self.rect.x-=self.width+30
        self.rect.y-=self.height*2+10
        self.creat_rect(msg)
class High_Difficulty_Button(Button):
    """高难度按钮"""
    def __init__(self,ai_game,msg):
        super().__init__(ai_game,msg)
        self.rect.x-=self.width+30
        self.rect.y+=self.height+10
        self.creat_rect(msg)
class Custom_Difficulty_Button(Button):
    """自定义难度按钮"""
    def __init__(self,ai_game,msg):
        super().__init__(ai_game,msg)
        self.rect.x-=self.width+30
        self.rect.y+=self.height*2+10
        self.creat_rect(msg)

class Alien_Speed_Inuput_Button(Button):
    """外星人速度输入按钮"""
    def __init__(self,ai_game,msg):
        super().__init__(ai_game,msg)
        self.rect.x+=self.width+30
        self.rect.y-=self.height+10
        self.creat_rect(msg)
class Bullet_Quantity_Input_Button(Button):
    """子弹数量输入按钮"""
    def __init__(self,ai_game,msg):
        super().__init__(ai_game,msg)
        self.rect.x+=self.width+30
        self.rect.y-=self.height*2+10
        self.creat_rect(msg)
class Ship_Speed_Input_Button(Button):
    """飞船速度输入按钮"""
    def __init__(self,ai_game,msg):
        super().__init__(ai_game,msg)
        self.rect.x+=self.width+30
        self.rect.y+=self.height+10
        self.creat_rect(msg)