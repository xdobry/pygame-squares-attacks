import pygame
import os
import sys

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "sprites", file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return surface.convert_alpha()

def loadImagesFromMap(file,count,columns,size=64):
    spriteMap = load_image(file)
    images = []
    for i in range(count):
        images.append(spriteMap.subsurface(pygame.Rect(i%columns*size,int(i/columns)*size,size,size)))
    return images

def loadImagesFromMapScale(file,count,columns,scale):
    spriteMap = load_image(file)
    spriteMap = pygame.transform.scale(spriteMap,(spriteMap.get_width()*scale,spriteMap.get_height()*scale))
    images = []
    for i in range(count):
        images.append(spriteMap.subsurface(pygame.Rect(i%columns*64*scale,int(i/columns)*64*scale,64*scale,64*scale)))
    return images

def collideRectWithCircel(obstacleRect, circleRect):
    if obstacleRect.colliderect(circleRect):
        if (obstacleRect.bottom>circleRect.centery and obstacleRect.top<circleRect.centery) or (obstacleRect.left<circleRect.centerx and obstacleRect.right>circleRect.centerx):
            return True
        else:
            if circleRect.centerx>obstacleRect.centerx:
                if circleRect.centery>obstacleRect.centery:
                    corner = obstacleRect.bottomright
                else:
                    corner = obstacleRect.topright
            else:
                if circleRect.centery>obstacleRect.centery:
                    corner = obstacleRect.bottomleft
                else:
                    corner = obstacleRect.topleft
            corner = pygame.math.Vector2(corner)
            circlePos = pygame.math.Vector2(circleRect.center)
            r = corner.distance_to(circlePos)
            return r<circleRect.width/2            
    else:
        return False


def isDevMode():
    return not getattr(sys, 'frozen', False) or not hasattr(sys, '_MEIPASS')