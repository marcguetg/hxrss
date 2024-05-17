import PyQt5
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.patches as patches

import clscratch

class ApplicationWindow(QtWidgets.QMainWindow):
    """
    Application window for displaying crystal map.
    """
    def __init__(self, *, lpcb=None, corrparams=None, roi=None):
        """
        Initializes the application window.
        """
        super().__init__()
        self._main = QtWidgets.QWidget()
        roll_value = roi.roll[0]
        self.setWindowTitle('Crystal Map with roll angle '+ str(roll_value) + '°')
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(10, 8)))
        layout.addWidget(static_canvas)
        self.addToolBar(NavigationToolbar(static_canvas, self))
        self._static_ax = static_canvas.figure.subplots()
        clscratch.crystal_plot_core(None, static_canvas, self._static_ax, line_pick_cb=lpcb, corrparams=corrparams, roi=roi)

