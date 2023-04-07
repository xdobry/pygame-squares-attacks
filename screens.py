import pygame
import text
import random
import math

backgroundColor = pygame.Color((0,10,100))

message = "WELCOME! YOU WILL NEED TO PROTECT YOUR HOME FROM SQUARE INVASORS ** PROGRAMMING AND GRAPHICS BY TRZ-TEAM ** GAME ASSETS FROM KENNY.NL AND OPENGAMEART.ORG SEE FILE ATTRIBUTION.TXT FOR MORE INFORMATION ** ENJOY THE GAME **"

def doubleSurface(tSurface):
    return pygame.transform.scale(tSurface,(tSurface.get_width()*2,tSurface.get_height()*2))

# Demo Elemente
class MemoryPoint:
    def __init__(self,pos,v,memSize):
        self.pos = pygame.math.Vector2(pos)
        self.moveV = pygame.math.Vector2(v)
        self.memory = []
        self.counter = 0
        self.memSize = memSize
    def update(self):
        self.pos = self.pos + self.moveV
        if self.pos.x<=0 and self.moveV.x<0:
            self.moveV.x = -self.moveV.x
        elif self.pos.x>=MemoryPoint.screenRect.width and self.moveV.x>0:
            self.moveV.x = -self.moveV.x
        if self.pos.y<=0 and self.moveV.y<0:
            self.moveV.y = -self.moveV.y
        elif self.pos.y>=MemoryPoint.screenRect.height and self.moveV.y>0:
            self.moveV.y = -self.moveV.y
        self.counter += 1
        if self.counter%2==0:
            self.memory.append(self.pos.copy())
            if len(self.memory)>self.memSize:
                self.memory.pop(0)

class Line:
    def __init__(self,startColor,endColor,steps,velRange):
        self.colors = genColors(startColor,endColor,steps)
        self.p1 = MemoryPoint(genRandomXY(Line.screenRect.size),genRandomXY((velRange[1]-velRange[0],velRange[1]-velRange[0]),velRange[0],True),steps)
        self.p2 = MemoryPoint(genRandomXY(Line.screenRect.size),genRandomXY((velRange[1]-velRange[0],velRange[1]-velRange[0]),velRange[0],True),steps)
    def update(self):
        self.p1.update()
        self.p2.update()
    def draw(self,screen):
        for color, p1, p2 in zip(self.colors,self.p1.memory,self.p2.memory):
            pygame.draw.line(screen,color,(int(p1.x),int(p1.y)),(int(p2.x),int(p2.y)))

def genRandomXY(range,add=0, minus=False):
    x = random.randint(0,range[0])+add
    y = random.randint(0,range[1])+add
    if minus:
        x = -x if random.random()>0.5 else x
        y = -y if random.random()>0.5 else y
    return (x,y)

def genColors(startColor,endColor,steps):
    colors = []
    startV = pygame.math.Vector3(startColor.r,startColor.g,startColor.b)
    endV = pygame.math.Vector3(endColor.r,endColor.g,endColor.b)
    for s in range(0,steps):
        colorV = startV.lerp(endV,s/steps)
        colors.append(pygame.Color(int(colorV.x),int(colorV.y),int(colorV.z)))
    return colors

class IntroScreen:
    def __init__(self,game,screenRect):
        self.game = game
        self.gameName = doubleSurface(text.render("SQUARES ATTACKS"))
        self.textSurface = text.render("PRESS SPACE TO START")
        self.helpSurface = text.render("CONTROL BY WASD AND MOUSE")
        self.helpSurface2 = text.render("RICOCHET SHOTS HAVE MORE ENERGY!")
        self.screenRect = screenRect
        Line.screenRect = screenRect
        MemoryPoint.screenRect = screenRect
        linesCount = 8
        self.lines = [
            Line(backgroundColor,pygame.Color(0, 50, 250),linesCount,(2,6)),
            Line(backgroundColor,pygame.Color(0, 255, 20),linesCount,(2,6)),
            Line(backgroundColor,pygame.Color(255, 0, 20),linesCount,(2,6))
        ]
        self.startCounter = -1
        self.hasMusic = False
    def update(self,counter):
        if self.startCounter<0:
            self.startCounter = counter
        self.textSurface.set_alpha(int(abs(math.sin(counter/50))*255))            
        if not self.hasMusic and self.startCounter+250<counter:
            self.game.sounds["introMusic"].play()
            self.hasMusic = True
        for line in self.lines:
            line.update()
    def draw(self,screen,counter):
        screen.fill(backgroundColor)
        for line in self.lines:
            line.draw(screen)
        screen.blit(self.gameName,
            (self.screenRect.centerx-self.gameName.get_width()/2,self.screenRect.centery-self.gameName.get_height()/2-30))
        screen.blit(self.helpSurface,
            (self.screenRect.centerx-self.helpSurface.get_width()/2,self.screenRect.centery-self.helpSurface.get_height()/2+30))
        screen.blit(self.helpSurface2,
            (self.screenRect.centerx-self.helpSurface2.get_width()/2,self.screenRect.centery-self.helpSurface2.get_height()/2+30+(self.helpSurface.get_height()+5)*1))
        screen.blit(self.textSurface,
            (self.screenRect.centerx-self.textSurface.get_width()/2,self.screenRect.centery-self.textSurface.get_height()/2+50+(self.helpSurface.get_height()+5)*2))
        posX = counter % (self.screenRect.width+len(message)*16)
        for idx,c in enumerate(list(message)):
            xpos = self.screenRect.width-posX+idx*16
            if xpos>-16 and xpos<self.screenRect.width+16:
                text.blitChar(screen,c,(xpos,int(self.screenRect.height-100+math.sin((posX+idx*3)/20)*20)))
    def processEvent(self,event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.sounds["introMusic"].fadeout(2000)
            self.startCounter = -1
            self.hasMusic = False
            self.game.startGame()

class Star:
    move = pygame.math.Vector3(0,0,1)
    colors = []
    for c in range(0,256):
        colors.append(pygame.Color(c,c,c))
    def __init__(self):
        self.pos = pygame.math.Vector3(random.randint(-800,800),random.randint(-800,800),random.randint(50,800))
    def draw(self,surface):
        global colors
        if self.pos.z>100:
            # https://ogldev.org/www/tutorial12/tutorial12.html
            x2 = int(self.pos.x/self.pos.z*150+surface.get_width()/2)
            y2 = int(self.pos.y/self.pos.z*150+surface.get_height()/2)
            if x2>0 and x2<800 and y2>0 and y2<800:
                r = 255-int(self.pos.z/800*255)
                surface.set_at((x2,y2),self.colors[r])
    def update(self):
        self.pos.z -=2
        if self.pos.z<0: 
            self.pos.z = 800
            self.pos.y = random.randint(-800,800)
            self.pos.x = random.randint(-800,800)

class GameOverScreen:
    def __init__(self,game,screenRect):
        self.game = game
        self.textSurface = doubleSurface(text.render("GAME OVER"))
        self.screenRect = screenRect
        self.startCounter = 0
        self.counter = 0
        self.stars = []
        for i in range(0,600):
            self.stars.append(Star())
    def setCauseScore(self,cause,score):
        self.causeSurface = text.render(cause.upper())
        self.scoreSurface = text.render(score.upper())
    def update(self,counter):
        if self.startCounter == 0:
            self.startCounter = counter
        if counter-self.startCounter>500:
           self.startCounter = 0
           self.game.startIntro()
        for star in self.stars:
            star.update()
    def draw(self,screen,counter):
        screen.fill(backgroundColor)
        h1 = self.textSurface.get_height() + 20
        h2 = self.causeSurface.get_height() + 10
        h3 = self.scoreSurface.get_height() + 10
        ha = h1+h2+h3
        screen.blit(self.textSurface,
            (self.screenRect.centerx-self.textSurface.get_width()/2,self.screenRect.centery-ha/2))
        screen.blit(self.causeSurface,
            (self.screenRect.centerx-self.causeSurface.get_width()/2,self.screenRect.centery-ha/2+h1))
        screen.blit(self.scoreSurface,
            (self.screenRect.centerx-self.scoreSurface.get_width()/2,self.screenRect.centery-ha/2+h1+h2))
        for star in self.stars:
            star.draw(screen)
    def processEvent(self,event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.startCounter = 0
            self.game.startGame()