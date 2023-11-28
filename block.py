import pygame
from utils import *
from const import *

class Block:
    def __init__(self, index):
        self.g = None
        self.h = None
        self.f = None
        self.parent = None
        self.start = False
        self.end = False
        self.barrier = False
        self.path = False
        self.search = False
        self.state = "standard"
        self.colours = {"standard": SQUARE_COLOUR, "start": START_COLOUR, "end": END_COLOUR, "barrier": BARRIER_COLOUR, "path": PATH_COLOUR, "search": SEARCH_COLOUR}
        self.colour = self.colours[self.state]
        self.row, self.col = index
        self.rect = pygame.Rect(self.row * SQUARE_WIDTH, self.col * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT)

    def draw(self, win):
        pygame.draw.rect(win, self.colour, self.rect)
        pygame.draw.rect(win, BORDER_COLOUR, self.rect, 1)

    def update(self):
        self.colour = self.colours[self.state]

    def reset(self):
        self.state = "standard"
    
    def update_value(self):
        self.f = self.g + self.h