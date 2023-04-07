import pygame
from utils import loadImagesFromMap

class Explosion(pygame.sprite.Sprite):
    @classmethod
    def loadImages(cls):
        cls.images = loadImagesFromMap("explosion.png",10,3)
    def __init__(self,sprite):
        pygame.sprite.Sprite.__init__(self)
        self.liveTime = 0
        self.rect = pygame.Rect(sprite.rect.left,sprite.rect.top,64,64)
        self.image = self.images[0]
    def update(self,game):
        self.liveTime = self.liveTime+1   
        if self.liveTime>=len(self.images*2):
            self.kill()
        else:
            self.image = self.images[int(self.liveTime/2)]
