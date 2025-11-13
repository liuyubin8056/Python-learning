class Roommate:
    def __init__(self, name, food, san):
        self.food = food
        self.san = san
        self.name = name
    
    def eat(self):
        if self.food <= 5:
            while self.food <= 8:
                self.food += 1
            print(f"{self.name}干饭，现在饱食度吃到了{self.food}")
        if self.food >= 10:
            print("吃吃吃，就知道吃")
    
    def game(self):
        self.san += 2
        print(f"{self.name}玩游戏，san值增加到{self.san}")
    
    def gotoBed(self):
        self.san += 100
        print(f"{self.name}睡觉，san值增加到{self.san}")
    
    def exercise(self):
        print("锻炼？练个p！")
        self.gotoBed()  # 调用自己的方法

roommate_1=Roommate('zhou',5,100)
roommate_1.eat()
roommate_2=Roommate('jin',2,100)
roommate_2.game()
roommate_3=Roommate('zhang',10,20)
roommate_3.exercise()


class Superroommate(Roommate):
    def __init__(self,name,food,san):
        super().__init__(name,food,san)
    def showtime(self):
        print(f"{self.name}驾到统统闪开！(没想到吧我的顶级室友不需要吃饭睡觉打游戏)")

roommate_4=Superroommate('aaa',0,0)
roommate_4.showtime()