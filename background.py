from utils import load_image
import pygame

def createBackgroundImage(imageFileName, imageRect):
    tileImage = load_image(imageFileName)
    background = pygame.Surface(imageRect.size,pygame.SRCALPHA)
    for tx in range(int(imageRect.width/tileImage.get_width())+1):
        for ty in range(int(imageRect.height/tileImage.get_height())+1):
            background.blit(tileImage,(tx*tileImage.get_width(),ty*tileImage.get_height()))
    return background

def fillBackground(background, tileImage, imageRect):
    for tx in range(int(imageRect.width/tileImage.get_width())+1):
        for ty in range(int(imageRect.height/tileImage.get_height())+1):
            background.blit(tileImage,(tx*tileImage.get_width(),ty*tileImage.get_height()))


