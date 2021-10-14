# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hxrss_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 121, 16))
        self.label_2.setObjectName("label_2")
        self.photon_energy_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.photon_energy_edit.setGeometry(QtCore.QRect(140, 20, 113, 23))
        self.photon_energy_edit.setObjectName("photon_energy_edit")
        self.display_map_button = QtWidgets.QPushButton(self.centralwidget)
        self.display_map_button.setGeometry(QtCore.QRect(140, 70, 111, 23))
        self.display_map_button.setObjectName("display_map_button")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(170, 210, 411, 201))
        self.groupBox.setObjectName("groupBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(270, 40, 91, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(170, 40, 57, 15))
        self.label_4.setObjectName("label_4")
        self.mono2_pitch_display = QtWidgets.QLabel(self.groupBox)
        self.mono2_pitch_display.setGeometry(QtCore.QRect(270, 70, 91, 20))
        self.mono2_pitch_display.setObjectName("mono2_pitch_display")
        self.mono2_roll_display = QtWidgets.QLabel(self.groupBox)
        self.mono2_roll_display.setGeometry(QtCore.QRect(270, 100, 91, 20))
        self.mono2_roll_display.setObjectName("mono2_roll_display")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 70, 91, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 100, 91, 21))
        self.label_6.setObjectName("label_6")
        self.mono1_pitch_display = QtWidgets.QLabel(self.groupBox)
        self.mono1_pitch_display.setGeometry(QtCore.QRect(170, 70, 91, 20))
        self.mono1_pitch_display.setObjectName("mono1_pitch_display")
        self.mono1_roll_display = QtWidgets.QLabel(self.groupBox)
        self.mono1_roll_display.setGeometry(QtCore.QRect(170, 100, 91, 20))
        self.mono1_roll_display.setObjectName("mono1_roll_display")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Photon Energy"))
        self.label_2.setText(_translate("MainWindow", "Reflection"))
        self.display_map_button.setText(_translate("MainWindow", "Display Map"))
        self.groupBox.setTitle(_translate("MainWindow", "computed setpoints"))
        self.label_3.setText(_translate("MainWindow", "mono2"))
        self.label_4.setText(_translate("MainWindow", "mono1"))
        self.mono2_pitch_display.setText(_translate("MainWindow", "TextLabel"))
        self.mono2_roll_display.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "pitch angle"))
        self.label_6.setText(_translate("MainWindow", "roll angle"))
        self.mono1_pitch_display.setText(_translate("MainWindow", "TextLabel"))
        self.mono1_roll_display.setText(_translate("MainWindow", "TextLabel"))

