import pygame
import item

itemActivationTime = 500

# Speichert den kleine sprite zu item und die Zeit bis wann es leben soll
class ItemActivation:
    def __init__(self,item,time):
        self.item = item
        self.time = time
        self.activated = False

class ItemManager:
    def __init__(self,displayRect,game):
        self.itemGroup = pygame.sprite.Group()
        self.collectedItemGroup = pygame.sprite.Group()
        self.itemActivationList = []
        self.displayRect = displayRect
        self.game = game
    def draw(self,screen):
        self.itemGroup.draw(screen)
        self.collectedItemGroup.draw(screen)
    def update(self,game,counter):
        self.itemGroup.update(game)
        self.collectedItemGroup.update(game)
        itemToRemoveList = []
        for itemActivation in self.itemActivationList:
            if itemActivation.activated and counter>=itemActivation.time:
                itemToRemoveList.append(itemActivation)
        for itemToRemove in itemToRemoveList:
            itemToRemove.item.kill()
            self.itemActivationList.remove(itemToRemove)
        if len(itemToRemoveList):
            for i,itemActivation in enumerate(self.itemActivationList):
                itemActivation.item.rect.left = self.displayRect.left + 32 * i

    # check if collision player with item
    # wenn ja dann wird der Item als aktiviert hinzugefügt
    def checkPlayerCollision(self,player,counter):
        for itemTouch in pygame.sprite.spritecollide(player,self.itemGroup,True):
            self.addItem(itemTouch,counter)
            self.game.playSound("collect")
    # Für Aktivierte Item wird ein kleiner Sprite erschaffen in die collectedItemGroup
    # hinzugefügt und zusätzlich ein Eintrag in die Liste itemActivationList gemacht
    def addItem(self,itemInstance,counter):
        print(f"add item {itemInstance.kind}")
        displayItem = item.Item((self.displayRect.left+len(self.itemActivationList)*32,self.displayRect.top),itemInstance.kind,livetime=0,isSmall=True)
        self.itemActivationList.append(ItemActivation(displayItem,counter+itemActivationTime))
        self.collectedItemGroup.add(displayItem)
    def isDoubleSpeedActivated(self,counter):
        return self.isItemKindActivated("speedShot",counter)
    # Prüft ob ein Item aktiviert ist
    def isItemKindActivated(self,kind,counter,remove=False):
        for itemActivation in self.itemActivationList:
            if itemActivation.item.kind==kind:
                isActivated = itemActivation.activated and counter<itemActivation.time
                if isActivated and remove:
                    itemActivation.item.kill()
                    self.removeActivation(itemActivation)
                if isActivated:
                    return isActivated
        return False
    def removeItem(self,kind):
        itemToRemoveList = []
        for itemActivation in self.itemActivationList:
            if itemActivation.activated and itemActivation.item.kind==kind:
                itemToRemoveList.append(itemActivation)
        for itemToRemove in itemToRemoveList:
            itemToRemove.item.kill()
            self.removeActivation(itemToRemove)
        if len(itemToRemoveList):
            for i,itemActivation in enumerate(self.itemActivationList):
                itemActivation.item.rect.left = self.displayRect.left + 32 * i
    def removeActivation(self,itemActivation):
        self.itemActivationList.remove(itemActivation)
        for idx, itemActivation in enumerate(self.itemActivationList):
            itemActivation.item.rect.x = idx*32 + self.displayRect.left
    # Ein Item wird auf der Oberfläche dargestellt und kann gesammelt werde
    def spawnItem(self,desc):
        newItem = item.Item(desc["pos"],desc["kind"])
        self.itemGroup.add(newItem)
    def resetItems(self):
        self.itemGroup.empty()
        self.collectedItemGroup.empty()
        self.itemActivationList.clear()
    def handleMousePress(self,mousePos,counter):
        for itemActivation in self.itemActivationList:
            if itemActivation.activated:
                return
        for itemActivation in self.itemActivationList:
            if not itemActivation.activated and itemActivation.item.rect.collidepoint(mousePos):
                print(f"activate {itemActivation.item.kind} rect {itemActivation.item.rect} mousePos {mousePos}")
                itemActivation.activated = True
                itemActivation.time = counter + itemActivationTime
                itemActivation.item.activate()
                self.game.playSound("click")
                break


