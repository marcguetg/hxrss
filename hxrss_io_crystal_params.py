from types import SimpleNamespace

from hxrss_io import simple_doocs_read
from datetime import datetime

# Default correction parameters for mono2
# Parameters before Oct-18, 2021 beamtime are considered to be default parameters.
def hxrss_io_crystal_parameters_default():
    print('*** hxrss_io_crystal_parameters_default: loading default correction parameters for monochromator2 ***')
    d = SimpleNamespace()
    # imperfections of the system (from Channel_list.md document, as of 14.10.2021)
    d.dthp = -0.392      # pitch angle
    d.dthy = 1.17        # roll angle (American convention)
    d.dthr = 0.1675      # yaw angle (American convention)
    d.alpha = 0.00338    # alpha parameter: for different pitch angles, different rolls are needed to bring the lines together
    d.roll_list = [1.58]
    return d

def hxrss_io_crystal_parameters_fromDOOCS():
    print('*** hxrss_io_crystal_parameters_default: correction parameters for monochromator2 from DOOCS channels ***')
    prefix='XFEL.UTIL/DYNPROP/MISC/'
    d = SimpleNamespace()
    # imperfections of the system (channel assignment as per Confluence page)
    d.dthp = simple_doocs_read(prefix+'C1')  # pitch angle
    d.dthy = simple_doocs_read(prefix+'C2')  # roll angle (American convention)
    d.dthr = simple_doocs_read(prefix+'C3')  # yaw angle (American convention)
    d.alpha = simple_doocs_read(prefix+'C4') # alpha parameter: for different pitch angles, different rolls are needed to bring the lines together
    d.roll_list = [1.58]
    d.timestamp = datetime.now()
    d.from_DOOCS=1
    return d

