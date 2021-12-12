from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QEventLoop, QTimer
import cell as c
import random
import sys

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
        self.white = QBrush(QtGui.QColor(255, 255, 255))
        self.blue = QBrush(QtGui.QColor(0, 0, 255))
        self.red = QBrush(QtGui.QColor(255, 0, 0))
        self.white_pen = QPen(QtGui.QColor(255, 255, 255))
        self.black_pen = QPen(QtGui.QColor(0, 0, 0))
        self.white_pen.setWidth(-1)
        self.black_pen.setWidth(2)
        self.path_found = False
        self.delay_loop = QEventLoop()
        self.init_ui()

    def closeEvent(self, event):
        event.accept()
        sys.exit(self.delay_loop.exit())

    def init_ui(self):
        self.setGeometry(X_POS, Y_POS, WIDTH, HEIGHT)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self)

        self.scene.setSceneRect(0, 0, VIEW_W, VIEW_H)
        self.view.setGeometry(LEFT_MARGIN, TOP_MARGIN, VIEW_W + 20, VIEW_H + 20)
        self.view.setScene(self.scene)

        self.algorithm_label = QtWidgets.QLabel(self)
        self.algorithm_label.setText('Path Finding:')
        self.algorithm_label.setStyleSheet("font-weight: bold; color: black")
        self.algorithm_label.move(20, 30)

        self.algorithms = QtWidgets.QComboBox(self)
        self.algorithms.setGeometry(20, 55, 100, 30)
        algorithms = ['BFS', 'DFS']
        self.algorithms.insertItems(0, algorithms)

        self.maze_label = QtWidgets.QLabel(self)
        self.maze_label.setText('Maze Creation:')
        self.maze_label.setStyleSheet("font-weight: bold; color: black")
        self.maze_label.move(20, 85)

        self.maze_algorithms = QtWidgets.QComboBox(self)
        self.maze_algorithms.setGeometry(20, 110, 100, 30)
        maze_algorithms = ['Randomized DFS', 'Randomized Prim']
        self.maze_algorithms.insertItems(0, maze_algorithms)

        self.new_maze_button = QtWidgets.QPushButton(self)
        self.new_maze_button.setGeometry(20, 170, 100, 30)
        self.new_maze_button.setText('Create Maze')
        self.new_maze_button.clicked.connect(self.create_maze)

        self.visualize_button = QtWidgets.QPushButton(self)
        self.visualize_button.setGeometry(20, 210, 100, 30)
        self.visualize_button.setText('Find Path')
        self.visualize_button.clicked.connect(self.execute_search)
        self.visualize_button.setEnabled(False)

        self.animation_speed = QtWidgets.QSlider(Qt.Horizontal, self)
        self.animation_speed.setGeometry(20, 280, 100, 20)
        self.animation_speed.setInvertedAppearance(True)
        self.animation_speed.setRange(1, 60)
        self.animation_speed.setValue(20)
        self.animation_speed.valueChanged.connect(self.change_speed)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setText('Animation Speed')
        self.text_label.setStyleSheet("font-weight: bold; color: black")
        self.text_label.move(25, 300)

    def change_speed(self):
        self.speed = self.animation_speed.value()

    def delay(self):
        self.delay_loop = QEventLoop()
        QTimer.singleShot(self.speed, self.delay_loop.quit)
        self.delay_loop.exec_()
    
    def init_grid(self):
        edge1_id = 0
        edge2_id = 0
        for y in range(0, VIEW_H, STEP):
            for x in range(0, VIEW_W, STEP):
                edge1_id += 1
                edge2_id -= 1
                edge1 = self.scene.addLine(0, 0, STEP, 0, self.black_pen)
                edge2 = self.scene.addLine(0, 0, 0, STEP, self.black_pen)

                edge1.moveBy(x, y)
                edge2.moveBy(x, y)

                self.edges[edge1_id] = edge1
                self.edges[edge2_id] = edge2

                if y == 0 and x == 0:
                    continue

                if y == 0:
                    cell1 = self.cells[x, y]
                    cell2 = self.cells[x - STEP, y]
                    cell1.add_neighbour(cell2, edge2_id)
                    cell2.add_neighbour(cell1, edge2_id)
                
                elif x == 0:
                    cell1 = self.cells[x, y]
                    cell2 = self.cells[x, y - STEP]
                    cell1.add_neighbour(cell2, edge1_id)
                    cell2.add_neighbour(cell1, edge1_id)
                
                else:
                    cell1 = self.cells[x, y]
                    cell2 = self.cells[x - STEP, y]
                    cell3 = self.cells[x, y - STEP]

                    cell1.add_neighbour(cell2, edge2_id)
                    cell2.add_neighbour(cell1, edge2_id)

                    cell1.add_neighbour(cell3, edge1_id)
                    cell3.add_neighbour(cell1, edge1_id)

                if x == VIEW_W - STEP:
                    edge2_id -= 1
                    edge2 = self.scene.addLine(0, 0, 0, STEP, self.black_pen)
                    edge2.moveBy(x + STEP, y)
                    self.edges[edge2_id] = edge2
                if y == VIEW_H - STEP:
                    edge1_id += 1
                    edge1 = self.scene.addLine(0, 0, STEP, 0, self.black_pen)
                    edge1.moveBy(x, y + STEP)
                    self.edges[edge1_id] = edge1

    def create_cells(self):
        for y in range(0, VIEW_H, STEP):
            for x in range(0, VIEW_W, STEP):
                rect = self.scene.addRect(0, 0, CELL_SIZE, CELL_SIZE,
                                          self.white_pen, self.blue)
                rect.moveBy(x, y)
                new_cell = c.Cell(x, y, rect)
                self.cells[x, y] = new_cell

    def create_maze(self):
        self.visualize_button.setEnabled(False)
        self.new_maze_button.setEnabled(False)
        self.cells.clear()
        self.edges.clear()
        self.create_cells()
        self.init_grid()
        creation_method = self.maze_algorithms.currentText()
        if creation_method == 'Randomized DFS':
            self.create_maze_DFS(0, 0)
        elif creation_method == 'Randomized Prim':
            self.create_maze_prim(0, 0)
        self.visualize_button.setEnabled(True)
        self.new_maze_button.setEnabled(True)
        self.animation_speed.setValue(20)

    def create_maze_DFS(self, x, y):
        self.delay()
        cell = self.cells[x, y]
        cell.visit_cell()
        cell.get_rect().setBrush(self.white)
        all_visited = False
        while not all_visited:
            neighbours = cell.get_neighbours()
            if not neighbours:
                break
            rand_neigh = random.choice(list(neighbours.items()))
            edge = rand_neigh[0]
            neighbour = rand_neigh[1]
            if not neighbour.is_visited():
                neighbour.visit_cell()
                self.edges[edge].setZValue(-1)
                self.create_maze_DFS(neighbour.x, neighbour.y)

            if all(n.is_visited() for n in neighbours.values()):
                all_visited = True

        for edge, neighbour in list(neighbours.items()):
            if self.edges[edge].zValue() == 0:
                cell.delete_neighbour(edge)

    def create_maze_prim(self, x, y):
        self.cells[x, y].visit_cell()
        self.cells[x, y].get_rect().setBrush(self.white)
        frontier_cells = set()
        frontier_cells.add((x, y))
        while len(frontier_cells) > 0:
            self.delay()

            random_cell = random.choice(list(frontier_cells))
            cell = self.cells[random_cell[0], random_cell[1]]
            cell.get_rect().setBrush(self.white)
            cell.visit_cell()

            frontier_cells.remove((cell.x, cell.y))

            neighbours = cell.get_neighbours()
            for neighbour in neighbours.items():
                if not neighbour[1].is_visited():
                    frontier_cells.add((neighbour[1].x, neighbour[1].y))

            visited_neigh = dict(filter(lambda elem: elem[1].is_visited()
                                        == True, neighbours.items()))
            if len(visited_neigh) > 0:
                random_neighbour = random.choice(list(visited_neigh.items()))
                edge = random_neighbour[0]
                self.edges[edge].setZValue(-1)

        for coord, cell in list(self.cells.items()):
            neighbours = cell.get_neighbours()
            for edge, neighbour in list(neighbours.items()):
                if self.edges[edge].zValue() == 0:
                    cell.delete_neighbour(edge)

    def execute_search(self):
        self.reset_cells()
        self.path_found = False
        self.new_maze_button.setEnabled(False)
        self.visualize_button.setEnabled(False)
        search_method = self.algorithms.currentText()
        if search_method == 'BFS':
            self.execute_BFS(0, 0)
        elif search_method == 'DFS':
            self.cells[0, 0].set_arrived_from(None, None)
            self.execute_DFS(0, 0)
        self.draw_path()
        self.new_maze_button.setEnabled(True)
        self.visualize_button.setEnabled(True)
        self.animation_speed.setValue(20)

    def execute_BFS(self, x, y):
        queue = []
        self.cells[x, y].visit_cell()
        self.cells[x, y].set_arrived_from(None, None)
        queue.append([x, y])

        while len(queue) > 0:
            self.delay()
            coords = queue.pop(0)
            cell = self.cells[coords[0], coords[1]]
            cell.get_rect().setBrush(self.blue)
            if coords[0] == 780 and coords[1] == 780:
                break
            neighbours = cell.get_neighbours()
            for n in list(neighbours.items()):
                neighbour = n[1]
                if not neighbour.is_visited():
                    self.cells[neighbour.x, neighbour.y].visit_cell()
                    neighbour.set_arrived_from(coords[0], coords[1])
                    queue.append([neighbour.x, neighbour.y])

    def execute_DFS(self, x, y):
        self.delay()
        cell = self.cells[x, y]
        cell.get_rect().setBrush(self.blue)
        cell.visit_cell()
        if x == 780 and y == 780:
            self.path_found = True
            return
        neighbours = cell.get_neighbours()
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
            cell[1].get_rect().setBrush(self.white)
            cell[1].visited = False

    def draw_path(self):
        self.animation_speed.setValue(20)
        cell = [780, 780]
        while True:
            cell = self.cells[cell[0], cell[1]]
            cell.get_rect().setBrush(self.red)
            arrived_from = cell.arrived_from
            if arrived_from == [None, None]:
                break
            cell = arrived_from
            self.delay()
