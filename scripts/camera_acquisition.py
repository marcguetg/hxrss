#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 16:13:42 2022
Camera images acqusition. Once started the script has to be stopped using CTRL+C
@author: christiangrech
"""

import pydoocs
import time
import json
import pandas as pd
import numpy as np
from datetime import date
from functools import reduce
import matplotlib.pyplot as plt
import pickle
from datetime import datetime

#pd.set_option('plotting.backend', 'pandas_bokeh')

today = date.today()
print("Today's date:", today)
labels = {}
labelsc = {}

camdata = {}
labelsc['camera'] = "XFEL.DIAG/CAMERA/MONO2.CAM1.2304.T1/IMAGE_EXT_ZMQ"
#labelsc['camera'] = "XFEL.FEL/CAM.SA1/SA1_XTD2_IMGFEL/BEAMVIEWCROSSHAIR"
camdata['image'] = []
camdata['timestamp'] = []
camdata['macropulse'] = []

#Simulation and pySpectrometer Data         
fig = plt.figure(figsize=(8,6))
  

#time_length_s = 20
#image_ticks = 0.1
try:
    while True: #time.time() < t_end:
        print("Data read at: ", datetime.now().strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3])
        image = pydoocs.read(labelsc['camera'])["data"]
        camdata['image'].append(image)
        camdata['timestamp'].append(pydoocs.read(labelsc['camera'])["timestamp"])
        camdata['macropulse'].append(pydoocs.read(labelsc['camera'])["macropulse"])
        #time.sleep(image_ticks)
except KeyboardInterrupt:
    pass
    
print('Acquisition Ended')


plt.imshow(image, cmap='viridis')
plt.grid(None)
# Hide grid lines
#plt.colorbar()
# Hide axes ticks
plt.show()
timestampStr = dateTimeObj.strftime('%Y%m%d%H%M%S')
# Store data (serialize)
with open('/pnfs/desy.de/m/projects/felrd/daq/camera/camera_'+timestampStr+'.pkl', 'wb') as handle:
    pickle.dump(camdata, handle, protocol=pickle.HIGHEST_PROTOCOL)