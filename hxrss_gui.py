#!/usr/bin/env python3

from hxrss_main_window import Ui_MainWindow

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

# from clscratch import stuff2000
import do_crystal_plot

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.display_map_button.clicked.connect(self.demo)

    def demo(self):
        x = self.photon_energy_edit.text()
        print('value='+x)
        # stuff2000()
        blah = do_crystal_plot.ApplicationWindow()
        blah.show()
        blah.activateWindow()
        print('abc')

app = qtw.QApplication([])

w = MainWindow()
w.show()

app.exec_()
