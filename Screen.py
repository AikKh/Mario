import pygame
from pygame.locals import *
import os
import sys, time
from Mario import Mario
from BarrierSprites import Barrier
from Coin import Coin
from Mobs import Mush, EdibleMush


class Screen():
    
    white = (0, 0, 0)
    
    width = 600
    height = 450
    
    fps = 60

    time = 400
    time_score = 0
    
    myfont = pygame.font.SysFont("monospace", 16)
    
    time_text = None
    coins_text = None
    live_text = None
    score_text = None
    
    killed_mobs = []
    
    running = True
    
    class Background(pygame.sprite.Sprite):
        bgs = ['all_bg.png', 'main_bg_2.png']
        def __init__(self, location: list):
            self._location = location
            self._type = 'bg'
            pygame.sprite.Sprite.__init__(self)
            game_folder = os.path.dirname(__file__)
            img_folder = os.path.join(game_folder, 'walls_imgs')
            self.image = pygame.image.load(os.path.join(img_folder, self.bgs[1]))
            self.rect = self.image.get_rect()
            self.rect.center = location
            
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mario")
    
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    start_pos = None
    
    mario = Mario()
    bg = Background([960, 225])
    all_sprites.add(bg)
    all_sprites.add(mario)

            
    def bgMove(self, dir: str):
        if not self.touchValidate(self.mario, dir):
            for sprite in self.all_sprites:
                if sprite == self.mario:
                        continue
                elif dir == 'right':
                    sprite.rect.x -= self.mario.speed
                elif dir == 'left':
                    sprite.rect.x += self.mario.speed
                    
    def restart(self):
        time.sleep(1)
        self.mario.coins = 0
        self.mario.score = 0
        self.mario.rect.y = 380
        self.mario.switchSize(0)
        self.time = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.mario._type = 'plumber'
        self.mario.lives -= 1
        self.all_sprites = self.start_pos
        for spr in self.all_sprites:
            spr.rect.center = spr._location
        
                         
                    
    def marioDeadValidate(self):
        if self.mario.rect.top > self.height:
            self.mario._type = 'dead_mario'
        if self.mario.immortal > 0:
            self.mario.immortal -= 1
            self.mario.blinking()
        elif self.mario._type == 'dead_mario':
            self.mario.die()
            if self.mario.rect.top > self.height:
                self.running = False
                    
    def headValidate(self):
        for sprite in self.all_sprites:
            if sprite == self.mario or sprite == self.bg:
                continue
            elif self.mario.rect.top == sprite.rect.bottom and self.mario.rect.left < sprite.rect.right and self.mario.rect.right > sprite.rect.left or self.mario.rect.top - 1 == sprite.rect.bottom and self.mario.rect.left < sprite.rect.right and self.mario.rect.right > sprite.rect.left:
                if sprite._type == 'quiz' and sprite.stuff._gravity == 0:
                    if sprite.stuff._amount > 0:
                        print(sprite.stuff._amount)
                        self.mario.coins += 1
                    sprite.stuff._gravity += sprite.stuff._limit
                elif sprite._type == 'quiz_mush' and sprite.stuff._appear_count == 0:
                    sprite.stuff._appear_count += sprite.stuff._appear_limit
                return True
        return False
                    
    def groundValidate(self, object):
        for sprite in self.all_sprites:
            if sprite == self.mario or sprite == self.bg:
                continue
            elif object.rect.bottom == sprite.rect.top and object.rect.left < sprite.rect.right and object.rect.right > sprite.rect.left:
                return True
            elif object.rect.bottom - 1 == sprite.rect.top and object.rect.left < sprite.rect.right and object.rect.right > sprite.rect.left:
                return True
            elif object.rect.bottom + 1 == sprite.rect.top and object.rect.left < sprite.rect.right and object.rect.right > sprite.rect.left:
                return True
        return False
    

    def touchValidate(self, object,  dir: str):
        object = object.rect
        for sprite in self.all_sprites:
            if sprite._type == 'common' or sprite._type == 'quiz' or sprite._type == 'quiz_mush':
                if dir == 'right':
                    if object.bottom > sprite.rect.top and object.right == sprite.rect.left and object.top < sprite.rect.bottom:
                        return True
                    elif object.bottom > sprite.rect.top and object.right + 1 == sprite.rect.left and object.top < sprite.rect.bottom:
                        return True
                    elif object.bottom > sprite.rect.top and object.right - 1 == sprite.rect.left and object.top < sprite.rect.bottom:
                        return True
                elif dir == 'left':
                    if object.bottom > sprite.rect.top and object.left == sprite.rect.right and object.top < sprite.rect.bottom:
                        return True
                    elif object.bottom > sprite.rect.top and object.left + 1 == sprite.rect.right and object.top < sprite.rect.bottom:
                        return True
                    elif object.bottom > sprite.rect.top and object.left - 1 == sprite.rect.right and object.top < sprite.rect.bottom:
                        return True
        return False
    
    def enemyDirValidate(self, enemy):
        for sprite in self.all_sprites:
            if sprite._type == 'common' or sprite._type == 'quiz':
                if self.touchValidate(enemy, enemy._direction):
                    if enemy._direction == 'left':
                        return 'right'
                    elif enemy._direction == 'right':
                        return 'left'
                elif not self.groundValidate(enemy):
                    if enemy.rect.top > self.height:
                        self.all_sprites.remove(enemy)
                    enemy._direction = 'falling'
                elif self.groundValidate(enemy) and enemy._direction == 'falling':
                    enemy._direction = enemy._last_dir
                     
        return enemy._direction
                
    def enemiesCheak(self, sprite):
        if self.mario.rect.right >= sprite.rect.left and self.mario.rect.bottom > sprite.rect.top and self.mario.rect.top < sprite.rect.bottom and self.mario.rect.left < sprite.rect.right:
            if self.mario.immortal == 0:
                return 'kill_mario'
        if self.mario.rect.bottom == sprite.rect.top and self.mario.rect.left < sprite.rect.right and self.mario.rect.right > sprite.rect.left and self.mario.rect.top <= sprite.rect.bottom:
            if self.mario.immortal == 0:
                return 'kill_mob'
        return False
    
    def enemiesMove(self):
        
        for sprite in self.all_sprites:
            if sprite._type == 'quiz_mush':
                if sprite.stuff._state == 'active':
                    sprite.stuff.move(self.enemyDirValidate(sprite.stuff))
                    result = self.enemiesCheak(sprite.stuff)
                    if result:
                        sprite.stuff.rect.x = 0
                        sprite.stuff.kill()
                        self.all_sprites.remove(sprite.stuff)
                        self.mario.switchSize(1)
                        
            if sprite._type == 'enemy':
                sprite.move(self.enemyDirValidate(sprite))
                enemy_result = self.enemiesCheak(sprite)
                if enemy_result == 'kill_mob':
                    self.mario.score += 100
                    sprite.die()
                    self.mario._gravity = 5
                elif enemy_result == 'kill_mario':
                    if self.mario._sindex == 1:
                        self.mario.switchSize(0)
                        self.mario.immortal += 80
                    else:
                        self.mario._gravity = 10
                        self.mario.die()
                        
            elif sprite._type == 'die':
                if sprite._last_seconds > 0:
                    sprite._last_seconds -= 1
                else:
                    self.all_sprites.remove(sprite)
            
            
    def coinCheak(self):
        for sprite in self.all_sprites:
            if sprite == self.mario or sprite == self.bg:
                continue
            elif sprite._type == 'quiz':
                if sprite.stuff._amount > 0:
                    if sprite.stuff._gravity > 0:
                        sprite.stuff.getCoin()
                        sprite.stuff._gravity -= 1
                        if sprite.stuff._gravity == 0:
                            sprite.stuff._amount -= 1
                elif sprite.stuff._amount == 0:
                    self.all_sprites.remove(sprite.stuff)
                    
            elif sprite._type == 'quiz_mush':
                if sprite.stuff._appear_count > 0:
                    sprite.stuff.rect.y -= 1
                    sprite.stuff._appear_count -= 1
                    if sprite.stuff._appear_count == 0:
                        sprite.stuff._appear_limit = 0
                        sprite.stuff._state = 'active'
                        
    def count(self):
        self.time_text = self.myfont.render("Time {0}".format(self.time), 1, self.white)
        self.coins_text = self.myfont.render("Coins {0}".format(self.mario.coins), 1, self.white)
        self.live_text = self.myfont.render("Lives {0}".format(self.mario.lives), 1, self.white)
        self.score_text = self.myfont.render("Score {0}".format(self.mario.score), 1, self.white)
        
        self.time_score += 1
        if self.time_score == 20:
            self.time_score = 0
            self.time -= 1
                    
    def cheakingAll(self, jump_state: bool):
        if not self.groundValidate(self.mario) and not jump_state:
            self.mario.falling()
                
        if self.headValidate():
            self.mario._gravity = 0
            
        self.coinCheak()
        self.enemiesMove()
        self.marioDeadValidate()
        self.count()
                
        
    def main(self):
        
        for i in range(self.mario.lives):
            
            while self.running:
                
                self.clock.tick(self.fps)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                
                jump_state = self.mario.jump()

                if event.type == pygame.KEYDOWN:    
                    
                    if event.key == pygame.K_UP:
                        if self.groundValidate(self.mario):
                            self.mario._jump_count = 0
                        if self.mario._jump_count == 0:
                            if self.groundValidate(self.mario):
                                self.mario._gravity += self.mario.jump_height/3
                                self.mario._jump_count += self.mario.jump_height/3 
                        elif self.mario._jump_count > 0 and self.mario._jump_count < self.mario.jump_height:
                            self.mario._gravity += self.mario.jump_height/3
                            self.mario._jump_count += self.mario.jump_height/3
                        
                    if event.key == pygame.K_RIGHT:
                        if self.bg.rect.right > self.width:
                            #print(self.bg.rect.x)
                            self.bgMove('right')
                            self.mario.move('right')
                        
                    if event.key == pygame.K_LEFT:
                        if self.bg.rect.left < 0:
                            #print(self.bg.rect.x)
                            self.bgMove('left')
                            self.mario.move('left')
                        
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT:
                            self.mario.stop('right')
                        if event.key == pygame.K_LEFT:
                            self.mario.stop('left')
                
                self.cheakingAll(jump_state)
                    
                self.screen.fill(self.white)
                self.all_sprites.draw(self.screen)
                
                self.screen.blit(self.live_text, (500, 10))
                self.screen.blit(self.time_text, (350, 10))
                self.screen.blit(self.coins_text, (200, 10))
                self.screen.blit(self.score_text, (50, 10))
                
                pygame.display.flip()
                
            self.restart()
            
                    
game = Screen()

wall_1 = Barrier('walls.jpg', [63, 430], 'common')
wall_2 = Barrier('walls.jpg', [189, 430], 'common')
wall_3 = Barrier('walls.jpg', [315, 430], 'common')
wall_4 = Barrier('walls.jpg', [441, 430], 'common')
wall_5 = Barrier('walls.jpg', [567, 430], 'common')
wall_6 = Barrier('walls.jpg', [733, 430], 'common')
wall_7 = Barrier('walls.jpg', [909, 430], 'common')
wall_8 = Barrier('walls.jpg', [1035, 430], 'common')
wall_9 = Barrier('walls.jpg', [1161, 430], 'common')
wall_10 = Barrier('walls.jpg', [1327, 430], 'common')
wall_11 = Barrier('walls.jpg', [1453, 430], 'common')
wall_12 = Barrier('walls.jpg', [1579, 430], 'common')
wall_13 = Barrier('walls.jpg', [1705, 430], 'common')
wall_14 = Barrier('walls.jpg', [1831, 430], 'common')
wall_15 = Barrier('walls.jpg', [1957, 430], 'common')

rock_10 = Barrier('rock_5.png', [1377-166, 347], 'common')
rock_9 = Barrier('rock_4.png', [1352-166, 360], 'common')
rock_8 = Barrier('rock_3.png', [1327-166, 372], 'common')
rock_7 = Barrier('rock_2.png', [1302-166, 385], 'common')
rock_6 = Barrier('rock_1.png', [1276-166, 397], 'common')
rock_5 = Barrier('rock_5.png', [1276, 347], 'common')
rock_4 = Barrier('rock_4.png', [1302, 360], 'common')
rock_3 = Barrier('rock_3.png', [1327, 372], 'common')
rock_2 = Barrier('rock_2.png', [1352, 385], 'common')
rock_1 = Barrier('rock_1.png', [1377, 397], 'common')

duct_1 = Barrier('duct_1.png', [441, 390], 'common')
duct_2 = Barrier('duct_2.png', [567, 380], 'common')
duct_3 = Barrier('duct_3.png', [710, 370], 'common')
duct_4 =  Barrier('duct_3.png', [953, 370], 'common')

air_br_1 = Barrier('air_br_1.png', [757, 250], 'common')
air_br_2 = Barrier('air_br_2.png', [685, 250], 'common')
air_br_3 = Barrier('air_br_2.png', [345, 310], 'common')

coin_1 = Coin([559, 230], 2)
coin_2 = Coin([709, 250], 2)
good_mush = EdibleMush([370, 310])
quiz_1 = Barrier('quiz_block.jpg', [559, 230], 'quiz', coin_1)
quiz_2 = Barrier('quiz_block.jpg', [709, 250], 'quiz', coin_2)
quiz_3 = Barrier('quiz_block.jpg', [369, 310], 'quiz_mush', good_mush)

mush_1 = Mush([787, 230])
mush_9 = Mush([400, 402])
mush_3 = Mush([500, 402])



game.all_sprites.add(wall_1)
game.all_sprites.add(wall_2)
game.all_sprites.add(wall_3)
game.all_sprites.add(wall_4)
game.all_sprites.add(wall_5)
game.all_sprites.add(wall_6)
game.all_sprites.add(wall_7)
game.all_sprites.add(wall_8)
game.all_sprites.add(wall_9)
game.all_sprites.add(wall_10)
game.all_sprites.add(wall_11)
game.all_sprites.add(wall_12)
game.all_sprites.add(wall_13)
game.all_sprites.add(wall_14)
game.all_sprites.add(wall_15)

game.all_sprites.add(rock_10)
game.all_sprites.add(rock_9)
game.all_sprites.add(rock_8)
game.all_sprites.add(rock_7)
game.all_sprites.add(rock_6)
game.all_sprites.add(rock_5)
game.all_sprites.add(rock_4)
game.all_sprites.add(rock_3)
game.all_sprites.add(rock_2)
game.all_sprites.add(rock_1)

game.all_sprites.add(duct_1)
game.all_sprites.add(duct_2)
game.all_sprites.add(duct_3)
game.all_sprites.add(duct_4)
game.all_sprites.add(air_br_1)
game.all_sprites.add(air_br_2)
game.all_sprites.add(air_br_3)
game.all_sprites.add(quiz_1.stuff)
game.all_sprites.add(quiz_2.stuff)
game.all_sprites.add(quiz_3.stuff)
game.all_sprites.add(quiz_1)
game.all_sprites.add(quiz_2)
game.all_sprites.add(quiz_3)
game.all_sprites.add(mush_1)
game.all_sprites.add(mush_9)
game.all_sprites.add(mush_3)

game.start_pos = game.all_sprites

game.main()