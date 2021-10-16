#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v3 Christoph Lechner (2021-10-15):
    . Can now plot standalone (using Matplotlib.Pyplot) or integrated in PyQt5 program. In the PyQt5 case, the use of 'plt' is not possible.
    . Implemented callback function that is called when user is clicking one line
v2 Christoph Lechner (2021-10-14): added comments, code to pick line by clicking

Created on Sun Sep 26 19:46:24 2021

@author: christiangrech
"""
import numpy as np
from HXRSS_Bragg_max_generator import HXRSS_Bragg_max_generator
from itertools import cycle
from types import SimpleNamespace
import time

def stuff2000_core(fig, canvas, ax, standalone=False, line_pick=None, line_pick_cb=None):
    '''
    line_pick_cb: Caller-supplied callback function that is called whenever the user clicks on a trace, single argument to callback function is 'line_pick' data structure
    '''
    # Function to hover on plot and see a curve's Bragg id
    def on_plot_hover(event):
        # Iterating over each data member plotted
        pressi = False
        thy0 = 0
        thr0 = 0
        # if mouse hovers over Axes instance:
        # -> let's check over which curve we're hovering and report some infos
        # docu: https://matplotlib.org/stable/users/event_handling.html (accessed on 2021-Oct-14)
        if event.inaxes is not None:
            start = time.time()
            for curve in event.inaxes.get_lines():
                # Searching which data member corresponds to current mouse position
                if curve.contains(event)[0]:
                    plt.suptitle('over '+curve.get_gid())
                    fig.canvas.draw()
                    plt.show()
                    hlm = curve.get_gid()
                    print('hlm='+hlm)
                    x, y = event.xdata, event.ydata
                    Pitch = x
                    Phene = y
            end = time.time()
            print('execution time {}'.format(end-start))


    # expecting argument lp to be SimpleNamespace (to get infos about click out of callback function w/o global variables)
    def on_pick(event, lp):
        # returns tuple (x,y) in coordinate system of the plot data
        def xlat_me2plot(ax, me):
            # forward transformation: https://matplotlib.org/2.0.2/users/transforms_tutorial.html (section "The transformation pipeline", old docu but works)
            tr = ax.transLimits+ax.transAxes
            trinv = tr.inverted()
            q = trinv.transform((me.x,me.y))
            return (q[0],q[1])

        me = event.mouseevent # MouseEvent related to the PickEvent (coordinates in Figure coordinate system!)
        obj = event.artist    # information about the clicked line
        ax = obj.axes
        me_data = xlat_me2plot(ax,me) 
        print('MouseEvent ({},{}) => ({},{})'.format(me.x, me.y, me_data[0], me_data[1]))
        xdata = obj.get_xdata()
        ydata = obj.get_ydata()
        ind = event.ind # information about picked point (index into data set), this is not the exact point that was clicked
        print('got onpick event at (x={},y={}), data=(x={},y={},ind={}), gid={}'.format(me_data[0],me_data[1],xdata[ind],ydata[ind],ind, obj.get_gid()))
        #
        infotxt = obj.get_gid()
        lp.info_txt = infotxt
        lp.x = me_data[0]
        lp.y = me_data[1]
        lp.valid = True
        print(str(lp))
        # time.sleep(10)
        if line_pick_cb is not None:
            line_pick_cb(line_pick)





    # store picked line here
    if line_pick is None:
        line_pick = SimpleNamespace()
        line_pick.valid = False

    # maximum h,k,l to scan (generator loops over -hmax .. hmax, etc.)
    hmax, kmax, lmax = 5, 5, 5

    # scan over these pitch angles
    thplist = np.linspace(111, 113, 51)
    thplist = np.linspace(0, 360, 601)

    # test code
    hmax, kmax, lmax = 1,1,1
    # thplist = np.linspace(30, 40, 1001)

    # imperfections of the system (from Channel_list.md document, as of 14.10.2021)
    dthp = -0.392      # pitch angle
    dthy = 1.17        # roll angle (American convention)
    dthr = 0.1675      # yaw angle (American convention)
    alpha = 0.00238    # alpha parameter: for different pitch angles, different rolls are needed to bring the lines together

    roll_list = [1.58]

    #phen_list, p_angle_list, gid_list = HXRSS_Bragg_max_generator(
    #            thplist, hmax, kmax, lmax, dthp, dthy, roll_list, dthr, alpha)
    phen_list, p_angle_list, gid_list, min_pitch, min_photenergy = HXRSS_Bragg_max_generator(
                thplist, hmax, kmax, lmax, dthp, dthy, roll_list, dthr, alpha)

    colors = ['r', 'b', 'g', 'c', 'y', 'k']
    linecolors = cycle(colors)


    # fig,ax = plt.subplots(figsize=(12, 8))
    # canvas = fig.canvas

    for r in range(len(p_angle_list)):
        my_color=next(linecolors)
        ax.plot(p_angle_list[r], phen_list[r], color=my_color, gid=gid_list[r], picker=True, pickradius=20)
        print(f'___ plotted gid={gid_list[r]} in color={my_color} ___')

    ax.plot(min_pitch, min_photenergy, 'kx')

    ax.set_ylim(5000, 20000) # just some reasonable limits (there are also traces outside of this range)
    ax.set_ylim(2000, 20000)
    ax.set_ylabel('Photon Energy (eV)')
    ax.set_xlabel('Pitch angle (deg)')

    # still has some reference to plt, which is not working with PyQt5
    if standalone:
        canvas.mpl_connect('motion_notify_event', on_plot_hover)
    else:
        print('HXRSS line plot: hover infos disabled because not in standalone mode')
    canvas.mpl_connect('pick_event', lambda event: on_pick(event,line_pick))

    if standalone:
        plt.show()
    # if requested: drop the info object into call-supplied call-back function
    if line_pick_cb is not None:
        line_pick_cb(line_pick)

# when working with PyQt5, call this function
def stuff2000(standalone=False, line_pick=None, line_pick_cb=None):
    fig,ax = plt.subplots(figsize=(12, 8))
    canvas = fig.canvas
    stuff2000_core(None,canvas,ax, standalone, line_pick, line_pick_cb)


# STAND-ALONE DEMO
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # TEST 1
    lp = SimpleNamespace()
    lp.valid = False
    stuff2000(standalone=True, line_pick=lp)
    # once Figure is closed by user, display info on selected line
    if lp.valid==True:
        print('you picked line {} at position ({},{})'.format(lp.info_txt,lp.x,lp.y))
    else:
        print('no line was picked')

    # TEST 2: Callback function that is invoked whenevery a line is 'picked' (=clicked)
    def cb(my_lp):
        print('*** Entered Call-Back Function ***')
        print(str(my_lp))
    stuff2000(standalone=True, line_pick_cb=cb)
