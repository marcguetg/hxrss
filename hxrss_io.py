do_doocs=False

import queue
import threading
import os
from copy import deepcopy
import enum
from types import SimpleNamespace
from datetime import datetime
import time

if do_doocs:
    import pydoocs

class IO_Cmd(enum.Enum):
    """
    Enumeration for input/output commands.
    """
    IO_JUSTREAD = enum.auto()
    IO_QUIT = enum.auto()
    IO_SET = enum.auto()

def hxrss_io_mono1_motors():
    """
    Returns namespace with prefixes for mono1 motors.
    """
    r = SimpleNamespace()
    r.prefix_pitch = 'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2252.SA2/'
    r.prefix_roll = 'XFEL.FEL/UNDULATOR.SASE2/MONORA.2252.SA2/'
    r.prefix_xmotor = 'XFEL.FEL/UNDULATOR.SASE2/MONOCI.2252.SA2/'
    return r

def hxrss_io_mono2_motors():
    """
    Returns namespace with prefixes for mono2 motors.
    """
    r = SimpleNamespace()
    r.prefix_pitch = 'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/'
    r.prefix_roll = 'XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/'
    r.prefix_xmotor = 'XFEL.FEL/UNDULATOR.SASE2/MONOCI.2307.SA2/'
    return r

def timestr():
    """
    Returns the current time formatted as string.
    """
    now = datetime.now()
    now_s = now.strftime('%Y%m%dT%H%M%S')
    return now_s

def machine_writes_enabled():
    """
    Returns whether machine writes are enabled.
    """
    return do_doocs  # False

def simple_doocs_read(addr):
    """
    Performs a simple read operation in DOOCS.
    """
    if do_doocs:
        x = pydoocs.read(addr)
        v = x['data']
    else:
        v = 42
    return v

def mono_motor_busy(doocs_prefix):
    """
    Checks if a monochromator motor is busy.
    """
    mask_busy = 0x4
    q = simple_doocs_read(doocs_prefix+'HW_STATE')
    is_busy = (q & mask_busy) == mask_busy
    return is_busy

def mono_motor_wait(doocs_prefix):
    """
    Waits until a monochromator motor is not busy.
    """
    fn_abort_file = 'hxrss_abort_wait_42'
    while True:
        if not mono_motor_busy(doocs_prefix):
            break
        try:
            os.remove(fn_abort_file)
            print(f'user requested to leave wait loop (magic file detected and deleted)')
            break
        except FileNotFoundError:
            pass
        time.sleep(0.1)
    print(' DONE')

def mono_move_motor(doocs_prefix, sp, *, motor_speed=None, is_rot=True):
    """
    Moves a monochromator motor to a specified setpoint.
    """
    with open('my_log.txt', 'a') as f:
        f.write(
            timestr() + f' requested update of motor channel {doocs_prefix} to {sp}\n')

    if not machine_writes_enabled():
        print(
            f'mono_move_motor function is disabled (would move motor {doocs_prefix} to setpoint {sp}')
        return

    if motor_speed is not None:
        original_speed = simple_doocs_read(doocs_prefix+'SPEED.SET')
        pydoocs.write(doocs_prefix+'SPEED.SET', motor_speed)

    if is_rot:
        pydoocs.write(doocs_prefix+'ANGLE.SET', sp)
    else:
        pydoocs.write(doocs_prefix+'POS.SET', sp)

    pydoocs.write(doocs_prefix+'CONTROL.START', 1)
    pydoocs.write(doocs_prefix+'CONTROL.START', 0)
    mono_motor_wait(doocs_prefix)

    if motor_speed is not None:
        pydoocs.write(doocs_prefix+'SPEED.SET', original_speed)

def insert_mono(sp):
    """
    Moves mono2 in or out based on the setpoint.
    """
    with open('my_log.txt', 'a') as f:
        f.write(f'insert_mono function called')

    if not machine_writes_enabled():
        print('insert_mono function disabled')
        return
    
    mcfg = hxrss_io_mono2_motors()
    mono2_prefix_xmotor = mcfg.prefix_xmotor
    sp_in = -8.0
    sp_out = 1.0
    if sp == 'IN':
        mono_move_motor(mono2_prefix_xmotor, sp_in,  is_rot=False)
    elif sp == 'OUT':
        mono_move_motor(mono2_prefix_xmotor, sp_out, is_rot=False)
    else:
        print(
            f'insert_mono: unknown setpoint {sp}, supported values are IN and OUT.')

def is_mono2_inserted():
    """
    Checks if mono2 is inserted.
    """
    mcfg = hxrss_io_mono2_motors()
    mono2_prefix_xmotor = mcfg.prefix_xmotor
    mask_range_error = 0x10
    q = simple_doocs_read(mono2_prefix_xmotor+'HW_STATE')
    is_range_error = (q & mask_range_error) == mask_range_error
    is_inserted = not is_range_error
    return is_inserted

def is_mono1_inserted():
    """
    Checks if mono1 is inserted.
    """
    mcfg = hxrss_io_mono1_motors()
    mono1_prefix_xmotor = mcfg.prefix_xmotor
    mask_range_error = 0x10
    q = simple_doocs_read(mono1_prefix_xmotor+'HW_STATE')
    is_range_error = (q & mask_range_error) == mask_range_error
    is_inserted = not is_range_error
    return is_inserted

def set_mono(sp):
    """
    Sets the monochromator based on the provided setpoint.
    """
    print('set_mono was called with setpoint '+str(sp))
    motor_speed = sp.motor_speed
    mcfg = hxrss_io_mono2_motors()
    mono_move_motor(mcfg.prefix_pitch, sp.pitch, motor_speed=motor_speed)
    mono_move_motor(mcfg.prefix_roll, sp.roll,  motor_speed=motor_speed)
    return

def send_doocs(sp):
    """
    Sends data to DOOCS.
    """
    pydoocs.write("XFEL.UTIL/DYNPROP/MONO.2307.SA2/PHOTON_ENERGY", sp)

def send_model(sp):
    """
    Sends crystal model data to DOOCS.
    """
    pydoocs.write("XFEL.UTIL/DYNPROP/MONO.2307.SA2/A4", sp[0])
    pydoocs.write("XFEL.UTIL/DYNPROP/MONO.2307.SA2/A3", sp[1])
    pydoocs.write("XFEL.UTIL/DYNPROP/MONO.2307.SA2/A2", sp[2])
    pydoocs.write("XFEL.UTIL/DYNPROP/MONO.2307.SA2/A1", sp[3])


    pydoocs.write("XFEL.UTIL/DYNPROP/MONO.2307.SA2/A0", sp[4])
    print('updated crystal model in DOOCS: ', str(sp))

def thread_write_worker(qin, qout, dbg=False):
    """
    Worker function for write thread.
    """
    processing_time_warn = 30
    message_counter = 0
    while True:
        item = qin.get()
        if hasattr(item, 'io_dbg'):
            dbg = item.io_dbg
        if dbg:
            print('write thread: got task from queue')
        if item.cmd == IO_Cmd.IO_QUIT:
            print('write thread: got QUIT cmd ==> leaving')
            break
        tstart = time.time()
        if item.cmd != IO_Cmd.IO_SET:
            print('ERROR: write thread: got unsupported command')
            continue

        r = SimpleNamespace()
        r.tag = message_counter
        r.timestamp = time.time()

        if hasattr(item.setpoints, 'mono2_inserted'):
            insert_mono(item.setpoints.mono2_inserted)
        if hasattr(item.setpoints, 'mono2'):
            set_mono(item.setpoints.mono2)
        if hasattr(item.setpoints, 'doocs_phen'):
            send_doocs(item.setpoints.doocs_phen)
        if hasattr(item.setpoints, 'model'):
            send_model(item.setpoints.model)

        tend = time.time()
        dt = tend-tstart
        r.processing_time = dt
        if dbg:
            print('write thread: finishing item, processing time: {}'.format(dt))
        else:
            if dt > processing_time_warn:
                print(
                    'write thread: finishing item, excessive processing time was: {}'.format(dt))
        qin.task_done()
        qout.put(r)
        message_counter += 1
    print('write thread is finishing')

def thread_read_worker(qin, qout, dbg=False):
    """
    Worker function for read thread.
    """
    processing_time_warn = 1
    message_counter = 0
    while True:
        item = qin.get()
        if hasattr(item, 'io_dbg'):
            dbg = item.io_dbg
        if dbg:
            print('read thread: got task from queue')
        if item.cmd == IO_Cmd.IO_QUIT:
            print('read thread: got QUIT cmd ==> leaving')
            break
        tstart = time.time()

        if item.cmd != IO_Cmd.IO_JUSTREAD:
            print('ERROR: read thread: got unsupported command')
            continue

        r = SimpleNamespace()
        r.tag = message_counter
        r.timestamp = time.time()

        r.color1_rb = simple_doocs_read(
            'XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR1/E_PHOTON')
        r.color2_rb = simple_doocs_read(
            'XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR2/E_PHOTON')
        r.color3_rb = simple_doocs_read(
            'XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR3/E_PHOTON')
        r.mono1_motemp_rb = simple_doocs_read(
            'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2252.SA2/MOTEMP')
        r.mono2_motemp_rb = simple_doocs_read(
            'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/MOTEMP')
        r.global_color_rb = simple_doocs_read(
            'XFEL.UTIL/HIGH_LEVEL_STATUS/PHOTON_ENERGY.SA2/PHOTON_ENERGY_INPUT_1')
        r.mono1_pitch_rb = simple_doocs_read(
            'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2252.SA2/ANGLE')
        r.mono1_pitch_sp = simple_doocs_read(
            'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2252.SA2/ANGLE.SET')
        r.mono1_pitch_busy = mono_motor_busy(
            'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2252.SA2/')
        r.mono1_roll_rb = simple_doocs_read(
            'XFEL.FEL/UNDULATOR.SASE2/MONORA.2252.SA2/ANGLE')
        r.mono1_roll_sp = simple_doocs_read(
            'XFEL.FEL/UNDULATOR.SASE2/MONORA.2252.SA2/ANGLE.SET')
        r.mono1_roll_busy = mono_motor_busy(
            'XFEL.FEL/UNDULATOR.SASE2/MONORA.2252.SA2/')
        r.mono2_pitch_rb = simple_doocs_read(
            'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/ANGLE')
        r.mono2_pitch_sp = simple_doocs_read(
            'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/ANGLE.SET')
        r.mono2_pitch_busy = mono_motor_busy(
            'XFEL.FEL/UNDULATOR.SASE2/MONOPA.2307.SA2/')
        r.mono2_roll_rb = simple_doocs_read(
            'XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/ANGLE')
        r.mono2_roll_sp = simple_doocs_read(
            'XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/ANGLE.SET')
        r.mono2_roll_busy = mono_motor_busy(
            'XFEL.FEL/UNDULATOR.SASE2/MONORA.2307.SA2/')
        r.mono1_insert_busy = mono_motor_busy(
            'XFEL.FEL/UNDULATOR.SASE2/MONOCI.2252.SA2/')
        r.mono2_insert_busy = mono_motor_busy(
            'XFEL.FEL/UNDULATOR.SASE2/MONOCI.2307.SA2/')
        r.mono2_is_inserted = is_mono2_inserted()
        r.mono1_is_inserted = is_mono1_inserted()

        tend = time.time()
        dt = tend-tstart
        r.processing_time = dt
        if dbg:
            print('read thread: finishing item, processing time: {}'.format(dt))
        else:
            if dt > processing_time_warn:
                print(
                    'read thread: finishing item, excessive processing time was: {}'.format(dt))
        qin.task_done()
        qout.put(r)
        message_counter += 1
    print('read thread is finishing')

def get_initial_photon_energy_value():
    """
    Fetches the initial photon energy value.
    """
    print('Reading SASE2 undulator color1 set point as initial value for photon energy field')
    value = simple_doocs_read(
        'XFEL.FEL/WAVELENGTHCONTROL.SA2/XFEL.SA2.COLOR1/E_PHOTON')
    return value

def rt_request_update(queue, dbg):
    """
    Requests update in real-time.
    """
    cmd = SimpleNamespace()
    cmd.cmd = IO_Cmd.IO_JUSTREAD
    cmd.io_dbg = dbg
    queue.put(cmd)

def rt_get_msg(queue, *, block=True):
    """
    Gets message from the queue in real-time.
    """
    msg = deepcopy(queue.get(block=block))
    queue.task_done()
    return msg
