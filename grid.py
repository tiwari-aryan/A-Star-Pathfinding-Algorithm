import pygame
from time import sleep

from const import *
from block import Block

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Block((i, j)) for j in range(self.rows)] for i in range(self.cols)]
        self.start_node = None
        self.end_node = None

    def draw(self, win):
        for row in self.grid:
            for b in row:
                b.update()
                b.draw(win)

    def get_node(self, coordinates):
        row, col = coordinates
        if row >= 0 and col >= 0 and row < ROWS and col < COLS:
            return self.grid[row][col]
        else:
            return None
    
    def calculate_heuristic(self, current_node):
        start_x, start_y = current_node.row, current_node.col
        end_x, end_y = self.end_node.row, self.end_node.col
        return (start_x - end_x) ** 2 + (start_y - end_y) ** 2
    
    def get_lowest_node(self, unvisited):
        min_node = unvisited[0]
        for node in unvisited:
            if node.f:
                if node.f < min_node.f:
                    min_node = node
                elif node.f == min_node.f and node.h < min_node.h:
                    min_node = node
        return min_node
    
    

    def execute(self, win):

        # g is the distance from the start node
        # h is the heuristic distance from the end node

        if self.check_board():
            
            self.start_node.g = 0
            self.start_node.h = self.calculate_heuristic(self.start_node)
            self.start_node.f = self.start_node.g + self.start_node.h

            unvisited = [self.start_node]
            visited = []
            path = []

            while(unvisited):

                # getting the node with the lowest f value from the list of unvisited nodes
                current_node = self.get_lowest_node(unvisited)
                
                if current_node != self.start_node and current_node != self.end_node:
                    current_node.state = "path"
                    current_node.update()

                unvisited.remove(current_node)
                visited.append(current_node)

                for row in range(-1, 2):
                    for col in range(-1, 2):
                        if row != 0 or col != 0:
                            current_row = current_node.row + row
                            current_col = current_node.col + col
                            new_node = self.get_node((current_row, current_col))
                            if new_node:
                                if(new_node not in visited and new_node.state != "barrier"):
                                    if(new_node in unvisited):
                                        if current_node.g + abs(row) + abs(col) < new_node.g:
                                            new_node.parent = current_node
                                            new_node.g = current_node.g + abs(row) + abs(col)
                                            new_node.update_value()
                                    else:
                                        new_node.parent = current_node
                                        new_node.g = current_node.g + abs(row) + abs(col)
                                        new_node.h = self.calculate_heuristic(new_node)
                                        new_node.update_value()
                                        unvisited.append(new_node)

                                    if new_node != self.start_node and new_node != self.end_node and new_node.state != "path":
                                        new_node.state = "search"
                                        new_node.update()
                        self.draw(win)
                        pygame.display.update()
                        sleep(0.05)

                if self.end_node in visited:
                    path.append(self.end_node)
                    path_node = self.end_node.parent
                    while path_node != self.start_node:
                        path.append(path_node)
                        path_node = path_node.parent
                        path_node.state = "path"
                        path_node.update()
                    path.append(self.start_node)
                    path.reverse()
                    self.show_path(win, path)
                    break
        else:
            return False

    def show_path(self, win, path):
        for i in range(11):
            for node in path:
                node.state = "start" if i % 2 == 0 else "standard"
                node.update()
                self.draw(win)
            pygame.display.update()
            sleep(0.25)
        
    def check_board(self):
        return self.start_node and self.end_node

    def reset(self):
        for row in self.grid:
            for b in row:
                b.reset()
                b.update()

    def get_coordinates(self, pos):
        x, y = pos
        return (x // SQUARE_WIDTH, y // SQUARE_HEIGHT)

    def add_barrier(self, pos):
        row, col = self.get_coordinates(pos)
        b = self.grid[row][col]
        if b.state != "start" and b.state != "end":
            if b.state == "standard":
                b.state = "barrier"
            elif b.state == "barrier":
                b.state = "standard"

    def set_start(self, pos):
        if self.start_node is not None:
            self.start_node.reset()
        
        self.start_node = self.get_node(self.get_coordinates(pos))
        self.start_node.state = "start"

    def set_end(self, pos):
        end_node = self.get_node(self.get_coordinates(pos))
        if self.start_node != end_node:
            if self.end_node is not None:
                self.end_node.reset()
            self.end_node = end_node
            self.end_node.state = "end"

        
