import time
import numpy as np
import pydoocs
import sys
import getopt
import os
	
def HelpAndExit():
    print("This program creates a loop of energies that are written to pyDOOCS with a predefined pause.")
    print("Usage: $ python und_energy_program.py --start_en 8000 --step 4 --no_steps 10 --pause 30")
    print("\t--start_en  \t-start energy value in eV.")
    print("\t--step \t- the difference in eV between each energy change.")
    print("\t--no_steps  \t- number of energy levels in the loop.")
    print("\t--pause \t- duration of pause between energy changes in seconds.")
    print("\t-h\t\t- prints this help.\n")
    sys.exit(1)


def Fatal(msg):
    sys.stderr.write("%s: %s\n\n" % (os.path.basename(sys.argv[0]), msg))
    HelpAndExit()


def pre_loop(argv):
    start_en = None
    step = None
    no_steps = None
    pause = None

    try:
        opts, args = getopt.getopt(argv, "hs:t:n:p", ["start_en=", "step=", "no_steps=", "pause="])
    except getopt.GetoptError:
        HelpAndExit()
    for opt, arg in opts:
        if opt == '-h':
            HelpAndExit()
        elif opt in ("-s", "--start_en"):
            start_en = arg
        elif opt in ("-t", "--step"):
            step = arg
        elif opt in ("-n", "--no_steps"):
            no_steps = arg
        elif opt in ("-p", "--pause"):
            pause = arg
    print('start_en is: ', start_en)
    print('step is: ', step)
    print('no_steps is: ', no_steps)
    print('pause is: ', pause)

    if not step:
        Fatal("Please, check you input arguments and make sure to insert at a step value")
    if not start_en:
        Fatal("Please, check you input arguments and make sure to insert at a starting energy value")
    if not no_steps:
        Fatal("Please, check you input arguments and make sure to insert number of steps value")
    if not pause:
        Fatal("Please, check you input arguments and make sure to insert a pause value")
    return float(start_en), float(step), int(no_steps), float(pause)


if __name__ == "__main__":
    start_en, step, no_steps, pause = pre_loop(sys.argv[1:])
    energy = start_en
    for i in range(no_steps + 1):
        print(f'Setting {i}/{no_steps}: {energy}')
        value  = energy
        pydoocs.write('XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR1/E_PHOTON', value)
        #x = pydoocs.read('XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR1/E_PHOTON')
        time.sleep(0.01)
        pydoocs.write('XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR1/CMD', 1)
        energy = value+step                      
        time.sleep(pause)
                
    print('done')