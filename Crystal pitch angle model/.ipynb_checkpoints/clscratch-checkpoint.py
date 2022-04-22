#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v4 Christoph Lechner (2021-10-17)
v3 Christoph Lechner (2021-10-15):
    . Can now plot standalone (using Matplotlib.Pyplot) or integrated in PyQt5 program.
      In the PyQt5 case, the use of 'plt' is not possible.
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

from hxrss_io_crystal_params import hxrss_io_crystal_parameters_default

# 'test_mode' flag limits h,k,l to enable quick preparation of plot
#     to enable quick test iterations
def crystal_plot_core(fig, canvas, ax, standalone=False, line_pick=None, line_pick_cb=None, test_mode=False, corrparams=None, roi=None):
    '''
    line_pick_cb: Caller-supplied callback function that is called whenever the user clicks on a trace, single argument to callback function is 'line_pick' data structure
    '''

    ### TEST OPTIONS ###
    do_indicate_features=False
    do_indicate_features=False
    do_stt=False
    ### end of TEST OPTIONS ###


    # Function to hover on plot and see a curve's Bragg id
    def on_plot_hover(event):
        # Iterating over each data member plotted
        #pressi = False
        #thy0 = 0
        #thr0 = 0
        # if mouse hovers over Axes instance:
        # -> let's check over which curve we're hovering and report some infos
        # docu: https://matplotlib.org/stable/users/event_handling.html (accessed on 2021-Oct-14)
        if event.inaxes is not None:
            start = time.time()
            over_curve=False
            ax = event.inaxes
            for curve in ax.get_lines():
                # Searching which data member corresponds to current mouse position
                if curve.contains(event)[0]:
                    over_curve=True
                    # plt.suptitle('over '+curve.get_gid())
                    ax.set_title('over '+curve.get_gid())
                    #fig.canvas.draw()
                    parent_fig=ax.get_figure()
                    parent_fig.canvas.draw()
                    # not needed to have title of axes updating
                    #plt.show()
                    hlm = curve.get_gid()
                    #print('hlm='+hlm)
            # if mouse isn't hovering over a line (just over the canvas), clear title
            if over_curve==False:
                ax.set_title('')
                parent_fig=ax.get_figure()
                parent_fig.canvas.draw()
            end = time.time()
            #print('on_plot_hover: execution time {}'.format(end-start))


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
        xdata = obj.get_xdata()  # remark: when zoomed out, xdata/ydata/ind can have multiple elements
        ydata = obj.get_ydata()
        ind = event.ind # information about picked point (index into data set), this is not the exact point that was clicked
        print('got onpick event at (x={},y={}), data=(x={},y={},ind={}), gid={}'.format(me_data[0],me_data[1],xdata[ind],ydata[ind],ind, obj.get_gid()))
        #
        infotxt = obj.get_gid()
        lp.info_txt = infotxt
        lp.x = me_data[0]
        lp.y = me_data[1]
        lp.roll = roi.roll[0]
        lp.ax = ax # to plot data, etc.
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
    hmax,kmax,lmax = 5,5,5
    #hmax,kmax,lmax = 3,3,3

    # scan over these pitch angles
    thplist = np.linspace(0, 120, 101)

    # test mode
    if test_mode:
        hmax,kmax,lmax = 3,3,3
        thplist = np.linspace(0, 120, 101)

    # imperfections of the system (mono2 as of Oct-2021)
    if corrparams is None:
        print('==> no correction parameters provided, using default parameters from function hxrss_io_crystal_parameters_default <==')
        corrparams = hxrss_io_crystal_parameters_default()
    dthp = corrparams.dthp    # pitch angle
    dthy = corrparams.dthy    # roll angle (American convention)
    dthr = corrparams.dthr    # yaw angle (American convention)
    alpha = corrparams.alpha  # alpha parameter: for different pitch angles, different rolls are needed to bring the lines together
    #roll_list = corrparams.roll_list
    
    maxE = roi.maxE
    minE = roi.minE
    roll_list = roi.roll
 

    res = HXRSS_Bragg_max_generator(thplist, hmax, kmax, lmax, dthp, dthy, roll_list, dthr, alpha, maxE, minE, return_obj=True, analyze_curves=do_indicate_features)
    phen_list = res.phen_list
    p_angle_list = res.p_angle_list
    gid_list = res.gid_list

    colors = ['r', 'b', 'g', 'c', 'y', 'k']
    linecolors = cycle(colors)

    for r in range(len(p_angle_list)):
        my_color=next(linecolors)
        ax.plot(p_angle_list[r], phen_list[r], color=my_color, gid=gid_list[r], picker=True, pickradius=20)
        #print(f'___ plotted gid={gid_list[r]} in color={my_color} ___')

    # indicate minima using the information returned by Bragg max gen
    if do_indicate_features:
        min_pitch = res.min_pitch_list
        min_photenergy = res.min_photonenergy_list
        ax.plot(min_pitch, min_photenergy, 'kx')

    # stt = "single trace test"
    if do_stt:
        stt_thplist = np.linspace(65, 160, 1001)
        stt_r = HXRSS_Bragg_max_generator(
            stt_thplist, hmax, kmax, lmax, dthp, dthy, roll_list, dthr, alpha, maxE, minE, specific_hkl=[(1,1,-1)], return_obj=True) # <===
        stt_phen_list = stt_r.phen_list
        stt_p_angle_list = stt_r.p_angle_list
        stt_gid_list = stt_r.gid_list
        ax.plot(stt_p_angle_list[0], np.array(stt_phen_list[0]), 'k+')

    #ax.set_ylim(5000, 20000) # just some reasonable limits (there are also traces outside of this range)
    ax.set_ylim(roi.minE+600, roi.maxE-600)
    ax.set_xlim(roi.minpitch, roi.maxpitch)
    ax.set_ylabel('Photon Energy (eV)')
    ax.set_xlabel('Pitch angle (deg)')
    ax.set_title('hover mouse over curve to see its [h,k,l], click to select')

    # still has some reference to plt, which is not working with PyQt5
    '''
    if standalone:
        canvas.mpl_connect('motion_notify_event', on_plot_hover)
    else:
        print('HXRSS line plot: hover infos disabled because not in standalone mode')
    '''
    canvas.mpl_connect('motion_notify_event', on_plot_hover)
    canvas.mpl_connect('pick_event', lambda event: on_pick(event,line_pick))

    if standalone:
        plt.show() # wait for user (not possible with PyQt5-based program)
        # if requested: drop the info object into call-supplied call-back function
        if line_pick_cb is not None:
            line_pick_cb(line_pick)


# when working with PyQt5, call this function
def crystal_plot(standalone=False, line_pick=None, line_pick_cb=None):
    fig,ax = plt.subplots(figsize=(12, 8))
    canvas = fig.canvas
    crystal_plot_core(None,canvas,ax, standalone, line_pick, line_pick_cb)





### STAND-ALONE DEMO ###
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # TEST 1: Information on picked line is retrieved via passed data obj
    lp = SimpleNamespace()
    lp.valid = False
    crystal_plot(standalone=True, line_pick=lp, test_mode=True)
    # once Figure is closed by user, display info on selected line
    if lp.valid==True:
        print('you picked line {} at position ({},{})'.format(lp.info_txt,lp.x,lp.y))
    else:
        print('no line was picked')

    # TEST 2: Callback function that is invoked whenevery a line is 'picked' (=clicked)
    def cb(my_lp):
        print('*** Entered Call-Back Function ***')
        print(str(my_lp))
    crystal_plot(standalone=True, line_pick_cb=cb, test_mode=True)
