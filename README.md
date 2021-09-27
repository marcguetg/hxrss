# hxrss

## Crystal pitch angle model
A function generates a list of photon energy values for a supplied pitch angle range and roll angle value. All reflection lines in the range of [h, k, l]
values [1, 1, 1] to [hmax, kmax, lmax] are generated.

The crystal calibration parameters are also inputs to the function:
* Pitch angle error: dthp
* Roll angle error: dY = dthy + alpha*pitch_angle
* Yaw angle error: dthr
