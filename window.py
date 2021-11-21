from PyQt5 import QtWidgets
import PyQt5
from PyQt5 import QtGui
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtWidgets import QGraphicsLineItem, QMainWindow, QGraphicsRectItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QTime, QEventLoop, QCoreApplication
from collections import deque
import cell as c
import random

X_POS = 50
Y_POS = 300
WIDTH = 1000
HEIGHT = 900
VIEW_W = 800
VIEW_H = 800
LEFT_MARGIN = 140
TOP_MARGIN = 40

STEP = 20
START = 100

CELL_SIZE = 20
ALL_CELLS = 1600

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.edges = {}
        self.cells = {}
        self.speed = 100
        self.white = QBrush(QtGui.QColor(255,255,255))
        self.white_pen = QPen(QtGui.QColor(255,255,255))
        self.white_pen.setWidth(0)
        self.path_found = False
        self.init_ui()

    def init_ui(self):
        self.setGeometry(X_POS, Y_POS, WIDTH, HEIGHT)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self)

        self.scene.setSceneRect(0,0, VIEW_W, VIEW_H)
        self.view.setGeometry(LEFT_MARGIN, TOP_MARGIN, VIEW_W + 20, VIEW_H + 20)
        self.view.setScene(self.scene)

        self.algorithm_label = QtWidgets.QLabel(self)
        self.algorithm_label.setText('Path Finding:')
        self.algorithm_label.setStyleSheet("font-weight: bold; color: black")
        self.algorithm_label.move(20, 30)

        self.algorithms = QtWidgets.QComboBox(self)
        self.algorithms.setGeometry(20, 55, 100, 30)
        algorithms = ['BFS', 'DFS', 'Dijkstra', 'A*']
        self.algorithms.insertItems(0, algorithms)

        self.maze_label = QtWidgets.QLabel(self)
        self.maze_label.setText('Maze Creation:')
        self.maze_label.setStyleSheet("font-weight: bold; color: black")
        self.maze_label.move(20, 85)

        self.maze_algorithms = QtWidgets.QComboBox(self)
        self.maze_algorithms.setGeometry(20, 110, 100, 30)
        maze_algorithms = ['Randomized DFS', 'Randomised Prim']
        self.maze_algorithms.insertItems(0, maze_algorithms)

        self.new_maze_button = QtWidgets.QPushButton(self)
        self.new_maze_button.setGeometry(20, 170, 100, 30)
        self.new_maze_button.setText('Create Maze')

        self.visualize_button = QtWidgets.QPushButton(self)
        self.visualize_button.setGeometry(20, 210, 100, 30)
        self.visualize_button.setText('Find Path')
        self.visualize_button.clicked.connect(self.execute_search)

        self.animation_speed = QtWidgets.QSlider(Qt.Horizontal, self)
        self.animation_speed.setGeometry(20, 280, 100, 20)
        self.animation_speed.setInvertedAppearance(True)
        self.animation_speed.setRange(1, 400)
        self.animation_speed.setValue(40)
        self.animation_speed.valueChanged.connect(self.change_speed)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setText('Animation Speed')
        self.text_label.setStyleSheet("font-weight: bold; color: black")
        self.text_label.move(25, 300)


    def change_speed(self):
        self.speed = self.animation_speed.value()

    def delay(self):
        die_time = QTime.currentTime().addMSecs(self.speed)
        while QTime.currentTime() < die_time:
            QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    def init_grid(self):
        pen = QPen(QtGui.QColor(0,0,0))
        pen.setWidth(2)
        edge1_id = 0
        edge2_id = 0
        for y in range(0 ,VIEW_H, STEP):
            for x in range(0 ,VIEW_W, STEP):
                edge1_id += 1
                edge2_id -= 1
                edge1 = self.scene.addLine(0, 0, STEP, 0, pen)
                edge2 = self.scene.addLine(0, 0, 0, STEP, pen)

                edge1.moveBy(x, y)
                edge2.moveBy(x, y)

                self.edges[edge1_id] = edge1
                self.edges[edge2_id] = edge2

                if y == 0 and x == 0:
                    continue

                if y == 0:
                    cell1 = self.cells[x,y]
                    cell2 = self.cells[x - STEP, y]
                    cell1.add_neighbour(cell2, edge2_id)
                    cell2.add_neighbour(cell1, edge2_id)
                
                elif x == 0:
                    cell1 = self.cells[x,y]
                    cell2 = self.cells[x, y - STEP]
                    cell1.add_neighbour(cell2, edge1_id)
                    cell2.add_neighbour(cell1, edge1_id)
                
                else:
                    cell1 = self.cells[x,y]
                    cell2 = self.cells[x - STEP, y]
                    cell3 = self.cells[x, y - STEP]

                    cell1.add_neighbour(cell2, edge2_id)
                    cell2.add_neighbour(cell1, edge2_id)

                    cell1.add_neighbour(cell3, edge1_id)
                    cell3.add_neighbour(cell1, edge1_id)

                if x == VIEW_W - STEP:
                    edge2_id -= 1
                    edge2 = self.scene.addLine(0, 0, 0, STEP, pen)
                    edge2.moveBy(x + STEP, y)
                    self.edges[edge2_id] = edge2
                if y == VIEW_H - STEP:
                    edge1_id += 1
                    edge1 = self.scene.addLine(0, 0, STEP, 0, pen)
                    edge1.moveBy(x, y + STEP)
                    self.edges[edge1_id] = edge1

    def create_cells(self):
        brush = QBrush(QtGui.QColor(0,0,255))
        pen = QPen(QtGui.QColor(0,0,0))
        pen.setWidth(-1)
        for y in range(0 ,VIEW_H, STEP):
            for x in range(0 ,VIEW_W, STEP):
                rect = self.scene.addRect(0,0, CELL_SIZE, CELL_SIZE, pen, brush)
                rect.moveBy(x,y)
                new_cell = c.Cell(x, y, rect)
                self.cells[x, y] = new_cell

    def create_maze(self, x, y):
        self.delay()
        self.cells[x, y].visit_cell()
        self.cells[x, y].get_rect().setBrush(self.white)
        neighbours = self.cells[x, y].get_neighbours()

        all_visited = False
        while not all_visited:
            neighbours = self.cells[x, y].get_neighbours()
            if not neighbours:
                break
            cell = random.choice(list(neighbours.items()))
            edge = cell[0]
            neighbour = cell[1]
            if not neighbour.is_visited():
                neighbour.visit_cell()
                self.edges[edge].setZValue(-1)
                self.create_maze(neighbour.x, neighbour.y)

            if all(n.is_visited() for n in neighbours.values()):
                all_visited = True

        for edge, neighbour in list(neighbours.items()):
            if self.edges[edge].zValue() == 0:
                self.cells[x, y].delete_neighbour(edge)

    def create_maze_prim(self, x, y):
        self.cells[x, y].visit_cell()
        self.cells[x, y].get_rect().setBrush(self.white)
        frontier_cells = set()
        frontier_cells.add((x, y))
        while len(frontier_cells) > 0:
            self.delay()
            cell = random.choice(list(frontier_cells))
            self.cells[cell[0], cell[1]].get_rect().setBrush(self.white)
            frontier_cells.remove((cell[0], cell[1]))

            self.cells[cell[0], cell[1]].visit_cell()
            neighbours = self.cells[cell[0], cell[1]].get_neighbours()

            for neighbour in neighbours.items():
                if not neighbour[1].is_visited():
                    frontier_cells.add((neighbour[1].x, neighbour[1].y))

            visited_neigh = dict(filter(lambda elem: elem[1].is_visited()
                                        == True, neighbours.items()))
            if len(visited_neigh) > 0:
                random_neighbour = random.choice(list(visited_neigh.items()))
                edge = random_neighbour[0]
                self.edges[edge].setZValue(-1)

    def execute_search(self):
        self.reset_cells()
        self.path_found = False
        search_method = self.algorithms.currentText()
        if search_method == 'BFS':
            self.execute_BFS()
        elif search_method == 'DFS':
            self.cells[0, 0].set_arrived_from(None, None)
            self.execute_DFS(0, 0)
            self.draw_path()

    def execute_BFS(self):
        queue = []
        self.cells[0, 0].visit_cell()
        self.cells[0, 0].set_arrived_from(None, None)
        queue.append([0, 0])

        while len(queue) > 0:
            cell = queue.pop(0)
            self.delay()
            self.cells[cell[0], cell[1]].get_rect().setBrush(QBrush(QtGui.QColor(0, 0, 255)))
            if cell[0] == 780 and cell[1] == 780:
                break
            neighbours = self.cells[cell[0], cell[1]].get_neighbours()
            for n in list(neighbours.items()):
                neighbour = n[1]
                if not neighbour.is_visited():
                    self.cells[neighbour.x, neighbour.y].visit_cell()
                    neighbour.set_arrived_from(cell[0], cell[1])
                    queue.append([neighbour.x, neighbour.y])

        self.draw_path()

    def execute_DFS(self, x, y):
        self.delay()
        self.cells[x, y].get_rect().setBrush(QBrush(QtGui.QColor(0, 0, 255)))
        self.cells[x, y].visit_cell()
        if x == 780 and y == 780:
            self.path_found = True
            return
        neighbours = self.cells[x, y].get_neighbours()
        for n in list(neighbours.items()):
            if self.path_found:
                return
            neighbour = n[1]
            if not neighbour.is_visited():
                self.cells[neighbour.x, neighbour.y].visit_cell()
                neighbour.set_arrived_from(x, y)
                self.execute_DFS(neighbour.x, neighbour.y)

    def reset_cells(self):
        for cell in list(self.cells.items()):
            cell[1].visited = False

    def draw_path(self):
        cell = [780, 780]
        while True:
            self.cells[cell[0], cell[1]].get_rect().setBrush(QBrush(QtGui.QColor(255,0,0)))
            arrived_from = self.cells[cell[0], cell[1]].arrived_from
            if arrived_from == [None, None]:
                break
            cell = arrived_from
            self.delay()
