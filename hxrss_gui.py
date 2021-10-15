#!/usr/bin/env python3

from hxrss_main_window import Ui_MainWindow
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import QTimer

import threading,queue
import time
from types import SimpleNamespace
from copy import deepcopy

from hxrss_io import thread_ioworker, IO_Cmd, get_initial_photon_energy_value

# from clscratch import stuff2000
import do_crystal_plot

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        # self.close.connect(self.on_close)
        self.display_map_button.clicked.connect(self.on_show_map_button)
        self.apply_button.clicked.connect(self.on_apply_button)

        self.photon_energy_edit.setText('{:.2f}'.format(get_initial_photon_energy_value()))

        # thread for communication with machine: display dbg messages?
        self.io_thread_dbg=False
        # queue for communication to machine
        self.q_to_io = queue.Queue(maxsize=1000)
        self.q_from_io = queue.Queue(maxsize=1000)
        # start machine communication thread (specify daemon=True when the thread should automatically be terminated)
        # threading.Thread(target=thread_ioworker, args=(self.q_to_io,self.q_from_io), daemon=True).start()
        threading.Thread(target=thread_ioworker, args=(self.q_to_io,self.q_from_io,self.io_thread_dbg)).start()
        # setup Qt timer for machine IO (for updating current status)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.timeout)
        self.update_timer.start(1000)


    def closeEvent(self, event):
        print('got close event, stopping IO thread')

        # send to IO thread
        cmd = SimpleNamespace()
        cmd.cmd = IO_Cmd.IO_QUIT
        self.q_to_io.put(cmd)

        event.accept()
        # to ignore this event: event.ignore()


    # Data was received from IO thread
    # ==> update displayed readback values
    def update_readbacks(self, msg):
        self.color1_rb_display.setText(str(msg.color1_rb))
        self.color2_rb_display.setText(str(msg.color2_rb))
        self.color3_rb_display.setText(str(msg.color3_rb))
        self.mono1_pitch_rb_display.setText(str(msg.mono1_pitch_rb))
        self.mono1_pitch_sp_display.setText(str(msg.mono1_pitch_sp))
        self.mono1_roll_rb_display.setText(str(msg.mono1_roll_rb))
        self.mono1_roll_sp_display.setText(str(msg.mono1_roll_sp))
        self.mono2_pitch_rb_display.setText(str(msg.mono2_pitch_rb))
        self.mono2_pitch_sp_display.setText(str(msg.mono2_pitch_sp))
        self.mono2_roll_rb_display.setText(str(msg.mono2_roll_rb))
        self.mono2_roll_sp_display.setText(str(msg.mono2_roll_sp))
        self.io_msgtag_display.setText(str(msg.tag))
        self.io_processingtime_display.setText('{:.2f}'.format(1e3*msg.processing_time))
        self.io_msgage_display.setText('{:.2f}'.format(msg.age))

    def timeout(self):
        self.io_thread_dbg = self.io_threaddbg_checkbox.checkState()
        dbg = self.io_thread_dbg

        # send to IO thread
        cmd = SimpleNamespace()
        cmd.cmd = IO_Cmd.IO_JUSTREAD
        cmd.io_dbg = dbg
        self.q_to_io.put(cmd)

        got_something=False
        try:
            # there may be multiple objects waiting in the queue.
            # queue get operation will drop exception if queue is empty.
            while True:
                msg = deepcopy( self.q_from_io.get(block=False) )
                self.q_from_io.task_done() # to be sure, data was copied (TODO: determine if needed)
                msg.age = time.time()-msg.timestamp
                got_something=True
                if dbg: print('GUI timer: got event ID={}, age={}s'.format(msg.tag, msg.age))
                self.update_readbacks(msg)
        except queue.Empty:
            if got_something==False:
                if dbg: print('GUI timer: there was nothing in queue')

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
        cmd.setpoints = SimpleNamespace()
        cmd.setpoints.mono2_pitch = 1
        cmd.setpoints.mono2_roll  = 1.5
        self.q_to_io.put(cmd)

    def on_close(self):
        print('CLOSE')

app = qtw.QApplication([])

w = MainWindow()
w.show()

app.exec_()
