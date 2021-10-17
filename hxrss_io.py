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

def simple_doocs_read(addr):
    x = pydoocs.read(addr)
    v = x['data']
    return v

def insert_mono(sp):
    print('insert_mono function is disabled')

def set_mono(sp):
    print('set_mono function is disabled, it was called with setpoint: '+str(sp))
    return

    '''
    motor_speed = 80  # percent
    original_speed_pitch = simple_doocs_read('XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/SPEED.SET')
    original_speed_roll  = simple_doocs_read('XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/SPEED.SET')
    print(f'original speeds: roll {original_speed_pitch}, pitch {original_speed_pitch}')

    # increase motor speeds to fast
    pydoocs.write('XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/SPEED.SET', motor_speed)
    pydoocs.write('XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/SPEED.SET', motor_speed)

    time.sleep(10)
    print('==> implement code move mono2 to setpoint: pitch='+str(sp.pitch)+' roll='+str(sp.roll))

    # recover original motor speed settings
    print('reverting to original motor speed values')
    pydoocs.write('XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/SPEED.SET', original_speed_pitch)
    pydoocs.write('XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/SPEED.SET', original_speed_roll)
    return
    '''

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
        # do work
        if item.cmd!=IO_Cmd.IO_SET:
            print('ERROR: write thread: got unsupported command')
            continue

        r = SimpleNamespace()
        r.tag = message_counter
        r.timestamp = time.time() # timestamp to recognise 'old' msgs

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
        r.color2_rb = 234
        r.color3_rb = 456
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
    x = pydoocs.read('XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR1/E_PHOTON')
    value = x['data']
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
