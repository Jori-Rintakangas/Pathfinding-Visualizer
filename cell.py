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
        self.arrived_from = [0,0]

    def is_visited(self):
        return self.visited

    def visit_cell(self):
        self.visited = True

    def get_neighbours(self):
        return self.neighbours

    def add_neighbour(self, neighbour, edge):
        self.neighbours[edge] = neighbour

    def delete_neighbour(self, edge):
        del self.neighbours[edge]

    def get_rect(self):
        return self.rect

    def get_location(self):
        return [self.x, self.y]

    def set_arrived_from(self, x, y):
        self.arrived_from = [x, y]