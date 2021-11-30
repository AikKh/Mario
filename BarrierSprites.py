import pygame, os


class Barrier(pygame.sprite.Sprite):
    
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'walls_imgs')

    def __init__(self, image_file: str, location: list, type: str, stuff=None):
        self.stuff = stuff
        self._type = type
        self.image_file = image_file
        self._location = location
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(self.img_folder, '{}'.format(self.image_file)))
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = self._location
