#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 19:46:24 2021

@author: christiangrech
"""
import numpy as np
from HXRSS_Bragg_max_generator import HXRSS_Bragg_max_generator
import matplotlib.pyplot as plt
import matplotlib
from itertools import cycle

# Function to hover on plot and see a curve's Bragg id
def on_plot_hover(event):
    # Iterating over each data member plotted
    pressi = False
    thy0 = 0
    thr0 = 0
    for curve in plot.get_lines():
        # Searching which data member corresponds to current mouse position
        if curve.contains(event)[0]:
            plot.set_title("over %s" % curve.get_gid())
            fig.canvas.draw()
            plt.show()
            hlm = curve.get_gid()
            x, y = event.xdata, event.ydata
            Pitch = x
            Phene = y


thplist = np.linspace(111, 113, 100)
dthp = -0.392
dthy = 1.17
dthr = 0.1675
alpha = 0.00238
roll_list = [1.58]
hmax, kmax, lmax = 5, 5, 5

phen_list, p_angle_list, gid_list = HXRSS_Bragg_max_generator(
            thplist, hmax, kmax, lmax, dthp, dthy, roll_list, dthr, alpha)

colors = ['r', 'b', 'g', 'c', 'y', 'k']
linecolors = cycle(colors)


fig, ax = plt.subplots(figsize=(12, 8))
plot = fig.add_subplot()


for r in range(len(p_angle_list)):
    plt.plot(p_angle_list[r], phen_list[r], color=next(linecolors), gid=gid_list[r])

plt.ylim(12800, 13200)
plt.ylabel('Photon Energy (eV)')
plt.xlabel('Pitch angle (deg)')
plt.tight_layout()
fig.delaxes(ax)
fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)
