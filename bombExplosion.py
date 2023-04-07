
import pygame
from utils import loadImagesFromMap

class BombExplosion(pygame.sprite.Sprite):
    maxLive = 10
    explosionColor = pygame.Color(255,100,100)
    def __init__(self,position,radius):
        self.live = self.maxLive
        self.postion = position
        self.radius = radius
    def draw(self,screen):
        r = self.radius/2*(1+(self.maxLive-self.live)/self.maxLive)
        pygame.draw.circle(screen,self.explosionColor,self.postion,r,3)
    def update(self,counter):
        if self.live>0:
            self.live -= 1
    def isActive(self):
        return self.live>0
        