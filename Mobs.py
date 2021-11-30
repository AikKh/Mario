import pygame, os

class Mush(pygame.sprite.Sprite):
    
    game_folder = os.path.dirname(__file__)
    enemies_imgs = os.path.join(game_folder, 'enemies_imgs')
    

    def __init__(self, location: list):
        self.mush_1 = pygame.image.load(os.path.join(self.enemies_imgs, 'mush_1.png'))
        self.mush_2 = pygame.image.load(os.path.join(self.enemies_imgs, 'mush_2.png'))
        self.mush_die = pygame.image.load(os.path.join(self.enemies_imgs, 'mush_die.png'))
        self.mush_steps = [self.mush_1, self.mush_2]
        
        self._type = 'enemy'
        self._direction = 'left'
        self._last_dir = None
        self._index = 0
        self._last_seconds = 40
        self._speed = self._index % 2
        pygame.sprite.Sprite.__init__(self)
        self.image = self.mush_1
        self.rect = self.image.get_rect()
        self.rect.center = location
        
    def move(self, dir):
        if dir == 'left':
            self._direction = 'left'
            self._last_dir = 'left'
            self.rect.x -= self._index % 2
            self._index += 1
            self.image = self.mush_steps[(self._index//8) % 2]
        elif dir == 'right':
            self._direction = 'right'
            self._last_dir = 'right'
            self.rect.x += self._index % 2
            self._index += 1
            self.image = self.mush_steps[(self._index//8) % 2]
        elif dir == 'falling':
            self._direction = 'falling'
            self.rect.y += 2
            self._index += 1
            self.image = self.mush_steps[(self._index//8) % 2]
            
    def switchDir(self):
        if self._direction == 'right':
            self._direction = 'left'
        elif self._direction == 'left':
            self._direction == 'right'

    def die(self):
        self.image = self.mush_die
        self.rect.y += 8
        self._type = 'die'
        
class EdibleMush(Mush):
    
    def __init__(self, location: list):
        Mush.__init__(self, location)
        self.mush_1 = pygame.image.load(os.path.join(self.enemies_imgs, 'good_mush.png'))
        self.image = self.mush_1
        self.mush_steps = [self.mush_1, self.mush_1]
        self._type = 'good_mush'
        self._state = 'passive'
        self._appear_count = 0
        self._appear_limit = 22
        self._direction = 'right'
        self._last_dir = self._direction
        self.rect = self.image.get_rect()
        self.rect.center = location
        