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
        self.label_2.setGeometry(QtCore.QRect(10, 100, 121, 16))
        self.label_2.setObjectName("label_2")
        self.photon_energy_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.photon_energy_edit.setGeometry(QtCore.QRect(140, 20, 113, 23))
        self.photon_energy_edit.setObjectName("photon_energy_edit")
        self.display_map_button = QtWidgets.QPushButton(self.centralwidget)
        self.display_map_button.setGeometry(QtCore.QRect(140, 120, 111, 23))
        self.display_map_button.setObjectName("display_map_button")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(270, 100, 491, 141))
        self.groupBox.setObjectName("groupBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(310, 30, 151, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(130, 30, 141, 16))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.mono2_pitch_sp_display = QtWidgets.QLabel(self.groupBox)
        self.mono2_pitch_sp_display.setGeometry(QtCore.QRect(300, 70, 81, 20))
        self.mono2_pitch_sp_display.setObjectName("mono2_pitch_sp_display")
        self.mono2_roll_sp_display = QtWidgets.QLabel(self.groupBox)
        self.mono2_roll_sp_display.setGeometry(QtCore.QRect(300, 90, 81, 20))
        self.mono2_roll_sp_display.setObjectName("mono2_roll_sp_display")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 70, 91, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 90, 91, 21))
        self.label_6.setObjectName("label_6")
        self.mono1_pitch_sp_display = QtWidgets.QLabel(self.groupBox)
        self.mono1_pitch_sp_display.setGeometry(QtCore.QRect(120, 70, 81, 20))
        self.mono1_pitch_sp_display.setObjectName("mono1_pitch_sp_display")
        self.mono1_roll_sp_display = QtWidgets.QLabel(self.groupBox)
        self.mono1_roll_sp_display.setGeometry(QtCore.QRect(120, 90, 81, 20))
        self.mono1_roll_sp_display.setObjectName("mono1_roll_sp_display")
        self.mono2_pitch_rb_display = QtWidgets.QLabel(self.groupBox)
        self.mono2_pitch_rb_display.setGeometry(QtCore.QRect(400, 70, 81, 20))
        self.mono2_pitch_rb_display.setObjectName("mono2_pitch_rb_display")
        self.mono2_roll_rb_display = QtWidgets.QLabel(self.groupBox)
        self.mono2_roll_rb_display.setGeometry(QtCore.QRect(400, 90, 81, 20))
        self.mono2_roll_rb_display.setObjectName("mono2_roll_rb_display")
        self.mono1_pitch_rb_display = QtWidgets.QLabel(self.groupBox)
        self.mono1_pitch_rb_display.setGeometry(QtCore.QRect(210, 70, 81, 20))
        self.mono1_pitch_rb_display.setObjectName("mono1_pitch_rb_display")
        self.mono1_roll_rb_display = QtWidgets.QLabel(self.groupBox)
        self.mono1_roll_rb_display.setGeometry(QtCore.QRect(210, 90, 81, 20))
        self.mono1_roll_rb_display.setObjectName("mono1_roll_rb_display")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(120, 50, 71, 16))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(300, 50, 71, 16))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(210, 50, 71, 16))
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setGeometry(QtCore.QRect(400, 50, 71, 16))
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.mono2_crystal_insert_button = QtWidgets.QPushButton(self.groupBox)
        self.mono2_crystal_insert_button.setGeometry(QtCore.QRect(300, 110, 61, 21))
        self.mono2_crystal_insert_button.setObjectName("mono2_crystal_insert_button")
        self.mono2_crystal_park_button = QtWidgets.QPushButton(self.groupBox)
        self.mono2_crystal_park_button.setGeometry(QtCore.QRect(400, 110, 61, 21))
        self.mono2_crystal_park_button.setObjectName("mono2_crystal_park_button")
        self.label_22 = QtWidgets.QLabel(self.groupBox)
        self.label_22.setGeometry(QtCore.QRect(20, 110, 91, 21))
        self.label_22.setObjectName("label_22")
        self.reflection_display = QtWidgets.QLabel(self.centralwidget)
        self.reflection_display.setGeometry(QtCore.QRect(140, 100, 111, 16))
        self.reflection_display.setText("")
        self.reflection_display.setObjectName("reflection_display")
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(430, 20, 221, 16))
        self.horizontalScrollBar.setMinimum(-100)
        self.horizontalScrollBar.setMaximum(100)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(270, 270, 491, 141))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(10, 50, 71, 21))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(100, 30, 81, 20))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(190, 30, 121, 21))
        self.label_11.setObjectName("label_11")
        self.color1_sp_display = QtWidgets.QLabel(self.groupBox_2)
        self.color1_sp_display.setGeometry(QtCore.QRect(190, 50, 121, 21))
        self.color1_sp_display.setText("")
        self.color1_sp_display.setObjectName("color1_sp_display")
        self.color2_sp_display = QtWidgets.QLabel(self.groupBox_2)
        self.color2_sp_display.setGeometry(QtCore.QRect(190, 80, 121, 21))
        self.color2_sp_display.setText("")
        self.color2_sp_display.setObjectName("color2_sp_display")
        self.color3_sp_display = QtWidgets.QLabel(self.groupBox_2)
        self.color3_sp_display.setGeometry(QtCore.QRect(190, 110, 121, 21))
        self.color3_sp_display.setText("")
        self.color3_sp_display.setObjectName("color3_sp_display")
        self.label_15 = QtWidgets.QLabel(self.groupBox_2)
        self.label_15.setGeometry(QtCore.QRect(10, 80, 71, 21))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.groupBox_2)
        self.label_16.setGeometry(QtCore.QRect(10, 110, 71, 21))
        self.label_16.setObjectName("label_16")
        self.color1_detuning_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.color1_detuning_edit.setGeometry(QtCore.QRect(100, 50, 61, 23))
        self.color1_detuning_edit.setObjectName("color1_detuning_edit")
        self.color2_detuning_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.color2_detuning_edit.setGeometry(QtCore.QRect(100, 80, 61, 23))
        self.color2_detuning_edit.setObjectName("color2_detuning_edit")
        self.color3_detuning_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.color3_detuning_edit.setGeometry(QtCore.QRect(100, 110, 61, 23))
        self.color3_detuning_edit.setObjectName("color3_detuning_edit")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(330, 30, 121, 21))
        self.label_12.setObjectName("label_12")
        self.color3_rb_display = QtWidgets.QLabel(self.groupBox_2)
        self.color3_rb_display.setGeometry(QtCore.QRect(330, 110, 121, 21))
        self.color3_rb_display.setText("")
        self.color3_rb_display.setObjectName("color3_rb_display")
        self.color1_rb_display = QtWidgets.QLabel(self.groupBox_2)
        self.color1_rb_display.setGeometry(QtCore.QRect(330, 50, 121, 21))
        self.color1_rb_display.setText("")
        self.color1_rb_display.setObjectName("color1_rb_display")
        self.color2_rb_display = QtWidgets.QLabel(self.groupBox_2)
        self.color2_rb_display.setGeometry(QtCore.QRect(330, 80, 121, 21))
        self.color2_rb_display.setText("")
        self.color2_rb_display.setObjectName("color2_rb_display")
        self.apply_button = QtWidgets.QPushButton(self.centralwidget)
        self.apply_button.setGeometry(QtCore.QRect(650, 80, 111, 23))
        self.apply_button.setObjectName("apply_button")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(270, 440, 491, 101))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_19 = QtWidgets.QLabel(self.groupBox_3)
        self.label_19.setGeometry(QtCore.QRect(10, 50, 191, 21))
        self.label_19.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.label_17 = QtWidgets.QLabel(self.groupBox_3)
        self.label_17.setGeometry(QtCore.QRect(10, 30, 191, 21))
        self.label_17.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.io_processingtime_display = QtWidgets.QLabel(self.groupBox_3)
        self.io_processingtime_display.setGeometry(QtCore.QRect(210, 50, 91, 21))
        self.io_processingtime_display.setText("")
        self.io_processingtime_display.setObjectName("io_processingtime_display")
        self.io_msgtag_display = QtWidgets.QLabel(self.groupBox_3)
        self.io_msgtag_display.setGeometry(QtCore.QRect(210, 30, 91, 21))
        self.io_msgtag_display.setText("")
        self.io_msgtag_display.setObjectName("io_msgtag_display")
        self.io_msgage_display = QtWidgets.QLabel(self.groupBox_3)
        self.io_msgage_display.setGeometry(QtCore.QRect(210, 70, 91, 21))
        self.io_msgage_display.setText("")
        self.io_msgage_display.setObjectName("io_msgage_display")
        self.label_18 = QtWidgets.QLabel(self.groupBox_3)
        self.label_18.setGeometry(QtCore.QRect(10, 70, 191, 21))
        self.label_18.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.io_threaddbg_checkbox = QtWidgets.QCheckBox(self.groupBox_3)
        self.io_threaddbg_checkbox.setGeometry(QtCore.QRect(320, 30, 151, 21))
        self.io_threaddbg_checkbox.setObjectName("io_threaddbg_checkbox")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(10, 50, 121, 16))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(10, 70, 121, 16))
        self.label_21.setObjectName("label_21")
        self.photon_energy_min_display = QtWidgets.QLabel(self.centralwidget)
        self.photon_energy_min_display.setGeometry(QtCore.QRect(140, 50, 111, 16))
        self.photon_energy_min_display.setText("")
        self.photon_energy_min_display.setObjectName("photon_energy_min_display")
        self.photon_energy_max_display = QtWidgets.QLabel(self.centralwidget)
        self.photon_energy_max_display.setGeometry(QtCore.QRect(140, 70, 111, 16))
        self.photon_energy_max_display.setText("")
        self.photon_energy_max_display.setObjectName("photon_energy_max_display")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "HXRSS GUI v0.9"))
        self.label.setText(_translate("MainWindow", "Photon Energy [eV]"))
        self.label_2.setText(_translate("MainWindow", "Reflection"))
        self.display_map_button.setText(_translate("MainWindow", "Display Map"))
        self.groupBox.setTitle(_translate("MainWindow", "Monochromator crystal essentials"))
        self.label_3.setText(_translate("MainWindow", "mono2"))
        self.label_4.setText(_translate("MainWindow", "mono1"))
        self.mono2_pitch_sp_display.setText(_translate("MainWindow", "TextLabel"))
        self.mono2_roll_sp_display.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "pitch angle"))
        self.label_6.setText(_translate("MainWindow", "roll angle"))
        self.mono1_pitch_sp_display.setText(_translate("MainWindow", "TextLabel"))
        self.mono1_roll_sp_display.setText(_translate("MainWindow", "TextLabel"))
        self.mono2_pitch_rb_display.setText(_translate("MainWindow", "TextLabel"))
        self.mono2_roll_rb_display.setText(_translate("MainWindow", "TextLabel"))
        self.mono1_pitch_rb_display.setText(_translate("MainWindow", "TextLabel"))
        self.mono1_roll_rb_display.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "setpoint"))
        self.label_8.setText(_translate("MainWindow", "setpoint"))
        self.label_13.setText(_translate("MainWindow", "readback"))
        self.label_14.setText(_translate("MainWindow", "readback"))
        self.mono2_crystal_insert_button.setText(_translate("MainWindow", "Insert"))
        self.mono2_crystal_park_button.setText(_translate("MainWindow", "Park"))
        self.label_22.setText(_translate("MainWindow", "crystal status"))
        self.groupBox_2.setTitle(_translate("MainWindow", "undulator segments (SASE2 \"colors\")"))
        self.label_9.setText(_translate("MainWindow", "Color 1"))
        self.label_10.setText(_translate("MainWindow", "Detuning"))
        self.label_11.setText(_translate("MainWindow", "resulting setpoint"))
        self.label_15.setText(_translate("MainWindow", "Color 2"))
        self.label_16.setText(_translate("MainWindow", "Color 3"))
        self.color1_detuning_edit.setText(_translate("MainWindow", "0"))
        self.color2_detuning_edit.setText(_translate("MainWindow", "0"))
        self.color3_detuning_edit.setText(_translate("MainWindow", "0"))
        self.label_12.setText(_translate("MainWindow", "readback value"))
        self.apply_button.setText(_translate("MainWindow", "Apply"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Machine I/O"))
        self.label_19.setText(_translate("MainWindow", "I/O processing time [ms]"))
        self.label_17.setText(_translate("MainWindow", "last tag ID seen from thread"))
        self.label_18.setText(_translate("MainWindow", "age of last msg [s]"))
        self.io_threaddbg_checkbox.setText(_translate("MainWindow", "dbg I/O thread"))
        self.label_20.setText(_translate("MainWindow", "Min Photon Energy"))
        self.label_21.setText(_translate("MainWindow", "Max Photon Energy"))

