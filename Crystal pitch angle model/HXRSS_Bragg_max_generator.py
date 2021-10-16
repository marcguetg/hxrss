"""
Created on Mon Nov 11 14:12:59 2019

@author: ggeloni
Edited to function by cgrech (Jul 6, 21)
"""

from sympy.utilities.iterables import multiset_permutations
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import time
import logging


import scipy.optimize


def HXRSS_Bragg_max_generator(thplist, h_max, k_max, l_max, dthp, dthy, roll_angle_list, dthr, alpha):
    p_angle_list = []
    phen_list = []
    label_list = []
    linestyle_list = []
    gid_list = []
    color_list = []
    roll_list = []
    min_pitch_list = []
    min_photonenergy_list = []

    #annotaz = plot.annotate(" ", (0,0), (-60, 650), xycoords='axes fraction', textcoords='offset points', va='top')

    def rotm(th, ux, uy, uz):
        r = np.array((
            (ux*ux*(1-np.cos(th))+np.cos(th),     ux*uy*(1-np.cos(th))
             - uz*np.sin(th),     ux*uz*(1-np.cos(th))+uy*np.sin(th)),
            (ux*uy*(1-np.cos(th))+uz*np.sin(th),  uy*uy*(1-np.cos(th))
             + np.cos(th),        uy*uz*(1-np.cos(th))-ux*np.sin(th)),
            (ux*uz*(1-np.cos(th))-uy*np.sin(th),  uy*uz*(1-np.cos(th))
             + ux*np.sin(th),     uz*uz*(1-np.cos(th))+np.cos(th))
            ))
        return r

    #(1) Pitch of thp around PitchAx, and rotation of Yaw and Roll axis:
    def rotm1(thp, pitchax, rollax, yawax):
        r1 = rotm(np.pi/2-thp, pitchax[0], pitchax[1], pitchax[2])
        rollax2 = r1.dot(rollax)
        yawax2 = r1.dot(yawax)
        return r1, rollax2, yawax2

    #(2) Yaw of thy around yawax2, and rotation of Roll axis:
    def rotm2(thy, rollax2, yawax2):
        r2 = rotm(thy, yawax2[0], yawax2[1], yawax2[2])
        rollax3 = r2.dot(rollax2)
        return r2, rollax3

    #(3) Roll of thr around Rollax3:
    def rotm3(thr, rollax3):
        r3 = rotm(thr, rollax3[0], rollax3[1], rollax3[2])
        return r3

    def kirot(thp, thy, thr, n0, pitchax, rollax, yawax):
        #note: it seems like in Alberto's tool the roll and yaw are not transformed by subsequent rotations. For comparison, Ileave this out too.
        r1, rollax2, yawax2 = rotm1(thp, pitchax, rollax, yawax)
        rollax2 = rollax
        yawax2 = yawax
        r2, rollax3 = rotm2(thy, rollax2, yawax2)
        rollax3 = rollax
        r3 = rotm3(thr, rollax3)
        return r3.dot(r2.dot(r1.dot(n0)))

    # !!! here 'thp' is in radians !!!
    def phev(fact, n, h, k, l, a, thp, thy, thr, n0, pitchax, rollax, yawax):
        d = a/np.sqrt(h**2+k**2+l**2)
        return fact*np.sqrt(h**2+k**2+l**2)/(2*d*n*np.linalg.norm(kirot(thp, thy, thr, n0, pitchax, rollax, yawax).dot((h, k, l))))

#####
    # Determine pitch angle of minimum photon energy (in degrees!)
    # To be checked: It might be that this finds only a local minimum.
    #
    # Additional parameters dthy, alpha, and roll_angle are needed
    # to replicate the coupling of pitch and yaw from main loop
    # also during the optimization process.
    #
    # To find minimum photon energy supported by given (h,k,l):
    #    minimum photon energy <=> maximum value of denominator
    def phev_min(fact, n, h, k, l, a, thp, thy_not_used, thr, n0, pitchax, rollax, yawax,    dthy, alpha, roll_angle):
        def denom(fact, n, h, k, l, a, thp, thy, thr, n0, pitchax, rollax, yawax):
            v = np.linalg.norm(kirot(thp, thy, thr, n0, pitchax, rollax, yawax).dot((h, k, l)))
            return v

        def obj(fact, n, h, k, l, a, my_thp, thy, thr, n0, pitchax, rollax, yawax,    dthy, alpha, roll_angle):
            print('objective function: my_thp=' + repr(my_thp))
            my_thp=my_thp[0] # unpack from numpy.array into number
            # print('yyy {} {} {} {}'.format(dthy,my_thp, roll_angle,alpha))
            # code block copied from main function (there thp is in degrees, so we need to convert)
            DTHY = dthy+(alpha * my_thp*180/np.pi) # conversion of thp from rad to degrees needed
            # AMERICAN YAW DEFINITION, our roll angle
            my_thy = (-DTHY+roll_angle)/180*np.pi
            #
            v = denom(fact, n, h, k, l, a, my_thp, my_thy, thr, n0, pitchax, rollax, yawax)
            print('objective function: pitch angle={} (my_thy={}), value={}'.format(my_thp,my_thy,v))
            return v


        # remark: expected argument type is single-element array
        f = lambda my_thp: -obj(fact, n, h, k, l, a, my_thp, thy_not_used, thr, n0, pitchax, rollax, yawax, dthy, alpha, roll_angle)

        # to prevent the iteration procedure from aborting because of small gradients, etc., let's do a quick scan of the parameter range of interest
        sp_p = np.linspace(0, 2*np.pi, 41)
        sp_best_value = f([sp_p[0]])
        sp_best = sp_p[0]
        for qqq in sp_p:
            curr_value = f([qqq])
            if curr_value<sp_best_value:
                sp_best_value = curr_value
                sp_best = qqq
        print(f'starting point for minimization process is: {sp_best}')

        sol = scipy.optimize.minimize(f, [sp_best], bounds=scipy.optimize.Bounds(0,2*np.pi), options={'ftol':1e-15, 'gtol':1e-9, 'disp':True}) # https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html#optimize-minimize-lbfgsb


        print(str(sol))
        pitch_min = sol.x[0] * 180/np.pi + thp # final coordinate transformation as in 'plotene' (what is DTHP there is thp here) ==> result is in degrees

        # again the code block copied from main function (there thp is in degrees, so we need to convert)
        DTHY = dthy+(alpha * pitch_min) # pitch angle here in degrees, so no conversion needed
        # AMERICAN YAW DEFINITION, our roll angle
        my_thy = (-DTHY+roll_angle)/180*np.pi
        print(f'xyz pitch_min={pitch_min}, my_thy={my_thy} xyz')
        phot_energy_min = phev(fact, n, h, k, l, a, pitch_min/180*np.pi, my_thy, thr, n0, pitchax, rollax, yawax)
        print(f'*** h,k,l=({h},{k},{l}) => min=(pitch={pitch_min}, phot_energy={phot_energy_min}) ***')
        return pitch_min,phot_energy_min


#####
    # !!! 'thplist' is in degrees !!!
    def plotene(thplist, fact, n, h, k, l, a, DTHP, thylist, thr, n0, pitchax, rollax, yawax):
        count = 0
        fout = open('stuff.txt','w')
        for thp, thy in zip(thplist/180*np.pi, thylist):
            print(str( (thp,thy) ), file=fout)
            eevlist[count] = (phev(fact, 1, h, k, l, a, thp,
                                   thy, thr, n0, pitchax, rollax, yawax))
            count = count+1
        gid = [h, k, l]
        thplist_f = thplist+DTHP
        fout.close()
        return thplist_f, eevlist, gid

    # returns True is combination of (h,k,l) is allowed
    def is_allowed_reflection(h,k,l):
       allowed = False
       if (h % 2 and k % 2 and l % 2) or (not(h % 2) and not(k % 2) and not(l % 2) and not((h+k+l) % 4)) and not(h == 0 and k == 0 and l == 0):
           allowed = True
           if h == 0 and k < 0:
               allowed = False
           if h == 0 and k == 0 and l < 0:
               allowed = False
       return allowed

#User defined quantities
################ AMERICAN NAME CONVENTION --- OUR ROLL IS YAW HERE AND VICEVERSA!!!######################

    pitchax = np.array((-1, 1, 0))/np.linalg.norm(np.array((-1, 1, 0)))
    rollax = np.array((0, 0, 1))/np.linalg.norm(np.array((0, 0, 1)))
    yawax = np.array((1, 1, 0))/np.linalg.norm(np.array((1, 1, 0)))
    n0 = -rollax  # direction of incident radiation

    a = 3.5667899884942195e-10
    hbar = 1.05457173e-34
    clight = 299792458.0
    eel = 1.60217657e-19

    fact = 2*np.pi*clight*hbar/eel

    nord = 1
    hmax = h_max
    kmax = k_max
    lmax = l_max

    eevlist = np.zeros(len(thplist))

    DTHP = dthp  # -0.6921-0.09

    for roll_angle in roll_angle_list:
        # print('xxx {} {} {} {}'.format(dthy,thplist[1], roll_angle, alpha))
        DTHY = dthy+(alpha*thplist)  # 15#15#0#-0.15#-0.39#-0.15 #0.0885
        DTHR = dthr
        # AMERICAN YAW DEFINITION, our roll angle
        thylist = (-DTHY+roll_angle)/180*np.pi
        thr = (-DTHR)/180*np.pi  # AMERICAN ROLL DEFINITION


        # !!! 'thplist' is in degrees !!!
        for h in range(0, hmax+1):
            for k in range(-kmax, kmax+1):
                for l in range(-lmax, lmax+1):
                    ref = h*np.array((1, 0, 0))+k * \
                                     np.array((0, 1, 0))+l*np.array((0, 0, 1))
                    if is_allowed_reflection(h,k,l):
                          # (thplist, fact, n, h, k, l,   a, DTHP, thylist, thr, n0, pitchax, rollax, yawax):
                        p_angle, phen, gid = plotene(
                            thplist, fact, nord, h, k, l, a, DTHP, thylist, thr, n0, pitchax, rollax, yawax)
                        print('***')
                        min_pitch,min_photonenergy = phev_min(
                            fact, nord, h, k, l, a, DTHP, 0, thr, n0, pitchax, rollax, yawax,
                        #                                 ^ argument not used in function
                            dthy, alpha, roll_angle)
                        phen_list.append(list(phen))
                        p_angle_list.append(list(p_angle))
                        gid_list.append(str(gid))
                        min_pitch_list.append(min_pitch)
                        min_photonenergy_list.append(min_photonenergy)

    # print(f'after main loop: dthy={dthy}')
    # return phen_list, p_angle_list, gid_list
    return phen_list, p_angle_list, gid_list, min_pitch_list, min_photonenergy_list
