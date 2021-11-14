from PyQt5 import QtWidgets
import PyQt5
from PyQt5 import QtGui
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtWidgets import QGraphicsLineItem, QMainWindow, QGraphicsRectItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QTime, QEventLoop, QCoreApplication

import cell as c


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

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.edges = {}
        self.cells = {}
        self.speed = 20
        self.init_ui()

    def init_ui(self):
        self.setGeometry(X_POS, Y_POS, WIDTH, HEIGHT)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self)

        self.scene.setSceneRect(0,0, VIEW_W, VIEW_H)
        self.view.setGeometry(LEFT_MARGIN, TOP_MARGIN, VIEW_W + 20, VIEW_H + 20)
        self.view.setScene(self.scene)

        self.algorithms = QtWidgets.QComboBox(self)
        self.algorithms.setGeometry(20, 40, 100, 30)
        algorithms = ['BFS', 'DFS', 'Dijkstra', 'A*']
        self.algorithms.insertItems(0, algorithms)

        self.visualize_button = QtWidgets.QPushButton(self)
        self.visualize_button.setGeometry(20, 90, 100, 30)
        self.visualize_button.setText('Visualize')

        self.animation_speed = QtWidgets.QSlider(Qt.Horizontal, self)
        self.animation_speed.setGeometry(20, 160, 100, 20)
        self.animation_speed.setInvertedAppearance(True)
        self.animation_speed.setRange(1, 400)
        self.animation_speed.setValue(40)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setText('Animation Speed')
        self.text_label.move(25, 180)

        self.new_maze_button = QtWidgets.QPushButton(self)
        self.new_maze_button.setGeometry(20, 250, 100, 30)
        self.new_maze_button.setText('New Maze')

    
    def init_grid(self):
        pen = QPen(QtGui.QColor(0,0,0))
        pen.setWidth(2)
        edge1_id = 0
        for y in range(0 ,VIEW_H, STEP):
            for x in range(0 ,VIEW_W, STEP):
                edge1_id += 1

                edge1 = self.scene.addLine(0, 0, STEP, 0, pen)
                edge2 = self.scene.addLine(0, 0, 0, STEP, pen)

                edge1.moveBy(x, y)
                edge2.moveBy(x, y)

                self.edges[edge1_id] = edge1
                edge2_id = edge1_id + 1
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
                    edge1_id += 1
                    edge = self.scene.addLine(0, 0, 0, STEP, pen)
                    edge.moveBy(x + STEP, y)
                    self.edges[edge1_id] = edge1
                if y == VIEW_H - STEP:
                    edge1_id += 1
                    edge = self.scene.addLine(0, 0, STEP, 0, pen)
                    edge.moveBy(x, y + STEP)
                    self.edges[edge1_id] = edge1

    def create_cells(self):
        brush = QBrush(QtGui.QColor(0,0,255))
        pen = QPen(QtGui.QColor(0,0,0))
        for y in range(0 ,VIEW_H, STEP):
            for x in range(0 ,VIEW_W, STEP):
                rect = self.scene.addRect(0,0, CELL_SIZE, CELL_SIZE, pen, brush)
                rect.moveBy(x,y)
                new_cell = c.Cell(x, y, rect)
                self.cells[x, y] = new_cell
        


