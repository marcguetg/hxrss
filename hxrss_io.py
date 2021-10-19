import threading,queue
import time
from types import SimpleNamespace
import enum
from copy import deepcopy
import pydoocs

class IO_Cmd(enum.Enum):
    IO_JUSTREAD = enum.auto()
    IO_QUIT = enum.auto()
    IO_SET = enum.auto()

###########################
### LOW-LEVEL FUNCTIONS ###
###########################

def simple_doocs_read(addr):
    x = pydoocs.read(addr)
    v = x['data']
    return v

def mono_move_motor(doocs_prefix, sp, *, motor_speed=None):
    #print(f'mono_move_motor function is disabled (would move motor {doocs_prefix} to setpoint {sp}')
    #return
    # if requested, increase motor speed
    if motor_speed is not None:
        original_speed = simple_doocs_read(doocs_prefix+'SPEED.SET')
        print(f'{doocs_prefix}  original speed: {original_speed}')
        pydoocs.write(doocs_prefix+'SPEED.SET', motor_speed)

    print('mono_move_motor: implement code for assigning setpoint and starting motion')
    pydoocs.write(doocs_prefix+'ANGLE.SET', sp)
    time.sleep(1)
    pydoocs.write(doocs_prefix+'CONTROL.START', 1)
    pydoocs.write(doocs_prefix+'CONTROL.START', 0) # according to tooltip: mono control panel sends first 1 and then 0 to the CONTROL.START property???
    time.sleep(3)

    # revert to original motor speed
    if motor_speed is not None:
        pydoocs.write(doocs_prefix+'SPEED.SET', original_speed)

# Value of argument 'sp' determines action
# . 'IN'  ==> mono2 moves in
# . 'OUT' ==> mono2 moves out
def insert_mono(sp):
    print('insert_mono function disabled')
    return
    mono2_prefix_xmotor = 'XFEL.FEL/UNDULATOR.SASE2/MONOCI.2307.SA2/'
    sp_in = -7.5
    sp_out = 1.0
    if sp=='IN':
        mono_move_motor(mono2_prefix_xmotor, sp_in)
    elif sp=='OUT':
        mono_move_motor(mono2_prefix_xmotor, sp_out)
    else:
        print(f'insert_mono: unknown setpoint {sp}, supported values are IN and OUT.')

def set_mono(sp):
    print('set_mono was called with setpoint '+str(sp))
    motor_speed = 80  # percent
    mono_move_motor('XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/', sp.pitch, motor_speed=motor_speed)
    # mono_move_motor('XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/', sp.roll,  motor_speed=motor_speed)
    return

####################################
### READ THREAD AND WRITE THREAD ###
####################################
# Remark: Having a thread dedicated for write operations is advantageous
# since it can wait for the motors to reach their desired position without
# blocking all other I/O functions, such as updating the status indicators.

def thread_write_worker(qin, qout, dbg=False):
    processing_time_warn=30 # seconds
    message_counter=0
    while True:
        item = qin.get()
        if hasattr(item, 'io_dbg'):
            dbg=item.io_dbg
        if dbg: print('write thread: got task from queue')
        if item.cmd==IO_Cmd.IO_QUIT:
            print('write thread: got QUIT cmd ==> leaving')
            break
        tstart = time.time()
        if item.cmd!=IO_Cmd.IO_SET:
            print('ERROR: write thread: got unsupported command')
            continue

        # begin producing reply data structure and record current time
        r = SimpleNamespace()
        r.tag = message_counter
        r.timestamp = time.time() # timestamp to recognise 'old' msgs

        ###########
        # do work #
        ###########
        if hasattr(item.setpoints, 'mono2_inserted'):
            insert_mono(item.setpoints.mono2_inserted)
        if hasattr(item.setpoints,'mono2'):
            set_mono(item.setpoints.mono2)

        tend = time.time()
        dt = tend-tstart
        r.processing_time = dt
        if dbg:
            print('write thread: finishing item, processing time: {}'.format(dt))
        else:
            if dt>processing_time_warn:
                print('write thread: finishing item, excessive processing time was: {}'.format(dt))
        qin.task_done()
        qout.put(r)
        message_counter+=1
    print('write thread is finishing')

def thread_read_worker(qin, qout, dbg=False):
    processing_time_warn=1 # seconds
    message_counter=0
    while True:
        item = qin.get()
        if hasattr(item, 'io_dbg'):
            dbg=item.io_dbg
        if dbg: print('read thread: got task from queue')
        if item.cmd==IO_Cmd.IO_QUIT:
            print('read thread: got QUIT cmd ==> leaving')
            break
        tstart = time.time()
        # do work
        if item.cmd!=IO_Cmd.IO_JUSTREAD:
            print('ERROR: read thread: got unsupported command')
            continue

        r = SimpleNamespace()
        r.tag = message_counter
        r.timestamp = time.time() # timestamp to recognise 'old' msgs
        r.color1_rb = simple_doocs_read('XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR1/E_PHOTON')
        r.color2_rb = simple_doocs_read('XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR2/E_PHOTON')
        r.color3_rb = simple_doocs_read('XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR3/E_PHOTON')
        r.mono1_pitch_rb = simple_doocs_read('XFEL.FEL/UNDULATOR.SASE2/MONOPA.2252.SA2/ANGLE')
        r.mono1_pitch_sp = simple_doocs_read('XFEL.FEL/UNDULATOR.SASE2/MONOPA.2252.SA2/ANGLE.SET')
        r.mono1_roll_rb  = simple_doocs_read('XFEL.FEL/UNDULATOR.SASE2/MONORA.2252.SA2/ANGLE')
        r.mono1_roll_sp  = simple_doocs_read('XFEL.FEL/UNDULATOR.SASE2/MONORA.2252.SA2/ANGLE.SET')
        r.mono2_pitch_rb = simple_doocs_read('XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/ANGLE')
        r.mono2_pitch_sp = simple_doocs_read('XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/ANGLE.SET')
        r.mono2_roll_rb  = simple_doocs_read('XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/ANGLE')
        r.mono2_roll_sp  = simple_doocs_read('XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/ANGLE.SET')
        tend = time.time()
        dt = tend-tstart
        r.processing_time = dt
        if dbg:
            print('read thread: finishing item, processing time: {}'.format(dt))
        else:
            if dt>processing_time_warn:
                print('read thread: finishing item, excessive processing time was: {}'.format(dt))
        qin.task_done()
        qout.put(r)
        message_counter+=1
    print('read thread is finishing')


##### USER INTERFACE #####

# Initial photon energy value to be displayed on the GUI
# Value is fetched once during start-up of the GUI
def get_initial_photon_energy_value():
    print('Reading SASE2 undulator color1 set point as initial value for photon energy field')
    value = simple_doocs_read('XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR1/E_PHOTON')
    return value

def rt_request_update(queue, dbg):
    # send to IO thread
    cmd = SimpleNamespace()
    cmd.cmd = IO_Cmd.IO_JUSTREAD
    cmd.io_dbg = dbg
    queue.put(cmd)

def rt_get_msg(queue,*,block=True): # block parameter has same default as Queue.get
    msg = deepcopy( queue.get(block=block) )
    queue.task_done() # to be sure, data was copied (TODO: determine if needed)
    return msg
