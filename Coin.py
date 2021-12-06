import pygame, os

class Coin(pygame.sprite.Sprite):
    
    game_folder = os.path.dirname(__file__)
    quiz_folder = os.path.join(game_folder, 'quiz_stuff')
    
    coin_1 = pygame.image.load(os.path.join(quiz_folder, 'coin_1.png'))
    coin_2 = pygame.image.load(os.path.join(quiz_folder, 'coin_2.png'))
    coin_3 = pygame.image.load(os.path.join(quiz_folder, 'coin_3.png'))
    coin_4 = pygame.image.load(os.path.join(quiz_folder, 'coin_4.png'))
    
    coins = [coin_1, coin_2, coin_3, coin_4]
    
    def __init__(self, location: list, amount):
        self._location = (location[0] + 1, location[1])
        self._amount = amount
        self._type = 'coin'
        self._limit = 40
        self._index = 0
        self._gravity = 0
        self._go_home = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = self.coin_1
        self.rect = self.image.get_rect()
        self.rect.center = location
        
        
    def getCoin(self):
        if self._gravity == 0:
            self._amount -= 1
        if self._gravity > self._limit/2:
            self.rect.y -= 5
            self.image = self.coins[(self._index//2) % len(self.coins)]
            self._index += 1
        else:
            self.rect.y += 5
            self.image = self.coins[(self._index//2) % len(self.coins)]
            self._index += 1
            