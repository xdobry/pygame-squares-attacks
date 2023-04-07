import pygame

class Obstacle(pygame.sprite.Sprite):
    color = pygame.Color(230,230,230)
    colorB1 = pygame.Color(250,250,250)
    colorB2 = pygame.Color(170,170,170)
    def __init__(self,pos,size,groups):
        pygame.sprite.Sprite.__init__(self,groups)
        self.image = pygame.Surface(size,pygame.SRCALPHA)
        self.image.fill(self.color)
        pygame.draw.line(self.image,self.colorB1,(0,0),(size[0],0),width=2)
        pygame.draw.line(self.image,self.colorB1,(0,0),(0,size[1]),width=2)
        pygame.draw.line(self.image,self.colorB2,(2,size[1]-2),(size[0],size[1]-2),width=2)
        pygame.draw.line(self.image,self.colorB2,(size[0]-2,2),(size[0]-2,size[1]),width=2)
        self.rect = pygame.rect.Rect(pos,size)
    def hitIsAlive(self,hitPower,direction):
        return 0
