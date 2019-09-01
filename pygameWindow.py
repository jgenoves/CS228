import pygame
from constants import pygameWindowWidth, pygameWindowDepth

class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((pygameWindowWidth,pygameWindowDepth))

    def Prepare(self):
        white = (255,255,255)
        self.screen.fill(white)

    def Reveal(self):
        pygame.display.update()