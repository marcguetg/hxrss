# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hxrss_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(857, 787)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 840, 775))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.label_40 = QtWidgets.QLabel(self.tab)
        self.label_40.setMinimumSize(QtCore.QSize(150, 0))
        self.label_40.setObjectName("label_40")
        self.gridLayout.addWidget(self.label_40, 26, 0, 1, 1)
        self.mono1_roll_rb_display = QtWidgets.QLabel(self.tab)
        self.mono1_roll_rb_display.setObjectName("mono1_roll_rb_display")
        self.gridLayout.addWidget(self.mono1_roll_rb_display, 27, 1, 1, 5)
        self.label_20 = QtWidgets.QLabel(self.tab)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 9, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.tab)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 7, 0, 1, 11)
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setLineWidth(4)
        self.line.setMidLineWidth(4)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 8, 0, 1, 10)
        self.label_26 = QtWidgets.QLabel(self.tab)
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 10, 0, 1, 1)
        self.photonE = QtWidgets.QLineEdit(self.tab)
        self.photonE.setObjectName("photonE")
        self.gridLayout.addWidget(self.photonE, 9, 1, 1, 3)
        self.reflection_display = QtWidgets.QLabel(self.tab)
        self.reflection_display.setMinimumSize(QtCore.QSize(100, 0))
        self.reflection_display.setText("")
        self.reflection_display.setObjectName("reflection_display")
        self.gridLayout.addWidget(self.reflection_display, 9, 7, 1, 3)
        self.label_27 = QtWidgets.QLabel(self.tab)
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 20, 0, 1, 10)
        self.roll_angle_edit = QtWidgets.QLineEdit(self.tab)
        self.roll_angle_edit.setObjectName("roll_angle_edit")
        self.gridLayout.addWidget(self.roll_angle_edit, 10, 1, 1, 3)
        self.computed_pitch_angle_display = QtWidgets.QLabel(self.tab)
        self.computed_pitch_angle_display.setText("")
        self.computed_pitch_angle_display.setObjectName("computed_pitch_angle_display")
        self.gridLayout.addWidget(self.computed_pitch_angle_display, 16, 1, 1, 2)
        self.computed_pitch_angle_slope_display = QtWidgets.QLabel(self.tab)
        self.computed_pitch_angle_slope_display.setText("")
        self.computed_pitch_angle_slope_display.setObjectName("computed_pitch_angle_slope_display")
        self.gridLayout.addWidget(self.computed_pitch_angle_slope_display, 16, 8, 1, 2)
        self.calclabel = QtWidgets.QLabel(self.tab)
        self.calclabel.setText("")
        self.calclabel.setObjectName("calclabel")
        self.gridLayout.addWidget(self.calclabel, 12, 0, 1, 11)
        self.line_5 = QtWidgets.QFrame(self.tab)
        self.line_5.setLineWidth(4)
        self.line_5.setMidLineWidth(4)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout.addWidget(self.line_5, 19, 0, 1, 10)
        self.apply_button = QtWidgets.QPushButton(self.tab)
        self.apply_button.setObjectName("apply_button")
        self.gridLayout.addWidget(self.apply_button, 10, 9, 1, 1)
        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setMinimumSize(QtCore.QSize(0, 0))
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 5, 0, 1, 11)
        self.line_4 = QtWidgets.QFrame(self.tab)
        self.line_4.setLineWidth(4)
        self.line_4.setMidLineWidth(4)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 0, 0, 1, 10)
        self.line_6 = QtWidgets.QFrame(self.tab)
        self.line_6.setLineWidth(4)
        self.line_6.setMidLineWidth(4)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout.addWidget(self.line_6, 21, 0, 1, 10)
        self.label_25 = QtWidgets.QLabel(self.tab)
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 16, 3, 1, 3)
        self.photon_energy_edit = QtWidgets.QLineEdit(self.tab)
        self.photon_energy_edit.setObjectName("photon_energy_edit")
        self.gridLayout.addWidget(self.photon_energy_edit, 3, 1, 1, 5)
        self.label_38 = QtWidgets.QLabel(self.tab)
        self.label_38.setMinimumSize(QtCore.QSize(200, 0))
        self.label_38.setObjectName("label_38")
        self.gridLayout.addWidget(self.label_38, 23, 7, 1, 3)
        self.loglabel = QtWidgets.QLabel(self.tab)
        self.loglabel.setText("")
        self.loglabel.setObjectName("loglabel")
        self.gridLayout.addWidget(self.loglabel, 4, 0, 1, 11)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.line_7 = QtWidgets.QFrame(self.tab)
        self.line_7.setLineWidth(4)
        self.line_7.setMidLineWidth(4)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout.addWidget(self.line_7, 23, 6, 5, 1)
        self.label_24 = QtWidgets.QLabel(self.tab)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 1, 0, 1, 10)
        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setLineWidth(4)
        self.line_2.setMidLineWidth(4)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 6, 0, 1, 10)
        self.display_map_button = QtWidgets.QPushButton(self.tab)
        self.display_map_button.setObjectName("display_map_button")
        self.gridLayout.addWidget(self.display_map_button, 3, 8, 1, 1)
        self.tableButton = QtWidgets.QPushButton(self.tab)
        self.tableButton.setObjectName("tableButton")
        self.gridLayout.addWidget(self.tableButton, 3, 9, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.tab)
        self.line_3.setLineWidth(4)
        self.line_3.setMidLineWidth(4)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 2, 0, 1, 10)
        self.label_41 = QtWidgets.QLabel(self.tab)
        self.label_41.setMinimumSize(QtCore.QSize(150, 0))
        self.label_41.setObjectName("label_41")
        self.gridLayout.addWidget(self.label_41, 27, 0, 1, 1)
        self.mono1_crystal_inserted_display = QtWidgets.QLabel(self.tab)
        self.mono1_crystal_inserted_display.setObjectName("mono1_crystal_inserted_display")
        self.gridLayout.addWidget(self.mono1_crystal_inserted_display, 25, 1, 1, 5)
        self.mono2_roll_rb_display = QtWidgets.QLabel(self.tab)
        self.mono2_roll_rb_display.setObjectName("mono2_roll_rb_display")
        self.gridLayout.addWidget(self.mono2_roll_rb_display, 27, 7, 1, 3)
        self.label_39 = QtWidgets.QLabel(self.tab)
        self.label_39.setMinimumSize(QtCore.QSize(150, 0))
        self.label_39.setObjectName("label_39")
        self.gridLayout.addWidget(self.label_39, 25, 0, 1, 1)
        self.mono1_crystal_insert_button = QtWidgets.QPushButton(self.tab)
        self.mono1_crystal_insert_button.setObjectName("mono1_crystal_insert_button")
        self.gridLayout.addWidget(self.mono1_crystal_insert_button, 24, 1, 1, 3)
        self.mono2_crystal_park_button = QtWidgets.QPushButton(self.tab)
        self.mono2_crystal_park_button.setObjectName("mono2_crystal_park_button")
        self.gridLayout.addWidget(self.mono2_crystal_park_button, 24, 9, 1, 1)
        self.mono1_pitch_rb_display = QtWidgets.QLabel(self.tab)
        self.mono1_pitch_rb_display.setObjectName("mono1_pitch_rb_display")
        self.gridLayout.addWidget(self.mono1_pitch_rb_display, 26, 1, 1, 5)
        self.mono1_crystal_park_button = QtWidgets.QPushButton(self.tab)
        self.mono1_crystal_park_button.setMinimumSize(QtCore.QSize(0, 0))
        self.mono1_crystal_park_button.setObjectName("mono1_crystal_park_button")
        self.gridLayout.addWidget(self.mono1_crystal_park_button, 24, 4, 1, 2)
        self.label_37 = QtWidgets.QLabel(self.tab)
        self.label_37.setMinimumSize(QtCore.QSize(200, 0))
        self.label_37.setObjectName("label_37")
        self.gridLayout.addWidget(self.label_37, 23, 2, 1, 4)
        self.mono2_crystal_inserted_display = QtWidgets.QLabel(self.tab)
        self.mono2_crystal_inserted_display.setObjectName("mono2_crystal_inserted_display")
        self.gridLayout.addWidget(self.mono2_crystal_inserted_display, 25, 7, 1, 3)
        self.mono2_crystal_insert_button = QtWidgets.QPushButton(self.tab)
        self.mono2_crystal_insert_button.setObjectName("mono2_crystal_insert_button")
        self.gridLayout.addWidget(self.mono2_crystal_insert_button, 24, 7, 1, 2)
        self.line_8 = QtWidgets.QFrame(self.tab)
        self.line_8.setLineWidth(4)
        self.line_8.setMidLineWidth(4)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout.addWidget(self.line_8, 28, 0, 1, 10)
        self.mono2_pitch_rb_display = QtWidgets.QLabel(self.tab)
        self.mono2_pitch_rb_display.setObjectName("mono2_pitch_rb_display")
        self.gridLayout.addWidget(self.mono2_pitch_rb_display, 26, 7, 1, 3)
        self.label_23 = QtWidgets.QLabel(self.tab)
        self.label_23.setMinimumSize(QtCore.QSize(150, 0))
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 16, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 9, 5, 1, 1)
        self.scan_checkBox = QtWidgets.QCheckBox(self.tab)
        self.scan_checkBox.setObjectName("scan_checkBox")
        self.gridLayout.addWidget(self.scan_checkBox, 17, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.tab)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 17, 3, 1, 3)
        self.undulatorph = QtWidgets.QDoubleSpinBox(self.tab)
        self.undulatorph.setEnabled(True)
        self.undulatorph.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.undulatorph.setReadOnly(True)
        self.undulatorph.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.undulatorph.setDecimals(1)
        self.undulatorph.setMaximum(25000.0)
        self.undulatorph.setObjectName("undulatorph")
        self.gridLayout.addWidget(self.undulatorph, 17, 8, 1, 1)
        self.scanlabel = QtWidgets.QLabel(self.tab)
        self.scanlabel.setText("")
        self.scanlabel.setObjectName("scanlabel")
        self.gridLayout.addWidget(self.scanlabel, 18, 0, 1, 10)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.params_report_button = QtWidgets.QPushButton(self.tab_2)
        self.params_report_button.setGeometry(QtCore.QRect(70, 110, 171, 21))
        self.params_report_button.setObjectName("params_report_button")
        self.params_default_button = QtWidgets.QPushButton(self.tab_2)
        self.params_default_button.setGeometry(QtCore.QRect(70, 140, 171, 21))
        self.params_default_button.setObjectName("params_default_button")
        self.params_fromDOOCS_button = QtWidgets.QPushButton(self.tab_2)
        self.params_fromDOOCS_button.setGeometry(QtCore.QRect(70, 170, 171, 21))
        self.params_fromDOOCS_button.setObjectName("params_fromDOOCS_button")
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(60, 550, 701, 141))
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
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(60, 260, 701, 141))
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
        self.color1_detuning_edit.setReadOnly(True)
        self.color1_detuning_edit.setObjectName("color1_detuning_edit")
        self.color2_detuning_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.color2_detuning_edit.setGeometry(QtCore.QRect(100, 80, 61, 23))
        self.color2_detuning_edit.setReadOnly(True)
        self.color2_detuning_edit.setObjectName("color2_detuning_edit")
        self.color3_detuning_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.color3_detuning_edit.setGeometry(QtCore.QRect(100, 110, 61, 23))
        self.color3_detuning_edit.setReadOnly(True)
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
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_3.setGeometry(QtCore.QRect(60, 430, 701, 101))
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
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_4.setGeometry(QtCore.QRect(60, 60, 711, 171))
        self.groupBox_4.setObjectName("groupBox_4")
        self.update_table_button = QtWidgets.QPushButton(self.groupBox_4)
        self.update_table_button.setGeometry(QtCore.QRect(240, 50, 171, 21))
        self.update_table_button.setObjectName("update_table_button")
        self.groupBox_4.raise_()
        self.params_report_button.raise_()
        self.params_default_button.raise_()
        self.params_fromDOOCS_button.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.groupBox_3.raise_()
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 857, 24))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionExpert_Settings = QtWidgets.QAction(MainWindow)
        self.actionExpert_Settings.setObjectName("actionExpert_Settings")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HXRSS GUI v0.9"))
        self.label_40.setText(_translate("MainWindow", "Pitch Angle:"))
        self.mono1_roll_rb_display.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> </p></body></html>"))
        self.label_20.setText(_translate("MainWindow", "Photon Energy [ev]"))
        self.label_21.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Crystal Configuration Calculator</span></p></body></html>"))
        self.label_26.setText(_translate("MainWindow", "Roll Angle [°]"))
        self.label_27.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Crystal Status</span></p></body></html>"))
        self.apply_button.setText(_translate("MainWindow", "Apply"))
        self.label_25.setText(_translate("MainWindow", "Pitch: Local Derivative [eV/deg]"))
        self.label_38.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Monochromator 2</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Photon Energy [eV]"))
        self.label_24.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">HXRSS Crystal Set Tool</span></p></body></html>"))
        self.display_map_button.setText(_translate("MainWindow", "Display Map"))
        self.tableButton.setText(_translate("MainWindow", "Clear Table Selection"))
        self.label_41.setText(_translate("MainWindow", "Roll Angle:"))
        self.mono1_crystal_inserted_display.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"/></body></html>"))
        self.mono2_roll_rb_display.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"/></body></html>"))
        self.label_39.setText(_translate("MainWindow", "Inserted/Parked:"))
        self.mono1_crystal_insert_button.setText(_translate("MainWindow", "Insert"))
        self.mono2_crystal_park_button.setText(_translate("MainWindow", "Park"))
        self.mono1_pitch_rb_display.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"/></body></html>"))
        self.mono1_crystal_park_button.setText(_translate("MainWindow", "Park"))
        self.label_37.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Monochromator 1</span></p></body></html>"))
        self.mono2_crystal_inserted_display.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"/></body></html>"))
        self.mono2_crystal_insert_button.setText(_translate("MainWindow", "Insert"))
        self.mono2_pitch_rb_display.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"/></body></html>"))
        self.label_23.setText(_translate("MainWindow", "Computed Pitch Angle"))
        self.label_2.setText(_translate("MainWindow", "Reflection:"))
        self.scan_checkBox.setText(_translate("MainWindow", "Scan mode"))
        self.label_22.setText(_translate("MainWindow", "Undulator Photon Energy [ev]"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tool"))
        self.params_report_button.setText(_translate("MainWindow", "Report Params"))
        self.params_default_button.setText(_translate("MainWindow", "Default Params"))
        self.params_fromDOOCS_button.setText(_translate("MainWindow", "Load Params from DOOCS"))
        self.groupBox.setTitle(_translate("MainWindow", "Monochromator crystal essentials"))
        self.label_3.setText(_translate("MainWindow", "mono2"))
        self.label_4.setText(_translate("MainWindow", "mono1"))
        self.mono2_pitch_sp_display.setText(_translate("MainWindow", "TextLabel"))
        self.mono2_roll_sp_display.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "pitch angle"))
        self.label_6.setText(_translate("MainWindow", "roll angle"))
        self.mono1_pitch_sp_display.setText(_translate("MainWindow", "TextLabel"))
        self.mono1_roll_sp_display.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "setpoint"))
        self.label_8.setText(_translate("MainWindow", "setpoint"))
        self.label_13.setText(_translate("MainWindow", "readback"))
        self.label_14.setText(_translate("MainWindow", "readback"))
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
        self.groupBox_3.setTitle(_translate("MainWindow", "Machine I/O"))
        self.label_19.setText(_translate("MainWindow", "I/O processing time [ms]"))
        self.label_17.setText(_translate("MainWindow", "last tag ID seen from thread"))
        self.label_18.setText(_translate("MainWindow", "age of last msg [s]"))
        self.io_threaddbg_checkbox.setText(_translate("MainWindow", "dbg I/O thread"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Update Parameters"))
        self.update_table_button.setText(_translate("MainWindow", "Update Config Table"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Expert Settings"))
        self.actionExpert_Settings.setText(_translate("MainWindow", "Expert Settings"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
