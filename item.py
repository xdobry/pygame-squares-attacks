import pygame
import math
from utils import loadImagesFromMap, loadImagesFromMapScale

kinds = ["speedShot","bomb","fireball","mine"]

class Item(pygame.sprite.Sprite):
    @classmethod
    def loadImages(cls):
        cls.images = loadImagesFromMap("items.png",4,2)
        cls.imagesSmall = loadImagesFromMapScale("items.png",4,2,0.5)
    def __init__(self,pos,kind,livetime=300,isSmall=False):
        pygame.sprite.Sprite.__init__(self)
        self.liveTime = livetime
        kindIndex = kinds.index(kind)
        self.kind = kind
        size = 32 if isSmall else 64
        self.rect = pygame.Rect(pos[0],pos[1],size,size)
        self.image = self.images[kindIndex] if not isSmall else self.imagesSmall[kindIndex]
        self.alphaIndex = -1 if isSmall else 0
        if not isSmall:
            self.image.set_alpha(255)
    def update(self,game):
        if self.liveTime>0:
            self.liveTime -= 1
            if self.liveTime<=0:
                self.kill()
        if self.alphaIndex>=0:
            self.alphaIndex += 1
            self.image.set_alpha(200+int(abs(math.sin(self.alphaIndex/25)*55)))
    def activate(self):
        self.alphaIndex = 0
