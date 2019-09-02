import pygame
from constants import pygameWindowWidth, pygameWindowDepth

class PYGAME_WINDOW:
    def __init__(self):

        self.pygWindowWidth = pygameWindowWidth
        self.pygWindowDepth = pygameWindowDepth
        pygame.init()
        self.screen = pygame.display.set_mode((self.pygWindowWidth,self.pygWindowDepth))

    def Prepare(self):
        white = (255,255,255)
        self.screen.fill(white)

    def Reveal(self):
        pygame.display.update()

    def Draw_Black_Circle(self,x,y):
        pygame.draw.circle(self.screen, (0,0,0), [x,y], 25)

        
