from PyQt5 import QtWidgets,QtCore,QtGui
import logging

class QTextEditLogger(QtCore.QObject,logging.Handler):
    appendPlainText = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QTextEdit(parent)
        self.widget.setReadOnly(True)
        # p = self.widget.palette()
        # p.setColor(self.widget.backgroundRole(), QtCore.Qt.gray)
        # self.widget.setPalette(p)
        # self.widget.setAutoFillBackground(True)
        #self.widget.setBackgroundRole(QtGui.QColor('gray'))
        self.appendPlainText.connect(self.widget.append)

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)

    def setMinimumSize(self,size:QtCore.QSize):
        self.widget.setMinimumSize(size)
    def setMaximumSize(self,size:QtCore.QSize):
        self.widget.setMaximumSize(size)
    def setObjectName(self,name):
        self.widget.setObjectName(name)
    def setEnabled(self,enabled_flag:bool):
        self.widget.setEnabled(enabled_flag)

        
