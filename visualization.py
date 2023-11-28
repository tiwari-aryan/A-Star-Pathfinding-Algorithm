import pygame
import sys

from const import *
from utils import *
from block import Block
from grid import Grid

pygame.init()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A* Pathfinding Algorithm")

grid = Grid(ROWS, COLS)

run = True

state = {"start": True, "end": False, "barriers": False, "running": False, "result": False}

while run:

    if state["start"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state["start"] = False
                    state["end"] = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                grid.set_start(event.pos)

    elif state["end"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state["end"] = False
                    state["barrier"] = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                grid.set_end(event.pos)

    elif state["barrier"]:
        mouse_state = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state["barrier"] = False
                    state["running"] = True
        pos = pygame.mouse.get_pos()
        left, middle, right = pygame.mouse.get_pressed()
        if left is True:
            grid.add_barrier((pos))
    
    elif state["running"]:
        path = grid.execute(win)
        state["running"] = False
        state["result"] = True

    elif state["result"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    grid.reset()
                    state["result"] = False
                    state["start"] = True


    grid.draw(win)
    pygame.display.update()
    


pygame.quit()
sys.exit()