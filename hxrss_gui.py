#!/usr/bin/env python3

from hxrss_main_window import Ui_MainWindow
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import QTimer

import threading,queue
import time
from types import SimpleNamespace
import enum
from copy import deepcopy
import pydoocs

# from clscratch import stuff2000
import do_crystal_plot

class IO_Cmd(enum.Enum):
    IO_JUSTREAD = enum.auto()
    IO_QUIT = enum.auto()
    IO_SET = enum.auto()


def thread_ioworker(qin, qout):
    message_counter=0
    while True:
        item = qin.get()
        print('io thread: got task from queue')
        if item.cmd==IO_Cmd.IO_QUIT:
            print('io thread: got QUIT cmd ==> leaving')
            break
        tstart = time.time()
        # do work
        if item.cmd==IO_Cmd.IO_SET:
            print('io thread: got set command (currently not implemented)')

        r = SimpleNamespace()
        r.tag = message_counter
        r.timestamp = time.time() # timestamp to recognise 'old' msgs
        r.color1_rb = 123
        r.color2_rb = 234
        r.color3_rb = 456
        x = pydoocs.read('XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/MOTEMP')
        r.mono2_pitch = x['data']
        tend = time.time()
        print('io thread: finishing item, processing time: {}'.format(tend-tstart))
        qin.task_done()
        qout.put(r)
        message_counter+=1

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        # self.close.connect(self.on_close)
        self.display_map_button.clicked.connect(self.on_show_map_button)
        self.apply_button.clicked.connect(self.on_apply_button)

        # queue for communication to machine
        self.q_to_io = queue.Queue(maxsize=1000)
        self.q_from_io = queue.Queue(maxsize=1000)
        # start machine communication thread
        threading.Thread(target=thread_ioworker, args=(self.q_to_io,self.q_from_io), daemon=True).start()
        # setup Qt timer for machine IO (for updating current status)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.timeout)
        self.update_timer.start(1000)


    # Data was received from IO thread
    # ==> update displayed readback values
    def update_readbacks(self, msg):
        self.color1_rb_display.setText(str(msg.color1_rb))
        self.color2_rb_display.setText(str(msg.color2_rb))
        self.color3_rb_display.setText(str(msg.color3_rb))
        self.color1_rb_display.setText(str(msg.tag))
        self.mono2_pitch_display.setText(str(msg.mono2_pitch))

    def timeout(self):
        # send to IO thread
        cmd = SimpleNamespace()
        cmd.cmd = IO_Cmd.IO_JUSTREAD
        self.q_to_io.put(cmd)

        got_something=False
        try:
            # there may be multiple objects waiting in the queue.
            # queue get operation will drop exception if queue is empty.
            while True:
                msg = deepcopy( self.q_from_io.get(block=False) )
                self.q_from_io.task_done() # to be sure, data was copied (TODO: determine if needed)
                msg_age = time.time()-msg.timestamp
                got_something=True
                print('got event ID={}, age={}s'.format(msg.tag, msg_age))
                self.update_readbacks(msg)
        except queue.Empty:
            if got_something==False:
                print('there was nothing in queue')

    def on_show_map_button(self):
        x = self.photon_energy_edit.text()
        print('value='+x)
        blah = do_crystal_plot.ApplicationWindow(lpcb=self.on_crystal_map_linepicked)
        blah.show()
        blah.activateWindow()
        self.crystal_plot = blah # prevent issues with garbage collector (2021-Oct-15). On Ubuntu 20.04LTS plot was showing, on MacOS in BKR, the plot was not displayed, but there was also no crash or error msg displayed. Pointed out by Marc G.
        print('abc')

    def on_crystal_map_linepicked(self,the_info):
        print('### CRYSTAL MAP CALLBACK ###')
        print(str(the_info))
        if the_info.valid:
            self.reflection_display.setText(the_info.info_txt)
            self.photon_energy_edit.setText('{:.2f}'.format(the_info.y))


    def on_apply_button(self):
        cmd = SimpleNamespace()
        cmd.cmd = IO_Cmd.IO_SET
        self.q_to_io.put(cmd)

    def on_close(self):
        print('CLOSE')

app = qtw.QApplication([])

w = MainWindow()
w.show()

app.exec_()
