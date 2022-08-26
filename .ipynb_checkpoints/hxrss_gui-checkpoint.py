#!/usr/bin/env python3
# put the HXRSS tool box on the path, so that the Python modules can be imported
import os
import sys
import csv
import pandas as pd
script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)
hxrss_toolbox_dir = script_dir+'/Crystal pitch angle model'
sys.path.append(hxrss_toolbox_dir)


from hxrss_main_window import Ui_MainWindow
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import QTimer, QAbstractTableModel, Qt
from PyQt5 import QtGui

import threading,queue
import time
from types import SimpleNamespace
from copy import deepcopy

from hxrss_io import thread_read_worker, rt_request_update, rt_get_msg, thread_write_worker, get_initial_photon_energy_value, IO_Cmd
from hxrss_io_crystal_params import hxrss_io_crystal_parameters_default, hxrss_io_crystal_parameters_fromDOOCS

import do_crystal_plot

# for development of crystal control code
from scipy import interpolate
import scipy
import numpy as np
from HXRSS_Bragg_max_generator import HXRSS_Bragg_max_generator
import re

from spectr_gui import send_to_desy_elog
from data.update_table import update_table
from datetime import datetime




# for development of crystal control code

class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.display_map_button.clicked.connect(self.on_show_map_button)
        self.apply_button.clicked.connect(self.on_apply_button)
        self.photon_energy_edit.returnPressed.connect(
            self.on_photon_energy_enter)
        self.photonE.returnPressed.connect(self.on_calc_photon_energy_enter)
        self.roll_angle_edit.returnPressed.connect(
            self.on_calc_roll_angle_enter)
        self.mono2_crystal_insert_button.clicked.connect(
            self.on_mono2_crystal_insert_button)
        self.mono2_crystal_park_button.clicked.connect(
            self.on_mono2_crystal_park_button)
        #
        self.params_report_button.clicked.connect(self.on_params_report_button)
        self.params_fromDOOCS_button.clicked.connect(
            self.on_params_fromDOOCS_button)
        self.params_default_button.clicked.connect(
            self.on_params_default_button)
        self.tableButton.clicked.connect(self.on_table_clear_click)
        self.update_table_button.clicked.connect(self.on_update_table_button)

        # set initial photon energy value (currently SASE2 color1 setpoint)
        self.photon_energy_edit.setText(
            '{:.2f}'.format(get_initial_photon_energy_value()))
        self.apply_button.setEnabled(False)
        self.display_map_button.setEnabled(False)
        self.tableButton.setEnabled(False)
        self.scan_checkBox.setEnabled(False)
        # hide HXRSS crystal reflection curve information (it will become visible once needed)
        #self.photon_energy_min_label.setVisible(False)
        #self.photon_energy_min_display.setVisible(False)
        #self.photon_energy_max_label.setVisible(False)
        #self.photon_energy_max_display.setVisible(False)
        self.label_2.setVisible(False)
        self.reflection_display.setVisible(False)
        self.label_22.setVisible(False)
        self.undulatorph.setVisible(False)
        self.label_28.setVisible(False)
        self.temp.setVisible(False)
        self.label_23.setVisible(False)
        self.label_25.setVisible(False)
        self.loglabel.setText('Insert the desired Photon Energy value')
        self.model = QtGui.QStandardItemModel(self)
        self.logbookstring = []

        # TableView
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(1)
        self.tableView.clicked.connect(self.viewClicked)
        self.tableView.setSelectionBehavior(qtw.QTableView.SelectRows)
        self.tableView.doubleClicked.connect(self.on_row_double_click)
        self.filename = script_dir+'/data/machine_status.csv'

        self.mono2 = SimpleNamespace()
        self.mono2.infotxt = 'Crystal 2'
        self.mono2.setpoint = SimpleNamespace()
        self.mono2.valid = False
        self.mono2.setpoint.pitch = 100
        print('assuming roll=1.58')
        self.mono2.setpoint.roll = 1.58
        self.roll_angle_edit.setText('{:.3f}'.format(self.mono2.setpoint.roll))
        # [deg], min/max values from mono control panel
        self.mono2.pitch_min = 29.88
        self.mono2.pitch_max = 120.06
        self.mono2.pitch_minmax_safetymargin = 1  # don't go to the limits
        self.line = None
        self.pitchconfig = None
        self.rollconfig = None
        # Obtain default correction parameters for mono2
        # These describe imperfections of the system
        self.mono2.corrparams = hxrss_io_crystal_parameters_default()
        self.mono1_roll_rb_display.setAlignment(Qt.AlignCenter)
        self.mono2_roll_rb_display.setAlignment(Qt.AlignCenter)
        self.mono1_pitch_rb_display.setAlignment(Qt.AlignCenter)
        self.mono2_pitch_rb_display.setAlignment(Qt.AlignCenter)
        self.mono1_motemp_rb_display.setAlignment(Qt.AlignCenter)
        self.mono2_motemp_rb_display.setAlignment(Qt.AlignCenter)
        self.mono1_crystal_inserted_display.setAlignment(Qt.AlignCenter)
        self.mono2_crystal_inserted_display.setAlignment(Qt.AlignCenter)

        self.scan_checkBox.stateChanged.connect(self.state_changed)

        ### THREAD FOR MACHINE I/O ###
        # thread for communication with machine: display dbg messages?
        self.io_thread_dbg = False
        # queue for communication to machine
        self.q_to_read = queue.Queue(maxsize=1000)
        self.q_from_read = queue.Queue(maxsize=1000)
        self.q_to_write = queue.Queue(maxsize=1000)
        self.q_from_write = queue.Queue(maxsize=1000)
        # start machine communication threads (specify daemon=True when the thread should automatically be terminated -> we don't do that)
        threading.Thread(target=thread_read_worker, args=(
            self.q_to_read, self.q_from_read, self.io_thread_dbg), name='read thread').start()
        threading.Thread(target=thread_write_worker, args=(
            self.q_to_write, self.q_from_write, self.io_thread_dbg), name='write thread').start()
        # setup Qt timer for machine IO (for updating current status)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.timeout)
        self.update_timer.start(1000)

    def closeEvent(self, event):
        # send IO threads command to stop
        print('got close event, stopping IO thread')
        cmd = SimpleNamespace()
        cmd.cmd = IO_Cmd.IO_QUIT
        self.q_to_read.put(cmd)
        self.q_to_write.put(cmd)

        # close crystal plot window (otherwise closing main window will not terminate application when crystal plot window is still open)
        if hasattr(self, 'crystal_plot'):
            self.crystal_plot.close()

        event.accept()
        # to ignore this event: event.ignore()

    # Data was received from IO thread
    # ==> update displayed readback values

    def update_readbacks(self, msg):
        def str_ph_energy(q_):
            return f'{q_:.1f}'

        def str_pitch_angle(q_):
            return f'{q_:.3f}'

        def str_roll_angle(q_):
            return f'{q_:.4f}'

        def update_busy_indicator(qlabel, is_busy=False):
            if is_busy:
                # qlabel.setStyleSheet('background-color:red') # reserved for future error indication, only red border for busy
                qlabel.setStyleSheet('border: 2px solid red')
            else:
                qlabel.setStyleSheet('')

        self.color1_rb_display.setText(str_ph_energy(msg.color1_rb))
        self.color2_rb_display.setText(str_ph_energy(msg.color2_rb))
        self.color3_rb_display.setText(str_ph_energy(msg.color3_rb))
        self.mono1_pitch_rb_display.setText(
            str_pitch_angle(msg.mono1_pitch_rb))
        update_busy_indicator(self.mono1_pitch_rb_display,
                              msg.mono1_pitch_busy)
        self.mono1_pitch_sp_display.setText(
            str_pitch_angle(msg.mono1_pitch_sp))
        self.mono1_roll_rb_display.setText(str_roll_angle(msg.mono1_roll_rb))
        update_busy_indicator(self.mono1_roll_rb_display, msg.mono1_roll_busy)
        self.mono1_roll_sp_display.setText(str_roll_angle(msg.mono1_roll_sp))
        self.mono2_pitch_rb_display.setText(
            str_pitch_angle(msg.mono2_pitch_rb))
        update_busy_indicator(self.mono2_pitch_rb_display,
                              msg.mono2_pitch_busy)
        self.mono2_pitch_sp_display.setText(
            str_pitch_angle(msg.mono2_pitch_sp))
        self.mono2_roll_rb_display.setText(str_roll_angle(msg.mono2_roll_rb))
        update_busy_indicator(self.mono2_roll_rb_display, msg.mono2_roll_busy)
        self.mono2_roll_sp_display.setText(str_roll_angle(msg.mono2_roll_sp))
        self.mono1_motemp_rb_display.setText(str_ph_energy(msg.mono1_motemp_rb))
        self.mono2_motemp_rb_display.setText(str_ph_energy(msg.mono2_motemp_rb))
        self.undulatorph.setValue(msg.global_color_rb)
        #self.undulatorph.setValue(msg.mono1_pitch_rb)
        str_mono1_crystal_status = 'parked'
        str_mono2_crystal_status = 'parked'
        self.mono1_crystal_park_button.setEnabled(False)
        self.mono2_crystal_park_button.setEnabled(False)
        if msg.mono1_is_inserted:
            self.mono1_crystal_insert_button.setEnabled(False)
            self.mono1_crystal_park_button.setEnabled(True)
            if msg.mono1_insert_busy == False:
                str_mono1_crystal_status = 'inserted'
                self.mono1_crystal_insert_button.setEnabled(False)
                self.mono1_crystal_park_button.setEnabled(True)
            else:
                str_mono1_crystal_status = 'inserting...'
                update_busy_indicator(
                    self.mono1_crystal_inserted_display, msg.mono1_insert_busy)
                self.mono1_crystal_insert_button.setEnabled(False)
                self.mono1_crystal_park_button.setEnabled(False)
        if msg.mono2_is_inserted:
            self.mono2_crystal_insert_button.setEnabled(False)
            self.mono2_crystal_park_button.setEnabled(True)
            if msg.mono2_insert_busy == False:
                str_mono2_crystal_status = 'inserted'
                self.mono2_crystal_insert_button.setEnabled(False)
                self.mono2_crystal_park_button.setEnabled(True)
            else:
                str_mono2_crystal_status = 'inserting...'
                update_busy_indicator(
                    self.mono2_crystal_inserted_display, msg.mono2_insert_busy)
                self.mono2_crystal_insert_button.setEnabled(False)
                self.mono2_crystal_park_button.setEnabled(False)
        if msg.mono1_is_inserted == False and msg.mono1_insert_busy == True:
            update_busy_indicator(
                self.mono1_crystal_inserted_display, msg.mono1_insert_busy)
            str_mono1_crystal_status = 'moving...'
            self.mono1_crystal_insert_button.setEnabled(False)
            self.mono1_crystal_park_button.setEnabled(False)
        if msg.mono2_is_inserted == False and msg.mono2_insert_busy == True:
            update_busy_indicator(
                self.mono2_crystal_inserted_display, msg.mono2_insert_busy)
            str_mono2_crystal_status = 'moving...'
            self.mono2_crystal_insert_button.setEnabled(False)
            self.mono2_crystal_park_button.setEnabled(False)
        self.mono1_crystal_inserted_display.setText(str_mono1_crystal_status)
        self.mono2_crystal_inserted_display.setText(str_mono2_crystal_status)
        self.io_msgtag_display.setText(str(msg.tag))
        self.io_processingtime_display.setText(
            '{:.2f}'.format(1e3*msg.processing_time))
        self.io_msgage_display.setText('{:.2f}'.format(msg.age))

    def timeout(self):
        self.io_thread_dbg = self.io_threaddbg_checkbox.checkState()
        dbg = self.io_thread_dbg
        rt_request_update(self.q_to_read, dbg)
        got_something = False
        try:
            # there may be multiple objects waiting in the queue.
            # queue get operation will drop exception if queue is empty.
            while True:
                msg = rt_get_msg(self.q_from_read, block=False)
                msg.age = time.time()-msg.timestamp
                got_something = True
                if dbg:
                    print('GUI timer: got event ID={}, age={}s'.format(
                        msg.tag, msg.age))
                self.update_readbacks(msg)
        except queue.Empty:
            if got_something == False:
                if dbg:
                    print('GUI timer: there was nothing in queue')

################################
### CRYSTAL-MAP RELATED CODE ###
################################
    def on_show_map_button(self):
        roi = SimpleNamespace()
    # imperfections of the system (from Channel_list.md document, as of 14.10.2021)
        roi.minE = self.phen-1500
        roi.maxE = self.phen+1500   # roll angle (American convention)
        roi.phen = self.phen
        if self.pitchconfig == None:
            roi.minpitch = 30
            roi.maxpitch = 120
        else:
            roi.minpitch = self.pitchconfig-2
            roi.maxpitch = self.pitchconfig+2
        if self.rollconfig == None:
            roi.roll = self.mono2.corrparams.roll_list
        else:
            roi.roll = [self.rollconfig]
        blah = do_crystal_plot.ApplicationWindow(
            lpcb=self.on_crystal_map_linepicked, corrparams=self.mono2.corrparams, roi=roi)
        blah.show()
        blah.activateWindow()
        # prevent issues with garbage collector (2021-Oct-15). On Ubuntu 20.04LTS plot was showing, on MacOS in BKR, the plot was not displayed, but there was also no crash or error msg displayed. Pointed out by Marc G.
        self.crystal_plot = blah

    def on_crystal_map_linepicked(self, the_info):
        print('### CRYSTAL MAP CALLBACK ###')
        print(str(the_info))
        if the_info.valid:
            self.apply_button.setEnabled(True)
            self.label_2.setVisible(True)
            self.label_23.setVisible(True)
            self.label_25.setVisible(True)
            self.reflection_display.setVisible(True)
            self.reflection_display.setText(the_info.info_txt)
            self.reflection_chosen = the_info.info_txt
            self.photonE.setText('{:.2f}'.format(the_info.y))
            self.roll_angle_edit.setText('{:.3f}'.format(the_info.roll))
            #self.loglabel.setText('You have selected reflection '+ the_info.info_txt+'. Adjust the Photon energy and click Enter to calculate the crystal configuration.')

            mono = self.mono2
            # Check that the click is within the travel range of the actuator
            # Don't use the full travel range (note that 'abs' was used to guard against
            # negative safety margin values)
            click_inrange = (mono.pitch_min+abs(mono.pitch_minmax_safetymargin) <= the_info.x) and (
                the_info.x <= mono.pitch_max-abs(mono.pitch_minmax_safetymargin))
            if not click_inrange:
                print('ERROR: you need to click within the pitch angle range: '
                      + str(mono.pitch_min
                            + abs(mono.pitch_minmax_safetymargin)) + ' and '
                      + str(mono.pitch_max-abs(mono.pitch_minmax_safetymargin))
                      + ' (safety margin {})'.format(abs(mono.pitch_minmax_safetymargin)))
                return

            # from string "[h,k,l]", extract the numerical values
            # FIXME: improve this error prone conversion to string (in the plot code) and conversion back to needed object. Instead, get (h,k,l) as Python object not as string from plot window.
            matchresult = re.match(
                r'\[\s*(-?[0-9]+)\s*,\s*(-?[0-9]+)\s*,\s*(-?[0-9]+)\s*\]', the_info.info_txt)
            if matchresult is not None:
                hkl = (int(matchresult[1]), int(
                    matchresult[2]), int(matchresult[3]))
            else:
                # could not match the string
                print('Warning: could not extract crystal orientation from '
                      + the_info.info_txt+', using hkl=(1,1,1)')
                hkl = (1, 1, 1)

            # Obtain correction parameters for mono2
            # These describe imperfections of the system
            # Program starts with default values but can also load updates values from DOOCS
            dthp = mono.corrparams.dthp   # pitch angle
            dthy = mono.corrparams.dthy   # roll angle (American convention)
            dthr = mono.corrparams.dthr   # yaw angle (American convention)
            # alpha parameter: for different pitch angles, different rolls are needed to bring the lines together
            alpha = mono.corrparams.alpha
            #roll_list = mono.corrparams.roll_list

            ################################################################
            ### store detailed curve data for interpolation of setpoints ###
            ################################################################
            # has no effect because specific_hkl parameters overrides these
            hmax, kmax, lmax = 1, 1, 1
            ### Step 1: determine pitch angle scan range ###
            # stt = "single trace test"
            maxE = self.phen+1000
            minE = self.phen-1000
            if self.rollconfig != None:
                roll_list = [self.rollconfig]
            else:
                roll_list = mono.corrparams.roll_list
            # values are not really relevant, as we need to determine the pitch scan range first
            stt_thplist = np.linspace(45, 115, 1001)
            stt_r = HXRSS_Bragg_max_generator(
                stt_thplist, hmax, kmax, lmax, dthp, dthy, roll_list, dthr, alpha, maxE, minE,
                specific_hkl=[hkl],  # <====
                return_obj=True, analyze_curves_complete=True)

            # Remember that HXRSS_Bragg_max_generator returns lists containing lists,
            # as it is designed to handle multiple curve traces simultaneously
            workspace_range_analysis = deepcopy(stt_r.analysis_result_list[0])
            print('*** STEP 1: result of analysis procedure ***')
            print(str(workspace_range_analysis))
            print('*** STEP 2: add travel min/max and click pos ***')
            workspace_range_analysis.append((mono.pitch_min, -1, 'travel_min'))
            workspace_range_analysis.append((mono.pitch_max, -1, 'travel_max'))
            key_click = 'click_pos'
            workspace_range_analysis.append((the_info.x, -1, key_click))
            print(str(workspace_range_analysis))

            def my_cmp(x_, y_):
                # print('compare '+str(x_)+' and '+str(y_))
                return(x_[0]-y_[0])  # first element: pitch angle

            import functools
            workspace_range_analysis = sorted(workspace_range_analysis,
                                              key=functools.cmp_to_key(my_cmp))  # docu: https://docs.python.org/3/library/functools.html#functools.cmp_to_key
            print('*** STEP 3: sort pitch angles in ascending order ***')
            print(str(workspace_range_analysis))
            print('*** DONE ***')

            # Let's assume that there are no curve features (pole,minimum),
            # still the clicked point (if between travel_min and travel_max)
            # will have two neighboring element in the sorted data. If this
            # is not the case, then the click was outside of the valid travel
            # range.
            idx_click_valid = False
            for idx_click, qqq in enumerate(workspace_range_analysis):
                if qqq[2] == key_click:
                    idx_click_valid = True
                    break

            if (idx_click == 0) or (idx_click == len(workspace_range_analysis)-1) or (idx_click_valid == False):
                print('ERROR: click outside of motor travel range?')
                return

            print('idx_click-1: '+str(workspace_range_analysis[idx_click-1]))
            print('idx_click:   '+str(workspace_range_analysis[idx_click]))
            print('idx_click+1: '+str(workspace_range_analysis[idx_click+1]))
            idx_scanrange_min = idx_click-1
            idx_scanrange_max = idx_click+1

            pole_stay_away = 0.1  # pitch angle [degrees]
            scanrange_min = workspace_range_analysis[idx_scanrange_min][0]
            if workspace_range_analysis[idx_scanrange_min][2] == 'pole':
                scanrange_min += pole_stay_away
            scanrange_max = workspace_range_analysis[idx_scanrange_max][0]
            if workspace_range_analysis[idx_scanrange_max][2] == 'pole':
                scanrange_max -= pole_stay_away

            # FIXME: workaround for the fact that the pitch scan range specified to HXRSS_Bragg_max_generator
            workaround = 0.5
            print('WORKAROUND: reduce determined range by {workaround}')
            scanrange_min += workaround
            scanrange_max -= workaround
            if scanrange_min > scanrange_max:
                print('ERROR: scan range is too small. Pick different line.')
                return

            print(
                f'*** DONE: going to load pitch angle scan range {scanrange_min} -- {scanrange_max} degrees ***')

            ##############################################
            ### OBTAINING CURVE DATA FOR INTERPOLATION ###
            ##############################################
            # stt = "single trace test"
            # values are not really relevant, as we need to determine the pitch scan range first
            stt_thplist = np.linspace(scanrange_min, scanrange_max, 1001)
            stt_r = HXRSS_Bragg_max_generator(
                stt_thplist, hmax, kmax, lmax, dthp, dthy, roll_list, dthr, alpha, maxE, minE,
                specific_hkl=[hkl],  # <====
                return_obj=True)

            stt_phen_list = stt_r.phen_list
            stt_pangle_list = stt_r.p_angle_list
            # FIXME: implementation still not finalized since unclear what offset is needed for these values
            stt_rangle_list = stt_r.r_angle_list
            stt_gid_list = stt_r.gid_list

            # !!! there is an angle offset between input pitch angles and
            #     angles returned as second return argument !!!
            # for current test params, the offset is 0.392 deg.
            # function returns list containing lists, but they should only have single element
            stt_phen_list = stt_phen_list[0]
            stt_pangle_list = stt_pangle_list[0]
            stt_rangle_list = stt_rangle_list[0]

            # indicate the data points
            indicate_loaded_data = True
            if indicate_loaded_data:
                # need to specify 'gid', since the hover function expects it (otherwise there's a crash in the hover event handling function)
                if self.line:
                    self.line.remove()
                self.line, = the_info.ax.plot(stt_pangle_list, np.array(
                    stt_phen_list), 'r+', gid=the_info.info_txt)
                parent_fig = the_info.ax.get_figure()
                parent_fig.canvas.draw()

            def str_minmax(l: list):
                q = np.array(l)
                s = 'min={:f} max={:f}'.format(np.amin(q), np.amax(q))
                return s

            print('Information on curve data obtained for hkl='+str(hkl))
            print('  pitch angle   '+str_minmax(stt_pangle_list))
            print('  roll angle    '+str_minmax(stt_rangle_list))
            print('  photon energy '+str_minmax(stt_phen_list))
            #display_phen_max=False
            #self.photon_energy_min_display.setText(str(np.amin(np.array(stt_phen_list))))
            #self.photon_energy_min_label.setVisible(False)
            #self.photon_energy_min_display.setVisible(False)
            #if display_phen_max:
            #    self.photon_energy_max_display.setText(str(np.amax(np.array(stt_phen_list))))
            ##    self.photon_energy_max_label.setVisible(False)
            #    self.photon_energy_max_display.setVisible(False)
            self.calclabel.setText('Insert an energy value between ' + str(np.round(np.amin(np.array(stt_phen_list)), 1))
                                   + ' eV and '+str(np.round(np.amax(np.array(stt_phen_list)), 1))+' eV. Press Enter to calculate setpoint.')

            # dbg: pitch angle offset between input array and output array
            # print(str(stt_pangle_list[0]))
            # print(str(stt_thplist[0]))

            self.mono2.curvedata = SimpleNamespace()
            self.mono2.curvedata.pitch = stt_pangle_list
            self.mono2.curvedata.roll = stt_rangle_list
            self.mono2.curvedata.phen = stt_phen_list
            self.mono2.curvedata.valid = True

################################

    def determine_setpoints(self, sp_phen):
        self.determine_mono_setpoints(self.mono2, sp_phen)

    def determine_mono_setpoints(self, mono, sp_phen):
        if not hasattr(mono, 'curvedata'):
            print(mono.infotxt+': no curvedata available, select curve from map')
            return False
        cd = mono.curvedata
        if cd.valid != True:
            print(mono.infotxt+': curvedata is not valid')
            return False

        print(mono.infotxt
              + f': computing setpoint for requested photon energy {sp_phen} and roll angle {self.rollconfig}')

        # some information about crystal curve data used for interpolation
        phen_max = np.amax(np.array(cd.phen))
        phen_min = np.amin(np.array(cd.phen))
        pitch_max = np.amax(np.array(cd.pitch))
        pitch_min = np.amin(np.array(cd.pitch))

        # verify that the desired photon energy is possible
        if self.scan_checkBox.isChecked() == 1:
            if ((phen_min <= sp_phen) and (sp_phen <= phen_max)):
                self.calclabel.setText('Possible photon energy range: ' + str(
                    np.round(phen_min, 1)) + ' eV to '+str(np.round(phen_max, 1))+' eV.')
                self.scanlabel.setText('Calculating setpoint.')
                pass  # ok
            else:
                print(
                    mono.infotxt+f': requested photon energy is outside of possible range {phen_min}..{phen_max}')
                self.scanlabel.setText('Requested photon energy is outside of possible range ' + str(
                    np.round(phen_min, 1)) + ' eV and '+str(np.round(phen_max, 1))+' eV. Stopping scan')
                self.scan_checkBox.setChecked(False)
                return False
        else:
            if ((phen_min <= sp_phen) and (sp_phen <= phen_max)):
                self.calclabel.setText('Insert an energy value between ' + str(np.round(phen_min, 1))
                                       + ' eV and '+str(np.round(phen_max, 1))+' eV. Press Enter to calculate setpoint.')
                pass  # ok
            else:
                print(
                    mono.infotxt+f': requested photon energy is outside of possible range {phen_min}..{phen_max}')
                self.calclabel.setText('Requested photon energy is outside of possible range ' + str(
                    np.round(phen_min, 1)) + ' eV and '+str(np.round(phen_max, 1))+' eV.')
                self.phen = sp_phen
                self.on_show_map_button()
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
        def f(pitch): return (f_interp_phen(pitch)-sp_phen)
        # f = lambda pitch: (f_interp_phen(pitch)-sp_phen)
        pitch0 = (pitch_min+pitch_max)/2  # start value in the center of range
        # root finding does not support specification of bounds
        solroot = scipy.optimize.root(f, [pitch0])
        if not solroot.success:
            print(
                mono.infotxt+': issue with finding the pitch angle, scipy.optimize.root status:')
            print(str(solroot))
            return False

        # Verify that determined setpoint is not the result of extrapolation process
        setpoint_pitch = solroot.x[0]
        is_interpolation = (pitch_min <= setpoint_pitch) and (
            setpoint_pitch <= pitch_max)
        if not is_interpolation:
            print(mono.infotxt+': determined pitch setpoint is extrapolation of crystal curve data set, this is an error.')
            print(str(solroot))
            return False

        # Check that the determined setpoint is within the travel range of the actuator
        # Don't use the full travel range (note that 'abs' was used to guard against
        # negative safety margin values)
        setpoint_pitch_inrange = (mono.pitch_min+abs(mono.pitch_minmax_safetymargin) <= setpoint_pitch) and (
            setpoint_pitch <= mono.pitch_max-abs(mono.pitch_minmax_safetymargin))
        if setpoint_pitch_inrange == False:
            print(
                mono.infotxt+f': determined pitch setpoint {setpoint_pitch} not in allowed travel range (min={mono.pitch_min}, max={mono.pitch_max}, safety_margin={mono.pitch_minmax_safetymargin}')
            return False

        # determine dE_photon/dpitch
        d_pitch = 1e-3  # deg
        deriv = (f_interp_phen(setpoint_pitch+d_pitch/2)
                 - f_interp_phen(setpoint_pitch-d_pitch/2))/d_pitch

        # determine roll setpoint
        f_interp_roll = interpolate.interp1d(cd.pitch, cd.roll)
        setpoint_roll = f_interp_roll(setpoint_pitch)
        setpoint_roll *= 180/np.pi  # rad=>deg
        # NOTE: currently not using this setpoint as additional considerations are needed

        print(mono.infotxt
              + f': setpoint pitch={setpoint_pitch}, roll={self.roll_angle_edit.text()}')
        if self.scan_checkBox.isChecked() == 1:
            self.scanlabel.setText(
                'Computed pitch angle: '+'{:.4f}'.format(setpoint_pitch))
            self.logbookstring.append(datetime.now().isoformat()+':   Set Eph was noted to change to '+str(self.undulatorph.value(
            ))+' eV. Moving crystal pitch to ' + '{:.4f}'.format(setpoint_pitch) + 'deg (model Eph: ' + str(sp_phen) + ' eV).\n')
            self.phen_sp = sp_phen
        else:
            self.computed_pitch_angle_display.setText(
                '{:.4f}'.format(setpoint_pitch))
            self.computed_pitch_angle_slope_display.setText(
                '{:.2f}'.format(deriv))
        #self.computed_roll_angle_display.setText('1.58=const') # FIXME

        ### Store the setpoint in the internal structure ###
        mono.setpoint.pitch = setpoint_pitch
        #print('assuming roll from config table or roll=1.58 (overriding result of setpoint computation)')
        # 1.58 # FIXME: computed roll point is currently not used
        mono.setpoint.roll = float(self.roll_angle_edit.text())
        mono.setpoint.valid = True
        print('*** Crystal setpoint values updated ***')
        return True

    def on_photon_energy_enter(self):
        print('photon energy edit: [enter] detected')
        phen_str = self.photon_energy_edit.text()
        # convert string to number, continue only if this works
        try:
            self.phen = float(phen_str)
        except ValueError:
            print(f'photon energy cannot convert "{phen_str}" into number')
            self.loglabel.setText(
                'Make sure the Photon Energy value is a valid number.')
            self.display_map_button.setEnabled(False)
            return
        self.loadCsv()
        self.loglabel.setText(
            'Select a configuration from the table or click Display Map.')
        self.display_map_button.setEnabled(True)

        #self.determine_setpoints(self.phen)

    def on_calc_photon_energy_enter(self):
        print('photon energy edit: [enter] detected')
        phen_str = self.photonE.text()
        # convert string to number, continue only if this works
        try:
            self.phen_calc = float(phen_str)
        except ValueError:
            print(f'photon energy cannot convert "{phen_str}" into number')
            return
        self.determine_setpoints(self.phen_calc)

    def on_calc_roll_angle_enter(self):
        print('roll angle edit: [enter] detected')
        roll_str = self.roll_angle_edit.text()
        # convert string to number, continue only if this works
        try:
            self.roll_calc = float(roll_str)
        except ValueError:
            print(f'roll angle cannot convert "{roll_str}" into number')
            return
        self.rollconfig = self.roll_calc

    def on_params_report_button(self):
        print('reporting correction parameters: ' + str(self.mono2.corrparams))

    def on_params_fromDOOCS_button(self):
        print('previous correction parameters: ' + str(self.mono2.corrparams))
        self.mono2.corrparams = hxrss_io_crystal_parameters_fromDOOCS()
        print('loaded correction parameters from DOOCS:'
              + str(self.mono2.corrparams))

    def on_params_default_button(self):
        print('previous correction parameters: ' + str(self.mono2.corrparams))
        self.mono2.corrparams = hxrss_io_crystal_parameters_default()
        print('loaded default correction parameters:'
              + str(self.mono2.corrparams))

    def on_update_table_button(self):
        print('Updating table')
        try:
            update_table()
        except:
            print('Table not updated.')
            return
        print('Table updated successfully.')

    def loadCsv(self):
        df = pd.read_csv(self.filename)
        cols = df.columns.tolist()
        cols = ['date', 'SA2 Color 1 EPH', 'Mono 2 PA', 'Mono 2 RA']
        enfilt = (df['SA2 Color 1 EPH'] > self.phen
                  - 1000) & (df['SA2 Color 1 EPH'] < self.phen+1000)
        df = df[enfilt]
        df = df.sort_values(by="date", ascending=False)
        model = pandasModel(df[cols])
        self.tableView.setModel(model)

    def viewClicked(self, clickedIndex):
        row = clickedIndex.row()
        model = clickedIndex.model()

    def on_row_double_click(self):
        self.tableButton.setEnabled(True)
        for idx in self.tableView.selectionModel().selectedIndexes():
            row_number = idx.row()
            column_number = idx.column()
        timestampvalue = idx.sibling(row_number, 0).data()
        self.loglabel.setText('Selected configuration from ' + timestampvalue
                              + '. Click Display Map to see reflections with this configuration.')

        self.pitchconfig = float(idx.sibling(row_number, 2).data())
        self.rollconfig = float(idx.sibling(row_number, 3).data())
        self.roll_angle_edit.setText('{:.3f}'.format(self.rollconfig))

    def on_table_clear_click(self):
        self.tableView.clearSelection()
        self.loglabel.setText(
            'Select a configuration from the table or click Display Map.')
        self.roll_angle_edit.setText('{:.3f}'.format(self.mono2.setpoint.roll))
        self.pitchconfig = None
        self.rollconfig = None
        #print(value)

    def on_logbook_button(self, msg_text):
        self.logbook_entry(widget=self.tab, text=msg_text)

    def get_screenshot(self, window_widget):
        screenshot_tmp = QtCore.QByteArray()
        screeshot_buffer = QtCore.QBuffer(screenshot_tmp)
        screeshot_buffer.open(QtCore.QIODevice.WriteOnly)
        widget = QtWidgets.QWidget.grab(window_widget)
        widget.save(screeshot_buffer, "png")
        return screenshot_tmp.toBase64().data().decode()

    def logbook_entry(self, widget, text=""):
        """
        Method to send data + screenshot to eLogbook
        :return:
        """
        #screenshot = self.get_screenshot(widget)
        res = send_to_desy_elog(
            author="", title="Crystal Scan Tool: HXRSS", severity="INFO", text=text, elog="xfellog")
        if res == True:
            self.scanlabel.setText('Finished scan! Logbook entry submitted.')
        if not res:
            self.scanlabel.setText(
                'Finished scan! Error during eLogBook sending.')

    def state_changed(self, int):
        if self.scan_checkBox.isChecked():
            print("CHECKED!")
            self.label_22.setVisible(True)
            self.label_28.setVisible(True)
            self.temp.setVisible(True)
            self.undulatorph.setVisible(True)
            self.apply_button.setEnabled(False)
            self.difference = self.undulatorph.value() - self.phen_calc
            self.logbookstring = []
            self.logbookstring.append(datetime.now().isoformat(
            )+': Started scanning reflection ' + self.reflection_chosen + ' at ' + str(self.phen_calc) + ' eV.\n')
            self.undulatorph.valueChanged.connect(self.sync_phen)
        else:
            print("UNCHECKED!")
            self.label_22.setVisible(False)
            self.label_28.setVisible(False)
            self.temp.setVisible(False)
            self.undulatorph.setVisible(False)
            self.apply_button.setEnabled(True)
            s = ''.join(self.logbookstring)
            if len(s) > 85:
                self.on_logbook_button(s)
            print(s)
            
    def motor_temp_scan_shutdown(self):
        if self.temp.value() > 100:
            self.scan_checkBox.setChecked(False)
            self.label_22.setVisible(False)
            self.label_28.setVisible(False)
            self.temp.setVisible(False)
            self.undulatorph.setVisible(False)
            self.apply_button.setEnabled(True)
            self.logbookstring.append(datetime.now().isoformat()+'Scan mode shut down: motor temperature above threshold')
            self.scanlabel.setText('Scan mode shut down: motor temperature above threshold. Please restart when temperature is below the threshold.')

    def sync_phen(self):
        self.determine_setpoints(self.undulatorph.value()-self.difference)
        # Check motor temperature, if it is over 100 degrees then the scan is stopped
        self.temp.valueChanged.connect(self.motor_temp_scan_shutdown)
        self.on_apply_button()
                    

################################

    def on_apply_button(self):
        cmd = SimpleNamespace()
        cmd.cmd = IO_Cmd.IO_SET
        cmd.setpoints = SimpleNamespace()
        cmd.setpoints.mono2 = SimpleNamespace()
        cmd.setpoints.mono2.pitch = self.mono2.setpoint.pitch
        #print('assuming roll=1.58')
        # FIXME: current standard value in HXRSS_Bragg_max_generator for mono2, need to introduce actual roll angle set points (changes are small, however)
        cmd.setpoints.mono2.roll = self.mono2.setpoint.roll
        cmd.setpoints.mono2.valid = True
        if self.scan_checkBox.isChecked():
            self.scanlabel.setText('Scan mode activated: setpoint updated to pitch: ' + str(
                np.round(self.mono2.setpoint.pitch, 4)) + '° at model phen: ' + str(self.phen_sp) + ' eV')
        else:
            self.calclabel.setText('Crystal setpoint updated: pitch: ' + str(np.round(
                self.mono2.setpoint.pitch, 4)) + '° and roll: ' + str(self.mono2.setpoint.roll)+'°.')
            self.scan_checkBox.setEnabled(True)
        self.q_to_write.put(cmd)

    def on_mono2_crystal_insert_button(self):
        print('crystal2 insert button')
        cmd = SimpleNamespace()
        cmd.cmd = IO_Cmd.IO_SET
        cmd.setpoints = SimpleNamespace()
        cmd.setpoints.mono2_inserted = 'IN'
        self.q_to_write.put(cmd)

    def on_mono2_crystal_park_button(self):
        print('crystal2 park button')
        cmd = SimpleNamespace()
        cmd.cmd = IO_Cmd.IO_SET
        cmd.setpoints = SimpleNamespace()
        cmd.setpoints.mono2_inserted = 'OUT'
        self.q_to_write.put(cmd)


if __name__ == "__main__":
    app = qtw.QApplication([])

    path = os.path.join(os.path.dirname(
        sys.modules[__name__].__file__), 'gui/hxrss.png')
    app.setWindowIcon(QtGui.QIcon(path))

    w = MainWindow()
    w.show()

    app.exec_()
