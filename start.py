import pygame

pygame.init()
screenRect = pygame.Rect((0,0,800,600))
mainScreen = pygame.display.set_mode(screenRect.size)

from playScreen import PlayScreen
from screens import IntroScreen, GameOverScreen
from utils import load_image
import os

class Game:
    backgroundColor = pygame.Color((0,10,100))
    def __init__(self):
        # your need to init your pygame library, enviroment fist
        if pygame.get_sdl_version()[0] == 2:
            pygame.mixer.pre_init(44100, 32, 2, 1024)
        if pygame.mixer and not pygame.mixer.get_init():
            print("Warning, no sound")
            pygame.mixer = None
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR))
        pygame.display.set_icon(load_image("gameIco.png"))
        self.sounds = {}
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        for soundName,soundFile in zip(
            ["shoot","hit","bounce","playerKilled","bomb","bombExplosion","click","collect","shield","gameOver",
             "alarm","nextLevel","startGame","fire","death","introMusic"],
            ["laserSmall_000.ogg","laserLarge_000.ogg","impactMetal_000.ogg","explosionCrunch_000.ogg",
            "lowFrequency_explosion_000.ogg","explosionCrunch_004.ogg","select_001.ogg","confirmation_001.ogg",
            "glass_006.ogg","sfx_sounds_falling12.wav","sfx_alarm_loop2.wav","sfx_movement_portal1.wav","sfx_sound_neutral3.wav",
            "Fire.ogg","sfx_deathscream_human12.wav","MicroRecallOfEarlySynth.ogg"]):
            self.sounds[soundName] = pygame.mixer.Sound(os.path.join(main_dir, "audio", soundFile))

        # screen is the main display your draw on it
        # every game need it
        self.screen = mainScreen
        self.startLevel = 0
        # set screen title, optional
        pygame.display.set_caption('SQUARES ATTACKS')
        self.gameScreen = PlayScreen(self,screenRect)
        self.introScreen = IntroScreen(self,screenRect)
        self.gameOverScreen = GameOverScreen(self,screenRect)
        self.currentScreen = self.introScreen
        self.physicFrames = 2
    def startGame(self):
        self.score = 0
        self.gameScreen.newGame()
        self.currentScreen = self.gameScreen
    def startIntro(self):
        self.currentScreen = self.introScreen
    def gameOver(self,cause):
        #self.playSound("gameOver")
        self.gameOverScreen.setCauseScore(cause,"score " + str(self.score))
        self.currentScreen = self.gameOverScreen
    def playSound(self,soundName):
        #print(f"play {soundName}")
        self.sounds[soundName].play()
    def addScore(self,score):
        self.score = self.score + score
    def makeExplosion(self,sprite):
        self.currentScreen.makeExplosion(sprite)
    def bombExplosion(self,pos,range):
        self.currentScreen.bombExplosion(pos,range)
    def startGameLoop(self):
        running = True
        clock = pygame.time.Clock() 
        counter = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                else:
                    self.currentScreen.processEvent(event)
            self.currentScreen.update(counter)
            # fill screen with background color
            # self.screen.fill(backgroundColor)
            # draw your objects on screen
            self.currentScreen.draw(self.screen,counter)

            # update the real display
            pygame.display.flip()
            # the game loop should run 50 fps
            clock.tick(50)
            counter=counter+1

if __name__ == "__main__":
    game = Game()
    game.startGameLoop()
    pygame.quit()