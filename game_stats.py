from pathlib import Path 
import json 

class Gamestats:
    """跟踪游戏的统计信息"""

    def __init__(self,ai_game):
        """初始化统计信息"""
        self.settings=ai_game.settings
        self.load_high_score()
        self.reset_stats()
    
    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left=self.settings.ship_limit
        self.score=0
        self.level=1
    
    def load_high_score(self):
        """从文件加载最高分"""
        high_score_path=Path('high_score.json')
        if high_score_path.exists():
            with high_score_path.open('r',encoding='utf-8') as f:
                high_score_data=json.load(f)
                self.high_score=high_score_data.get("high_score",0)
        else:
            self.high_score=0
    def save_high_score(self):
        """将最高分保存到文件"""
        high_score_data={"high_score":self.high_score}
        high_score_path=Path('high_score.json')
        with high_score_path.open('w',encoding='utf-8') as f:
            json.dump(high_score_data,f,indent=4)