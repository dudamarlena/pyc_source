# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/usbarm/usbarm.py
# Compiled at: 2013-12-08 14:17:26
"""
A Python module that allows control of a USB arm with a Unix PC.
PyUSB must be installed for this module to work.
To initialise a connection to the arm, use the command 'usbarm.connect()'.
To send instructions to the arm, use the command 'usbarm.ctrl(duration, command)'.
The duration sets how long the command runs for, and the command tells the arm what to do.

Here are the commands you can use:
usbarm.rotate_ccw
usbarm.rotate_cw
usbarm.shoulder_up
usbarm.shoulder_down
usbarm.elbow_up
usbarm.elbow_down
usbarm.wrist_up
usbarm.wrist_down
usbarm.grip_open
usbarm.grip_close
usbarm.light_on
"""
rotate_ccw = [
 0, 1, 0]
rotate_cw = [0, 2, 0]
shoulder_up = [64, 0, 0]
shoulder_down = [128, 0, 0]
elbow_up = [16, 0, 0]
elbow_down = [32, 0, 0]
wrist_up = [4, 0, 0]
wrist_down = [8, 0, 0]
grip_open = [2, 0, 0]
grip_close = [1, 0, 0]
light_on = [0, 0, 1]

def connect():
    """
    Connect to the USB arm.
    """
    global usb_arm
    try:
        from time import sleep
    except:
        raise Exception('Time library not found')

    try:
        import usb.core, usb.util
    except:
        raise Exception('USB library not found')

    usb_arm = usb.core.find(idVendor=4711, idProduct=0)
    if usb_arm == None:
        raise Exception('Robotic arm not found')
    else:
        return True
    return


def ctrl(duration, command):
    """
    Send a command to the USB arm.
    """
    if usb_arm == None:
        raise Exception('Robotic arm not connected')
    usb_arm.ctrl_transfer(64, 6, 256, 0, command, 1000)
    sleep(duration)
    usb_arm.ctrl_transfer(64, 6, 256, 0, [0, 0, 0], 1000)
    return True


if __name__ == '__main__':
    raise Exception("Cannot run standalone - use 'import usbarm' to utlise this module")
    exit()