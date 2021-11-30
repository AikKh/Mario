import pygame
import random
import os
import sys
from Sound import Sound

class Mario(pygame.sprite.Sprite):
    
    right_index = 0
    left_index = 0
    
    jump_speed = 4
    falling_speed = 2
    jump_height = 27
    speed = 3
    
    right_run = []
    left_run = []
    
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'mario_imgs')
    
    stand_right = [pygame.image.load(os.path.join(img_folder, 'standing_right.png')), pygame.image.load(os.path.join(img_folder, 'standing_right(big).png'))]
    stand_left = [pygame.image.load(os.path.join(img_folder, 'standing_left.png')), pygame.image.load(os.path.join(img_folder, 'standing_left(big).png'))]
    run_right1 = [pygame.image.load(os.path.join(img_folder, 'run_right1.png')), pygame.image.load(os.path.join(img_folder, 'run_right1(big).png'))]
    run_right2 = [pygame.image.load(os.path.join(img_folder, 'run_right2.png')), pygame.image.load(os.path.join(img_folder, 'run_right2(big).png'))]
    run_left1 = [pygame.image.load(os.path.join(img_folder, 'run_left1.png')), pygame.image.load(os.path.join(img_folder, 'run_left1(big).png'))]
    run_left2 = [pygame.image.load(os.path.join(img_folder, 'run_left2.png')), pygame.image.load(os.path.join(img_folder, 'run_left2(big).png'))]
    jump_right = [pygame.image.load(os.path.join(img_folder, 'jump_right.png')), pygame.image.load(os.path.join(img_folder, 'jump_right(big).png'))]
    jump_left = [pygame.image.load(os.path.join(img_folder, 'jump_left.png')), pygame.image.load(os.path.join(img_folder, 'jump_left(big).png'))]
    falling_img = pygame.image.load(os.path.join(img_folder, 'falling.png'))
    none_img = pygame.image.load(os.path.join(img_folder, 'none.png'))
    
    
    right_run.append(run_right1)
    right_run.append(run_right2)
    
    left_run.append(run_left1)
    left_run.append(run_left2)
    
    #head_shot = Sound('head_shot.ogg')
    
    def __init__(self):
        self._type = 'plumber'
        self._sindex = 0
        self._gravity = 0
        self._jump_count = 0
        self.state = 'right'
        self.immortal = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = self.stand_right[self._sindex]
        self.rect = self.image.get_rect()
        self.rect.center = (300, 380)
        
    def switchSize(self, i: int):
        old_centre = self.rect.center
        self._sindex = i
        self.image = self.stand_right[self._sindex]
        self.rect.y -= 20
        self.rect = self.image.get_rect()
        self.rect.center = (old_centre[0], old_centre[1] - 15)
        
    def blinking(self):
        imgs = [self.image, self.none_img]
        self.image = imgs[self.immortal % 2]
        
    def jump(self):

        if self._gravity != 0:
            if self.state == 'right':
                self.image = self.jump_right[self._sindex]
            elif self.state == 'left':
                self.image = self.jump_left[self._sindex]
                
        if self._gravity == 0:
            pass
        elif self._gravity > 0:
            self.rect.y -= self.jump_speed
            self._gravity -= 1
                
        return self._gravity > 0
                
        
    def move(self, dir: str):
        if dir == 'right':
            self.state = 'right'
            self.right_index += 1
            if self._gravity == 0:
                self.image = self.right_run[(self.right_index//6) % len(self.right_run)][self._sindex]
        elif dir == 'left':
            self.state = 'left'
            self.left_index += 1
            if self._gravity == 0:
                self.image = self.left_run[(self.left_index//6) % len(self.left_run)][self._sindex]
            
    def stop(self, dir: str):
        if dir == 'right':
            self.right_index = 0
            self.image = self.stand_right[self._sindex]
        elif dir == 'left':
            self.left_index = 0
            self.image = self.stand_left[self._sindex]
            
    def falling(self):
        if self._type == 'plumber':
            if self.state == 'right':
                self.image = self.jump_right[self._sindex]
                self.rect.y += self.falling_speed
            elif self.state == 'left':
                self.image = self.jump_left[self._sindex]
                self.rect.y += self.falling_speed
        else:
            self.image = self.falling_img
            self.rect.y += self.falling_speed

    def die(self):
        self._type = 'dead_mario'
        self.falling()
        if self.rect.top > 450:
            pygame.quit()
            sys.exit()