# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cecdaemon/cecusercodes.py
# Compiled at: 2018-09-22 01:48:26
# Size of source mod 2**32: 1180 bytes
__doc__ = ' Listens for CEC keypresses and prints the keycode\n'
from time import sleep
import cec
from cecdaemon.const import USER_CONTROL_CODES

def print_keycode(event, *data):
    """ Takes a python-cec cec.EVENT_COMMAND callback and prints the user control code

    :param event: cec event type (is passed from callback even if unneeded
    :type event: int
    :param data: (code, milsec)
    :type data: tuple
    :param code: cec user command code
    :type code: int
    :param milsec: time pressed in miliseconds
    :type milsec: int
    """
    assert event == 2
    code, milsec = data
    if milsec > 0:
        print(f"{USER_CONTROL_CODES[code]} pressed (hex: {hex(code)}, dec: {code})")


def main():
    """ Inits cec and listens for remote keystrokes
    """
    print('Initializing CEC, please wait...')
    print('If this takes too long ensure the device is not already in use')
    cec.init()
    cec.add_callback(print_keycode, 2)
    print('CEC device initialized, press remote keys or hit ^C to quit')
    try:
        while True:
            sleep(1)

    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()