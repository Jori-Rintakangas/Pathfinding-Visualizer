from PyQt5 import QtWidgets
import PyQt5
from PyQt5 import QtGui
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsLineItem, QMainWindow
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QTime, QEventLoop, QCoreApplication


X_POS = 50
Y_POS = 300
WIDTH = 1000
HEIGHT = 900
VIEW_W = 800
VIEW_H = 800
LEFT_MARGIN = 140
TOP_MARGIN = 40

STEP = 10
START = 100

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.speed = 20
        self.init_ui()

    def init_ui(self):
        self.setGeometry(X_POS, Y_POS, WIDTH, HEIGHT)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self)

        self.scene.setSceneRect(0,0, VIEW_W - 2, VIEW_H - 2)
        self.view.setGeometry(LEFT_MARGIN, TOP_MARGIN, VIEW_W, VIEW_H)
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
