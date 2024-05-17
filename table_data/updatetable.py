import pandas as pd
import numpy as np
import warnings
import os, sys
from os import listdir
warnings.filterwarnings('ignore')
from collections import defaultdict
import re
from datetime import datetime


def update_table():
    directory = r'/home/xfeloper/user/pySpectrometer/SASE2/'
    status = defaultdict(list)

    for filename in os.listdir(directory):
        if filename.endswith("npz_status.txt"):
            #print(filename)
            filepath=os.path.join(directory, filename)
            #tt = np.load(filepath)

            filedata = np.loadtxt(filepath, dtype='str', delimiter=',', skiprows=1)
            ra1_pos = np.where(filedata == 'XFEL.FEL/UNDULATOR.SASE2/MONORA.2252.SA2/ANGLE')
            ra1_row = ra1_pos[0][0]
            status['Mono 1 RA'].append(np.round(float(filedata[ra1_row][1]),2))

            ra2_pos = np.where(filedata == 'XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/ANGLE')
            ra2_row = ra2_pos[0][0]
            status['Mono 2 RA'].append(np.round(float(filedata[ra2_row][1]),3))

            pa1_pos = np.where(filedata == 'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2252.SA2/ANGLE')
            pa1_row = pa1_pos[0][0]
            status['Mono 1 PA'].append(np.round(float(filedata[pa1_row][1]),3))

            pa2_pos = np.where(filedata == 'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/ANGLE')
            pa2_row = pa2_pos[0][0]
            status['Mono 2 PA'].append(np.round(float(filedata[pa2_row][1]),3))

            col_pos = np.where(filedata == 'XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR1/E_PHOTON')
            col_row = col_pos[0][0]
            status['SA2 Color 1 EPH'].append(np.round(float(filedata[col_row][1]),3))

            xgm_pos = np.where(filedata == 'XFEL.FEL/XGM/XGM.2595.T6/INTENSITY.SLOW.TRAIN')
            xgm_row = xgm_pos[0][0]
            status['SA2 XGM'].append(np.round(float(filedata[xgm_row][1]),3))

            dt1_pos = np.where(filedata == 'XFEL.MAGNETS/CHICANE/HXRSS01/DT_FS')
            dt1_row = dt1_pos[0][0]
            status['C1 DT_FS'].append(np.round(float(filedata[dt1_row][1]),3))

            dt2_pos = np.where(filedata == 'XFEL.MAGNETS/CHICANE/HXRSS02/DT_FS')
            dt2_row = dt2_pos[0][0]
            status['C2 DT_FS'].append(np.round(float(filedata[dt2_row][1]),3))

            ci1_pos = np.where(filedata == 'XFEL.FEL/UNDULATOR.SASE2/MONOCI.2252.SA2/POS')
            ci1_row = ci1_pos[0][0]
            status['Mono 1 Insert'].append(np.round(float(filedata[ci1_row][1]),3))

            ci2_pos = np.where(filedata == 'XFEL.FEL/UNDULATOR.SASE2/MONOCI.2307.SA2/POS')
            ci2_row = ci2_pos[0][0]
            status['Mono 2 Insert'].append(np.round(float(filedata[ci2_row][1]),3))

            result=re.search("([0-9]{8}\-[0-9]{2}\_[0-9]{2}_[0-9]{2})", filepath)
            status['date'].append(datetime.strptime(result.group(1), '%Y%m%d-%H_%M_%S'))

    df = pd.DataFrame(status)
    df.to_csv('machine_status.csv', encoding='utf-8', index=False)