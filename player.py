import pygame
import bullet
from utils import collideRectWithCircel, load_image

shootDelay = 50

class Player(pygame.sprite.Sprite):
    rsize = 32

    eyeColor = pygame.Color((0,0,0))
    eyePupileColor = pygame.Color((255,255,255))

    @classmethod
    def loadImages(cls):
        #spriteMap = load_image("player_shoot.png")
        cls.images = [load_image("player3.png")]
       # columns = 3
        #for i in range(8):
            #cls.images.append(spriteMap.subsurface(pygame.Rect(i%columns*64,int(i/columns)*64,64,64)))
            
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(0,0,self.rsize*2,self.rsize*2)
        self.rect.center = self.screenRect.center
        self.image = self.images[0]
        self.reset()
        self.isMouseDown = False
        self.fireCounter = -1
  
    def reset(self):    
        self.rect.center = self.screenRect.center

    def move(self,x,y,obstaclesGroup):
        self.rect.move_ip(x,y)
        for obstacleInst in obstaclesGroup:
            if collideRectWithCircel(obstacleInst.rect,self.rect):
                self.rect.move_ip(-x,-y)
                return
        self.rect = self.rect.clamp(self.screenRect)

    # gibt True wenn mit gegner collidiert
    def isHittingEnemy(self,gegner):
        return collideRectWithCircel(gegner.rect,self.rect) 
    
    def drawEyes(self,screenSurface):
        if self.alive():
            mousePos = pygame.mouse.get_pos()
            bereichX = 10
            bereichY = 15
            screenWidth = screenSurface.get_width()
            screenHeight = screenSurface.get_height()
            #pygame.draw.circle(screenSurface,self.eyePupileColor,(self.rect.left+10,self.rect.top+30),15)
            #pygame.draw.circle(screenSurface,self.eyePupileColor,(self.rect.left+20,self.rect.top+30),15)
            dx = 5+int((mousePos[0]-self.rect.left)*bereichX/screenWidth)
            dy = 35+int((mousePos[1]-self.rect.left)*bereichY/screenHeight)
            pygame.draw.rect(screenSurface,self.eyeColor,pygame.rect.Rect(self.rect.left+dx,self.rect.top+dy,4,6))
            pygame.draw.rect(screenSurface,self.eyeColor,pygame.rect.Rect(self.rect.left+10+dx,self.rect.top+dy,4,6))
    
    def handleMouse(self,mouseButtonState,counter,playScreen):
        if mouseButtonState[0]:
            if not self.isMouseDown:
                self.isMouseDown = True
                mousePos = pygame.mouse.get_pos()
                # print(f"mouseclick {mousePos}")
                # prüfe ob nicht genau in der mitte des spielers gedrückt wurde
                if self.rect.centerx != mousePos[0] or self.rect.centery != mousePos[1]:        
                    if mousePos[1]>playScreen.playRect.height:
                        playScreen.itemManager.handleMousePress(mousePos,counter)
                    elif counter - self.fireCounter >= self.getShotDelay(playScreen,counter) or self.fireCounter < 0:
                        #erzeuge eine bullet mit der startposition der mitte des spielers
                        if playScreen.itemManager.isItemKindActivated("bomb",counter,True):
                            sound = "bomb"
                            bulletKind = "bomb"
                        elif playScreen.itemManager.isItemKindActivated("fireball",counter,False):
                            sound = "fire"
                            bulletKind = "fireball"
                        else:
                            sound = "shoot"
                            bulletKind = "normal"
                        bullet.Bullet(self.rect.center,mousePos,self.rsize,(playScreen.bulletsGroup),counter,bulletKind)
                        playScreen.game.playSound(sound)
                        self.fireCounter = counter 
            else:
                self.isMouseDown = False
    
    def getShotDelay(self,playScreen,counter):
        if playScreen.itemManager.isDoubleSpeedActivated(counter):
            return shootDelay/2
        else:
            return shootDelay
    
    def handleKey(self,keystate,obstaclesGroup):
        self.move((keystate[pygame.K_d]-keystate[pygame.K_a])*3,(keystate[pygame.K_s]-keystate[pygame.K_w])*3,obstaclesGroup)