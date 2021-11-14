from PyQt5.QtWidgets import QGraphicsRectItem

NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

class Cell:
    def __init__(self, x, y, rect):
        self.x = x
        self.y = y
        self.rect = rect
        self.neighbours = {}
        self.visited = False


    def visited(self):
        return self.visited

    def get_neighbours(self):
        return self.neighbours

    def add_neighbour(self, neighbour, path):
        self.neighbours[path] = neighbour

    def get_rect(self):
        return self.rect