# based on Matplotlib example source code
# https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_sgskip.html (last access 2021-Oct)

# added this
import PyQt5

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

import clscratch

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, lpcb=None):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setWindowTitle('Crystal Map')
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(12, 8)))
        layout.addWidget(static_canvas)
        self.addToolBar(NavigationToolbar(static_canvas, self))
        self._static_ax = static_canvas.figure.subplots()
        clscratch.stuff2000_core(None,static_canvas,self._static_ax, line_pick_cb=lpcb)

