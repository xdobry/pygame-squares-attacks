import pygame
import player
import bullet
import enemy
import obstacle
import explosion
import itemManager
import item
import bombExplosion
import text
from enemySpawner import EnemySpawner
from background import fillBackground, createBackgroundImage
from utils import load_image, isDevMode

for cls in [bullet.Bullet,enemy.Enemy,explosion.Explosion,player.Player,item.Item]:
    cls.loadImages()
text.loadImages()


STATE_PLAY = 0
STATE_KILLED = 1
STATE_LEVELINTRO = 2

class PlayScreen:
    backgroundColor = pygame.Color((0,10,100))
    cockpitHeight = 32
    itemLeftPos = 400

    def __init__(self,game,screenRect):
        self.devMode = isDevMode()
        self.playRect = pygame.rect.Rect(0,0,screenRect.width,screenRect.height-self.cockpitHeight)
        player.Player.screenRect = self.playRect
        bullet.Bullet.screenRect = self.playRect
        enemy.Enemy.screenRect = self.playRect
        self.screen = game.screen
        self.game = game
        self.screenRect = screenRect
        self.mainGroup = pygame.sprite.Group()
        self.spieler = player.Player()
        self.mainGroup.add(self.spieler)
        self.bulletsGroup = pygame.sprite.Group()
        self.itemManager = itemManager.ItemManager(pygame.rect.Rect(self.itemLeftPos,screenRect.height-self.cockpitHeight,screenRect.width-self.itemLeftPos,self.cockpitHeight),game)
        # gegner setzen
        self.gegnerGroup = pygame.sprite.Group()
        self.obstacles = []
        self.obstaclesGroup = pygame.sprite.Group()
        self.font = pygame.font.SysFont("mono",18)
        self.enemySpawner = EnemySpawner(self)
        self.state = STATE_PLAY
        self.counter = 0
        self.stateChangeCounter = 0
        self.tiles = {}
        for tile in ["boden","boden2"]:
            self.tiles[tile] = load_image(tile+".png")
        for tile in ["crystal_wall06","hive1","marble_wall1","pebble_red0",
                     "sandstone_wall0","slime0","stone_brick1","wall_yellow_rock0"]:
            self.tiles[tile] = pygame.transform.scale(load_image(tile+".png"),(64,64))
        self.consoleBackground = load_image("console background.png")
        self.consoleBackgroundSurface = createBackgroundImage("console background.png",pygame.rect.Rect(0,0,screenRect.width,self.cockpitHeight))
        self.backgroundSurface = pygame.Surface(screenRect.size,pygame.SRCALPHA)
        self.setBackground("boden")
        self.scoreTextCache = ""
        self.effectElements = []
        self.msgTime = 0
    def processEvent(self,event):
        if event.type == pygame.KEYDOWN: 
            if self.devMode:
                if event.key == pygame.K_n:
                    self.enemySpawner.nextLevel()
                elif event.key == pygame.K_p:
                    self.lebenanzahl += 1
    def setBackground(self,name):
        fillBackground(self.backgroundSurface,self.tiles[name],self.screenRect)
    def showMessage(self,msg):
        self.msg = text.render(msg)
        self.msgTime = 100
    def setObstacles(self,obstaclesPositionList):
        self.obstacles = []
        for obstacleInst in self.obstaclesGroup:
            obstacleInst.kill()
        for obstaclePos in obstaclesPositionList:
            self.obstacles.append(obstacle.Obstacle(obstaclePos[0],obstaclePos[1],(self.obstaclesGroup,self.mainGroup)))
    def update(self,counter):
        self.counter = counter
        notActiveEffects = []
        for effect in self.effectElements:
            if effect.isActive():
                effect.update(counter)
            else:
                notActiveEffects.append(effect)
        for effect in notActiveEffects:
            self.effectElements.remove(effect)
        if self.state != STATE_PLAY:
            if self.counter >= self.stateChangeCounter:
                if self.state == STATE_KILLED:
                    if self.playerDeath():
                        return
                self.state = STATE_PLAY
        else:
            # spawn enemy
            self.enemySpawner.spawn(counter)
            mouseButtonState = pygame.mouse.get_pressed()
            # wenn die linke maustaste gedrückt ist
            self.spieler.handleMouse(mouseButtonState,counter,self)
            # update your objects, move, collision detection, etc
            #tastatur auslesen und player bewegen
            keystate = pygame.key.get_pressed()
            self.spieler.handleKey(keystate,self.obstaclesGroup)
        self.itemManager.update(self.game,counter)
        self.mainGroup.update(self.game)
        self.itemManager.checkPlayerCollision(self.spieler,self.counter)
        for i in range(self.game.physicFrames):
            self.physicUpdateCheckCollisions()

    def physicUpdateCheckCollisions(self):
        self.gegnerGroup.update(self.game)
        self.obstaclesGroup.update(self.game)
        self.bulletsGroup.update(self.game,self.counter)
        # prüfe ob enemy durchgegangen ist
        for enemyInst in self.gegnerGroup:
            if enemyInst.rect.left==self.screenRect.width-64:
                self.game.playSound("alarm")
            if enemyInst.rect.left>self.screenRect.width:
                self.playerKilled("enemy break out")
        # finde ob bullets und gegner kollidieren oder mit dem player
        for bulletInst in self.bulletsGroup:
            if bulletInst.bornCounter+3<self.counter and bulletInst.hitCircle(pygame.math.Vector2(self.spieler.rect.center),self.spieler.rsize):
                self.playerKilled("hit by bullet")
                bulletInst.kill()
                break
            for enemyInst in self.gegnerGroup:
                bulletInst.tryEnemyOrObstacle(enemyInst,self.game)
            for obstacleInst in self.obstaclesGroup:
                bulletInst.tryEnemyOrObstacle(obstacleInst,self.game)
        # prüfe ob enemry ein Hindernis berührt
        for enemyInst in self.gegnerGroup:
            for obstacleInst in self.obstaclesGroup:
                if obstacleInst.rect.colliderect(enemyInst.rect):
                    enemyInst.kill()
                    obstacleInst.kill()
                    self.game.playSound("hit")
            if self.spieler.isHittingEnemy(enemyInst):
                self.playerKilled("collide with enemy")
                break
    def makeExplosion(self,sprite):
        self.mainGroup.add(explosion.Explosion(sprite))
    def playerKilled(self,cause="hit by bullet"):
        if self.state != STATE_KILLED:
            self.killedCause = cause
            self.makeExplosion(self.spieler)
            self.spieler.kill()
            self.game.playSound("playerKilled")
            self.state = STATE_KILLED
            self.stateChangeCounter = self.counter + 40
    def playerDeath(self):
        self.bulletsGroup.empty()
        minLevel = 1000
        minAttack = 1000
        for enemyInst in self.gegnerGroup:
            if enemyInst.attack[0]<minLevel or (enemyInst.attack[0]==minLevel and enemyInst.attack[0]<minAttack):
                minLevel = enemyInst.attack[0]
                minAttack = enemyInst.attack[1]
            enemyInst.kill()
        if self.lebenanzahl == 1:
            self.game.gameOver(self.killedCause)
            self.game.playSound("gameOver")
            return True
        else:
            self.lebenanzahl = self.lebenanzahl - 1
        self.enemySpawner.resetAttack(minLevel,minAttack)
        self.newPlayer()
        return False
    def draw(self,screen,counter):
        screen.blit(self.backgroundSurface,(0,0))
        screen.blit(self.consoleBackgroundSurface,(0,self.screenRect.height-self.cockpitHeight))
        self.itemManager.draw(screen)
        self.mainGroup.draw(screen)
        self.gegnerGroup.draw(screen)
        self.obstaclesGroup.draw(screen)
        self.bulletsGroup.draw(screen)
        self.spieler.drawEyes(screen)
        for enemyInst in self.gegnerGroup:
            enemyInst.drawHands(screen)
        for effect in self.effectElements:
            effect.draw(screen)
        scoreTextNow = f"{self.game.score:05d} LEVEL: {self.enemySpawner.level+1} LIVES: {self.lebenanzahl}"
        if self.scoreTextCache != scoreTextNow:
            self.scoreText = text.render(scoreTextNow)
            self.scoreTextCache = scoreTextNow
        screen.blit(self.scoreText,(8,self.screenRect.height-self.cockpitHeight+10))
        if self.msgTime>0:
            self.msgTime-=1
            screen.blit(self.msg,(self.playRect.centerx-self.msg.get_width()/2,self.playRect.centery-64))
    def newPlayer(self):
        self.spieler.reset()
        self.mainGroup.add(self.spieler)
        for obstacleInst in self.obstacles:
            if not obstacleInst.alive():
                self.obstaclesGroup.add(obstacleInst)
    def newGame(self):
        self.lebenanzahl = 3
        self.newPlayer()
        self.enemySpawner.reset()
        self.itemManager.resetItems()
        self.game.playSound("startGame")
    def levelReset(self):
        self.spieler.reset()
        self.bulletsGroup.empty()
    def bombExplosion(self,pos,range):
        self.game.playSound("bombExplosion")
        self.effectElements.append(bombExplosion.BombExplosion(pos,range))
        posVector = pygame.math.Vector2(pos)
        if (posVector.distance_to(self.spieler.rect.center)<range):
            self.playerKilled("hurt by bomb explosion")
        for gegner in self.gegnerGroup:
            if (posVector.distance_to(gegner.rect.center)<range):
                self.game.makeExplosion(gegner)
                gegner.kill()




        