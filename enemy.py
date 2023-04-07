import pygame
import random
from utils import loadImagesFromMap

class Enemy(pygame.sprite.Sprite):
    # Anzahl der Bahnen
    laneCount = 6
    stopAfterHitMs = 2000
    enemies = []

    @classmethod
    def loadImages(cls):
        cls.maxHits = 3
        cls.images = loadImagesFromMap("enemy.png",6,3,64)
        cls.handImages = loadImagesFromMap("laufen.png",7,3,64)
        cls.enemySize = cls.images[0].get_width()

    def __init__(self,lane,kind="normal"):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.math.Vector2((0,0))
        self.rect = pygame.rect.Rect(0,0,self.enemySize,self.enemySize)
        self.stopUntil = 0
        self.relive(lane,kind)
        self.enemies.append(self)
    def setImageOffset(self,kind):
        self.kind = kind
        if kind=="shield" or kind=="sshield":
            self.imageOffset = 3
        else:
            self.imageOffset = 0
    def update(self,game):
        if self.stopUntil>0:
            if self.stopUntil>pygame.time.get_ticks():
                return
            else:
                self.stopUntil = 0
        # do not move if enemy in same lane is too near
        for otherEnemy in self.enemies:
            if otherEnemy != self and otherEnemy.alive() and otherEnemy.laneNumber==self.laneNumber and otherEnemy.pos.x>self.pos.x and otherEnemy.pos.x-self.pos.x<self.enemySize*2:
                return
        self.pos.x = self.pos.x + self.speed
        self.rect.topleft = self.pos
        self.handFrame += 1
    # ein treffer gibt zurrück ob der gegner noch lebt
    # 0 - nord
    # 1 - east
    # 2 - south
    # 3 - west
    # Result
    # 0 - bounce
    # 1 - shield
    # 2 - killed
    def hitIsAlive(self,hitPower,direction=0):
        if direction==1 and (self.kind=="shield" or self.kind=="sshield") and hitPower!=1000:
            return 1
        else:
            self.hits += hitPower
        if self.hits>=self.maxHits:
            self.kill()
            return 2
        else:
            self.stopUntil = pygame.time.get_ticks()+self.stopAfterHitMs
            self.image = self.images[self.hits+self.imageOffset]
            return 0
    def relive(self,lane,kind):
        self.laneNumber = lane
        self.hits = 0
        self.speed = 0.25 if kind=="slow" else 0.5
        self.handFrame = 0 
        self.setImageOffset(kind)
        self.image = self.images[self.hits+self.imageOffset]
        laneHeight = self.screenRect.height/self.laneCount
        self.pos.y = laneHeight*self.laneNumber+(laneHeight-self.image.get_height())/2
        self.pos.x = -self.image.get_width()
        self.rect.topleft = self.pos
    def drawHands(self,screen):
        div = 24 if self.kind=='slow' or self.kind=="sshield" else 12
        screen.blit(self.handImages[int(self.handFrame/div)%7],(self.rect.left-2,self.rect.top+32))



