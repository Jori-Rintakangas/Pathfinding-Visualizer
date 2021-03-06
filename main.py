import sys
from PyQt5.QtWidgets import QApplication
import window as w


def create_window():
    app = QApplication(sys.argv)
    win = w.MyWindow()
    win.show()
    win.create_cells()
    win.init_grid()
    sys.exit(app.exec_())


create_window()
