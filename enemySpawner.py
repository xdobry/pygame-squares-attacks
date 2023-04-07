import enemy
import levels
from utils import isDevMode

class EnemySpawner:
    def __init__(self,playScreen):
        self.playScreen = playScreen
        self.gameFinished = False
        self.needLevelFadeOut = 0
        if playScreen.devMode:
            self.levelsStat()
    def spawn(self,counter):
        if self.startCounter == 0:
            if self.playScreen.gegnerGroup:
                return
            if self.needLevelFadeOut>0:
                self.needLevelFadeOut -= 1
                return
            if self.gameFinished:
                self.playScreen.showMessage(f"CONGRATULATION MISSION ACCOMPLISHED")
                self.playScreen.game.sounds["introMusic"].play()
                self.gameFinished = False
            else:
                self.playScreen.showMessage(f"LEVEL {self.level+1}")
                if self.level != self.playScreen.game.startLevel:
                    self.playScreen.game.playSound("nextLevel")
            if "background" in levels.levels[self.level]:
                self.playScreen.setBackground(levels.levels[self.level]["background"])
            self.startCounter = counter
            self.playScreen.levelReset()
            self.playScreen.setObstacles(levels.levels[self.level]["obstacles"])
        if self.attackScenario==None:
            if self.playScreen.devMode:
                print(f"level {self.level} attack {levels.levels[self.level]['attacks'][self.attack]}")
            self.attackScenario = levels.attacks[levels.levels[self.level]["attacks"][self.attack]]
            self.item = 0
        item = self.attackScenario[self.item]
        if item["t"]<counter-self.startCounter:
            if "l" in item:
                l = item["l"]
                kind = "normal" if not "kind" in item else item["kind"]
                if isinstance(l,list):
                    for litem in l:
                        self.spawnEnemy(litem,[self.level,self.attack],kind)    
                else:
                    self.spawnEnemy(item["l"],[self.level,self.attack],kind)
            if "i" in item:
                self.spawnItem(item["i"])
            self.startCounter = counter
            self.item += 1
            if self.item>=len(self.attackScenario):
                self.attackScenario = None
                self.attack += 1
                if self.attack>=len(levels.levels[self.level]["attacks"]):
                    self.level += 1
                    self.startCounter = 0
                    self.needLevelFadeOut = 200
                    self.attack = 0
                    if self.level>=len(levels.levels):
                        self.gameFinished = True
                        self.level = 0
    def reset(self):
        self.level = self.playScreen.game.startLevel
        self.attack = 0
        self.startCounter = 0
        self.item = 0
        self.attackScenario = None
        self.gameFinished = False
    def resetAttack(self,level,attack):
        if level!=1000:
            self.level = level
            self.attack = attack
        else:
            self.attack = 0
        self.attackScenario = None
        self.item = 0
        self.startCounter = 0
        self.gameFinished = False
    def spawnEnemy(self,lane,attackData,kind):
        for enemyInstance in enemy.Enemy.enemies:
            if not enemyInstance.alive():
                self.playScreen.gegnerGroup.add(enemyInstance)
                enemyInstance.relive(lane,kind)
                enemyInstance.attack = attackData
                return
        newEnemy = enemy.Enemy(lane,kind)
        newEnemy.attack = attackData
        self.playScreen.gegnerGroup.add(newEnemy)
    def nextLevel(self):
        self.level += 1
        self.startCounter = 0
        self.attack = 0
        if self.level>=len(levels.levels):
            self.level = 0
        self.attackScenario = None
    def spawnItem(self,desc):
        self.playScreen.itemManager.spawnItem(desc)
    def levelsStat(self):
        for levelNum, level in enumerate(levels.levels):
            time = 0
            enemies = 0
            for aName in level["attacks"]:
                for attack in levels.attacks[aName]:
                    time += attack["t"]
                    if "l" in attack:
                        enemies += len(attack["l"]) if isinstance(attack["l"],list) else 1
            print(f"level {levelNum+1} time {time} enemies {enemies}")
