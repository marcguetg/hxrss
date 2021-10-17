#!/usr/bin/env python3

# put the HXRSS tool box on the path, so that the Python modules can be imported
import os
import sys
script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)
hxrss_toolbox_dir = script_dir+'/Crystal pitch angle model'
sys.path.append(hxrss_toolbox_dir)

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

# for development of crystal control code
from scipy import interpolate
import scipy
import numpy as np
from HXRSS_Bragg_max_generator import HXRSS_Bragg_max_generator

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        # self.close.connect(self.on_close)
        self.display_map_button.clicked.connect(self.on_show_map_button)
        self.apply_button.clicked.connect(self.on_apply_button)
        self.photon_energy_edit.returnPressed.connect(self.on_photon_energy_enter)

        self.photon_energy_edit.setText('{:.2f}'.format(get_initial_photon_energy_value()))

        self.mono2 = SimpleNamespace()
        self.mono2.infotxt = 'Crystal 2'
        self.mono2.pitch_min = 29.88  # [deg], min/max values from mono control panel
        self.mono2.pitch_max = 120.06
        self.mono2.pitch_minmax_safetymargin = 1 # don't go to the limits

        ### THREAD FOR MACHINE I/O ###
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

################################
### CRYSTAL-MAP RELATED CODE ###
################################
    def on_show_map_button(self):
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

            ### store detailed curve data for interpolation of setpoints ###
            hmax, kmax, lmax = 1,1,1 # has no effect because specific_hkl parameters overrides these
            # imperfections of the system (from Channel_list.md document, as of 14.10.2021)
            dthp = -0.392      # pitch angle
            dthy = 1.17        # roll angle (American convention)
            dthr = 0.1675      # yaw angle (American convention)
            alpha = 0.00238    # alpha parameter: for different pitch angles, different rolls are needed to bring the lines together

            roll_list = [1.58]
            stt_thplist = np.linspace(45, 115, 1001) # test data: cyan curve within pitch travel range
            stt_r = HXRSS_Bragg_max_generator(
                stt_thplist, hmax, kmax, lmax, dthp, dthy, roll_list, dthr, alpha,
                specific_hkl=[(1,1,1)], return_obj=True) # <===
            stt_phen_list = stt_r.phen_list
            stt_pangle_list = stt_r.p_angle_list
            stt_rangle_list = stt_r.r_angle_list # FIXME: implementation still not finalized since unclear what offset is needed for these values
            stt_gid_list = stt_r.gid_list
            print(str(stt_r.r_angle_list))

            # !!! there is an angle offset between input pitch angles and
            #     angles returned as second return argument !!!
            # for current test params, the offset is 0.392 deg.
            # function returns list containing lists, but they should only have single element
            stt_phen_list = stt_phen_list[0]
            stt_pangle_list = stt_pangle_list[0]
            stt_rangle_list = stt_rangle_list[0]

            # dbg: pitch angle offset between input array and output array
            # print(str(stt_pangle_list[0]))
            # print(str(stt_thplist[0]))

            self.mono2.curvedata = SimpleNamespace()
            self.mono2.curvedata.pitch = stt_pangle_list
            self.mono2.curvedata.roll = stt_rangle_list
            self.mono2.curvedata.phen = stt_phen_list
            self.mono2.curvedata.valid = True

################################

    def determine_setpoints(self,sp_phen):
        self.determine_mono_setpoints(self.mono2,sp_phen)

    def determine_mono_setpoints(self,mono,sp_phen):
        if not hasattr(mono,'curvedata'):
            print(mono.infotxt+': no curvedata available')
            return False
        cd = mono.curvedata
        if cd.valid!=True:
            print(mono.infotxt+': curvedata is not valid')
            return False

        # verify that the desired photon energy is possible
        phen_max = np.amax(np.array(cd.phen))
        phen_min = np.amin(np.array(cd.phen))
        if ((phen_min<=sp_phen) and (sp_phen<=phen_max)):
            pass # ok
        else:
            print(mono.infotxt+f': requested photon energy is outside of possible range {phen_min}..{phen_max}')
            return False

        # setup INTERPOLATION of stored crystal curve
        # Curve continues with extrapolation outside known pitch range
        # This is needed to force the search algorithm back into the known region
        # In the end, it is verified that the search converged to a value inside
        # the interpolation region.
        # The curve is assumed to be monotonic because it is from a photon energy
        # minimum to a maximum or vice versa.
        #f_interp_phen = interpolate.interp1d(cd.pitch, cd.phen,
        #    fill_value=(cd.phen[0],cd.phen[-1]), bounds_error=False)
        f_interp_phen = interpolate.interp1d(cd.pitch, cd.phen,
            fill_value='extrapolate', bounds_error=False)

        # find the pitch angle corresponding to the desired photon energy
        f = lambda pitch: (f_interp_phen(pitch)-sp_phen)
        # f = lambda pitch: (f_interp_phen(pitch)-sp_phen)
        pitch0 = (cd.pitch[0]+cd.pitch[-1])/2 # start value in the center of range
        solroot = scipy.optimize.root(f, [pitch0]) # root finding does not support specification of bounds
        if not solroot.success:
            print(mono.infotxt+': issue with finding the pitch angle, scipy.optimize.root status:')
            print(str(solroot))
            return False


        setpoint_pitch = solroot.x[0]

        # Check that the determined setpoint is within the travel range of the actuator
        # Don't use the full travel range (note that 'abs' was used to guard against
        # negative safety margin values)
        setpoint_pitch_inrange = (mono.pitch_min+abs(mono.pitch_minmax_safetymargin <= setpoint_pitch)) and (setpoint_pitch <= mono.pitch_max-abs(mono.pitch_minmax_safetymargin))
        if setpoint_pitch_inrange==False:
            print(mono.infotxt+f': determined pitch setpoint {setpoint_pitch} not in allowed travel range (min={mono.pitch_min}, max={mono.pitch_max}, safety_margin={mono.pitch_minmax_safetymargin}')
            return False

        # TODO: check that determined setpoint is from interpolation (= point lies in the scanned pitch range)


        # determine roll setpoint
        f_interp_roll = interpolate.interp1d(cd.pitch, cd.roll)
        setpoint_roll = f_interp_roll(setpoint_pitch)
        setpoint_roll *= 180/np.pi # rad=>deg
        # NOTE: currently not using this setpoint as additional considerations are needed

        print(mono.infotxt+f': setpoint pitch={setpoint_pitch}, roll={setpoint_roll}')
        return True

    def on_photon_energy_enter(self):
        print('photon energy edit: [enter] detected')
        phen_str = self.photon_energy_edit.text()
        # convert string to number, continue only if this works
        try:
            phen = float(phen_str)
        except ValueError:
            print(f'photon energy cannot convert "{phen_str}" into number')
            return
        self.determine_setpoints(phen)

    def on_apply_button(self):
        cmd = SimpleNamespace()
        cmd.cmd = IO_Cmd.IO_SET
        cmd.setpoints = SimpleNamespace()
        cmd.setpoints.mono2_pitch = 1
        cmd.setpoints.mono2_roll  = 1.5
        self.q_to_io.put(cmd)

    def on_close(self):
        print('CLOSE')



if __name__ == "__main__":
    app = qtw.QApplication([])

    w = MainWindow()
    w.show()

    app.exec_()
