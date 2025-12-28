import pygame

class Audio:
    def __init__(self):
        self.sounds = self.load_sounds()
        self.bg_music=pygame.mixer.Sound('auido/bg_music.ogg')
        #音量管理
        self.music_volume = 0.5
        self.sound_volume = 0.3
        self.music_enabled = True
        self.sounds_enabled = True

    def load_sounds(self):
        """预加载所有音效"""
        sounds = {}
        sound_files = {
            'shoot': 'auido/yu~.wav',
            'hit': 'auido/bong.wav',
            'injury': 'auido/man.wav',
            'lucky_box' : 'auido/nice.wav',
            'unlucky_box' : 'auido/gaobili.wav',
            'game_over' : 'auido/hihihi.wav'
        }
        for name, file in sound_files.items():
            sounds[name] = pygame.mixer.Sound(file)
        return sounds
    
    def play_sound(self, name):
        """播放指定音效"""
        if self.sounds_enabled and name in self.sounds:
            sound = self.sounds[name]
            sound.set_volume(self.sound_volume)
            sound.play()
    def play_bg_music(self):
        """播放背景音乐"""
        if self.music_enabled:
            self.bg_music.set_volume(self.music_volume)
            self.bg_music.play(loops=-1)  # 无限循环播放