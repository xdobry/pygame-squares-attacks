import pygame
from utils import load_image

size = (16,16)
colorTranparent = pygame.Color((255,255,255,0))

def loadImages():
    global fontImage
    fontImage = load_image("kromagrad_16x16.png")
def render(text):
    textList = list(text)
    surface = pygame.Surface((len(textList)*size[0],size[1]),pygame.SRCALPHA)
    for index, character in enumerate(textList):
        surface.blit(fontImage,(index*size[0],0),pygame.rect.Rect((ord(character)-ord(" "))*size[0],0,size[0],size[1]))
    return surface
def blitChar(surface,char,pos):
    surface.blit(fontImage,pos,pygame.rect.Rect((ord(char)-ord(" "))*size[0],0,size[0],size[1]))

