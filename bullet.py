import pygame
import math
from utils import loadImagesFromMap

class Bullet(pygame.sprite.Sprite):
    color_bullet = pygame.Color(255,0,0)
    speed = 4
    maxHit = 4

    @classmethod
    def loadImages(cls):
        cls.images = loadImagesFromMap("bullet.png",5,2,16)
        cls.rsize = cls.images[0].get_width()/2

    def __init__(self,bulletStart,targetPos,distance,groups,bornCounter,kind="normal"):
        # kind [normal, bomb, fireball]
        pygame.sprite.Sprite.__init__(self,groups)
        # Erzeuge ein Sprite Bild (image) und mal da ein Kreis      
        self.rect = pygame.rect.Rect(0,0,self.rsize*2,self.rsize*2)
        self.rect.center = bulletStart
        # Setze einen Bewegungsvektro
        self.move = pygame.math.Vector2(targetPos[0]-bulletStart[0],targetPos[1]-bulletStart[1])
        # Setzte die Länge des Bewegungsvektro "Geschwindigkeit" auf speed
        # Wenn Bombe dann verlangsame auf die Häflte
        speedVector = 1 if kind=="normal" else 0.5
        self.move.scale_to_length(self.speed*speedVector)
        # Setze die Position als Vektor
        # Es zeigt auf die Mitte des Bullets
        self.position = pygame.math.Vector2(bulletStart)
        distV = self.move.copy()
        distV.scale_to_length(distance)
        self.position = self.position + distV
        # Anzahl der Abprahler
        self.hits = 1
        self.bornCounter = bornCounter
        self.kind = kind
        if kind=="normal":
            self.image = self.images[0]
        elif kind=="bomb":
            self.image = self.images[3]
        else:
            self.image = self.images[1]
    def update(self,game,counter):
        # aktualisere die position idem man zu dem positions vektror den Bewegungsvektor (move) addiert
        #self.move.y = self.move.y + 0.1
        self.position = self.move + self.position
        self.handleBorderHit(game)
        self.rect.center = self.position
        if self.kind=="bomb":
            self.image = self.images[3+int(counter/4)%2]
        elif self.kind=="fireball":
            self.image = self.images[1+int(counter/4)%2]

        if self.hits>self.maxHit:
            self.kill()
    def hitBorder(self,game):
        self.kill()
        #self.hits += 1
        #game.playSound("bounce")
    def handleBorderHit(self,game):
        if (self.position.x<=self.rsize and self.move.x<0):
            self.hitBorder(game)
            tx = -(self.rsize-self.position.x)/self.move.x
            self.position = self.position - self.move * tx
            self.move.x = -self.move.x
            self.position = self.position + self.move * tx
            #print(f"rc 0 tx {tx} {self.position}")
        elif (self.position.x+self.rsize)>=self.screenRect.width and self.move.x>0:
            self.hitBorder(game)
            tx = (self.position.x+self.rsize-self.screenRect.width)/self.move.x
            self.position = self.position - self.move * tx
            self.move.x = -self.move.x
            self.position = self.position + self.move * tx
            #print(f"rc 1 tx {tx} {self.position}")
        if self.position.y<=self.rsize and self.move.y<0:
            self.hitBorder(game)
            ty = -(self.rsize-self.position.y)/self.move.y
            self.position = self.position - self.move * ty
            self.move.y = -self.move.y
            self.position = self.position + self.move * ty
            #print(f"rc 2 ty {ty} {self.position}")
        elif self.position.y+self.rsize>=self.screenRect.height and self.move.y>0:
            self.hitBorder(game)
            ty = (self.position.y+self.rsize-self.screenRect.height)/self.move.y
            self.position = self.position - self.move * ty
            self.move.y = -self.move.y
            self.position = self.position + self.move * ty
            #print(f"rc 3 ty {ty} {self.position}")
        self.rect.center = self.position

    def hitCircle(self,pos,rsize):
        return self.position.distance_squared_to(pos)<(rsize+self.rsize)**2

    def hitEnemyOrObstacleIsRebound(self,game,obstacleOrEnemy,direction):
        hitResult = obstacleOrEnemy.hitIsAlive(self.hits if self.kind=="normal" else 1000,direction)
        if hitResult == 0:
            self.hits += 1
            game.playSound("bounce")
            return True
        if hitResult == 1:
            self.hits += 1
            game.playSound("shield")
            return True
        else:
            game.makeExplosion(obstacleOrEnemy)
            game.addScore(50)
            if self.kind=="bomb":
                game.bombExplosion(self.rect.center,300)
                self.kill()
            elif self.kind=="fireball":
                game.playSound("death")
            else:
                game.playSound("hit")
                self.kill()
            return False

    def tryEnemyOrObstacle(self,obstacle,game):
        if self.rect.colliderect(obstacle.rect):
            # check side collision
            if (obstacle.rect.bottom>self.rect.centery and obstacle.rect.top<self.rect.centery) or (obstacle.rect.left<self.rect.centerx and obstacle.rect.right>self.rect.centerx):
                if self.rect.centerx<obstacle.rect.centerx:
                    if self.rect.centery<obstacle.rect.centery:
                        if self.rect.right-obstacle.rect.left<self.rect.bottom-obstacle.rect.top:
                            dir = 3
                        else:
                            dir = 0
                    else:
                        if self.rect.right-obstacle.rect.left<obstacle.rect.bottom-self.rect.top:
                            dir = 3
                        else:
                            dir = 2
                else:
                    if self.rect.centery<obstacle.rect.centery:
                        if obstacle.rect.right-self.rect.left<self.rect.bottom-obstacle.rect.top:
                            dir = 1
                        else:
                            dir = 0
                    else:
                        if obstacle.rect.right-self.rect.left<obstacle.rect.bottom-self.rect.top:
                            dir = 1
                        else:
                            dir = 2                
                if not self.hitEnemyOrObstacleIsRebound(game,obstacle,dir):
                    return
                if dir==0:
                    ty = (self.rect.bottom-obstacle.rect.top)/self.move.y
                    #print(f"dir {dir} ty {ty}")
                    self.position = self.position - self.move * ty
                    self.move.y = -self.move.y
                    self.position = self.position + self.move * ty                    
                elif dir==1:
                    tx = (self.rect.left-obstacle.rect.right)/self.move.x
                    #print(f"dir {dir} ty {tx}")
                    self.position = self.position - self.move * tx
                    self.move.x = -self.move.x
                    self.position = self.position + self.move * tx                    
                elif dir==2:
                    ty = (self.rect.top-obstacle.rect.bottom)/self.move.y
                    #print(f"dir {dir} ty {ty}")
                    self.position = self.position - self.move * ty
                    self.move.y = -self.move.y
                    self.position = self.position + self.move * ty                    
                elif dir==3:
                    tx = (self.rect.right-obstacle.rect.left)/self.move.x
                    #print(f"dir {dir} ty {tx}")
                    self.position = self.position - self.move * tx
                    self.move.x = -self.move.x
                    self.position = self.position + self.move * tx
                self.rect.center = self.position                   
            else:
                # corner collision
                if self.rect.centerx>obstacle.rect.centerx:
                    if self.rect.centery>obstacle.rect.centery:
                        corner = obstacle.rect.bottomright
                        dir = 1
                    else:
                        corner = obstacle.rect.topright
                        dir = 1
                else:
                    if self.rect.centery>obstacle.rect.centery:
                        corner = obstacle.rect.bottomleft
                        dir = 3
                    else:
                        corner = obstacle.rect.topleft
                        dir = 3
                corner = pygame.math.Vector2(corner)
                r = corner.distance_to(self.position)
                if r<self.rsize:
                    if not self.hitEnemyOrObstacleIsRebound(game,obstacle,dir):
                        return
                    vx = self.move.x
                    vy = self.move.y
                    vxq = vx * vx
                    vyq = vy * vy
                    r1x = corner.x - self.position.x
                    r1y = corner.y - self.position.y
                    rq = self.rsize * self.rsize
                    # t is the time needed to set back the ball to exactly match the corner
                    # vectors: r1 = r0-tv
                    # v - is bewegung
                    # r0 - gesuchter vector (ball center zu corner)
                    # | r0 | = r^2
                    # mit hilfe von maxima
                    t1 = -(math.sqrt((rq-r1x*r1x)*vyq+2*r1x*r1y*vx*vy+(rq-r1y*r1y)*vxq)-r1y*vy-r1x*vx)/(vyq+vxq)
                    #t2 = (math.sqrt((rq-r1x*r1x)*vyq+2*r1x*r1y*vx*vy+(rq-r1y*r1y)*vxq)+r1y*vy+r1x*vx)/(vyq+vxq)
                    #rqs = (r1x-t1*vx)*(r1x-t1*vx)+(r1y-t1*vy)*(r1y-t1*vy)
                    #s01 = self.position + t1 * self.move
                    #s02 = self.position + t2 * self.move
                    #r01 = corner.distance_to(s01)
                    #r02 = corner.distance_to(s02)
                    #print(f"t1 {t1} t2 {t2} rqs={rqs} rq={rq} r01={r01} r02={r02}")
                    self.position = self.position + self.move * t1
                    #r0 = corner.distance_to(self.pos)
                    #print(f"r0 {r0}")
                    r0 = self.position-corner
                    self.move.reflect_ip(r0)
                    self.position = self.position - self.move * t1
                    self.rect.center = self.position