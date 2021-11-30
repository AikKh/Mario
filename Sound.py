import pygame
import os
import sys

class Sound(pygame.mixer.Sound):
    
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    
    game_folder = os.path.dirname(__file__)
    sound_folder = os.path.join(game_folder, 'mario_sounds')
    #sound = pygame.mixer.music.load(os.path.join(sound_folder, 'head_shot.ogg'))
    
    def init(self, name: str):
        #pygame.mixer.Sound.__init__(self)
        self.adress = 'C:\\Projects\\Games\\Mario\\mario_sounds\\{}'.format(name)#os.path.join(self.sound_folder, name)
        self.sound = pygame.mixer.music.load(name)
    
    def playSound(self):
        self.sound.play()
        
        
#print(Sound('head_shot.ogg').adress)
#sound = Sound('head_shot.ogg')
#sound.playSound()