from PyQt5 import QtWidgets,QtCore,QtGui
import logging

class QTextEditLogger(QtCore.QObject,logging.Handler):
    appendPlainText = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QTextEdit(parent)
        self.widget.setReadOnly(True)
        #self.setFormatter(CustomFormatter())
        # p = self.widget.palette()
        # p.setColor(self.widget.backgroundRole(), QtCore.Qt.gray)
        # self.widget.setPalette(p)
        # self.widget.setAutoFillBackground(True)
        #self.widget.setBackgroundRole(QtGui.QColor('gray'))
        self.appendPlainText.connect(self.widget.append)

    def debug(self,msg):
        super().debug(msg)

    def info(self,msg):
        color = self.TextColor()
        self.setTextColor(QtGui.QColor('red'))
        super().info(msg)
        self.setTextColor(color)


    def emit(self, record):
        if record.levelno == logging.DEBUG:
            color = "green"
        elif record.levelno == logging.INFO or record.levelno == 25:
            color = "black"
        elif record.levelno == logging.WARNING:
            color = "orange"
        elif record.levelno == logging.ERROR:
            color = "red"
        elif record.levelno == logging.CRITICAL:
            color = "purple"

        msg = self.format(record)
        

        self.widget.setTextColor(QtGui.QColor(color))
        weight = self.widget.fontWeight()
        if  record.levelno == 25:
            self.widget.setFontWeight(63) #demi-bold

        self.appendPlainText.emit(msg)
        self.widget.setTextColor(QtGui.QColor("black"))
        self.widget.setFontWeight(weight)

    def setMinimumSize(self,size:QtCore.QSize):
        self.widget.setMinimumSize(size)
    def setMaximumSize(self,size:QtCore.QSize):
        self.widget.setMaximumSize(size)
    def setObjectName(self,name):
        self.widget.setObjectName(name)
    def setEnabled(self,enabled_flag:bool):
        self.widget.setEnabled(enabled_flag)

    