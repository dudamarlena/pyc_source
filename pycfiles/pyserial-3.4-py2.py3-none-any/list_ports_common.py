# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/tools/list_ports_common.py
# Compiled at: 2015-09-26 22:26:48
import re

def numsplit(text):
    """    Convert string into a list of texts and numbers in order to support a
    natural sorting.
    """
    result = []
    for group in re.split('(\\d+)', text):
        if group:
            try:
                group = int(group)
            except ValueError:
                pass

            result.append(group)

    return result


class ListPortInfo(object):
    """Info collection base class for serial ports"""

    def __init__(self, device=None):
        self.device = device
        self.name = None
        self.description = 'n/a'
        self.hwid = 'n/a'
        self.vid = None
        self.pid = None
        self.serial_number = None
        self.location = None
        self.manufacturer = None
        self.product = None
        self.interface = None
        return

    def usb_description(self):
        if self.interface is not None:
            return ('{} - {}').format(self.product, self.interface)
        else:
            return self.product
            return

    def usb_info(self):
        return ('USB VID:PID={:04X}:{:04X}{}{}').format(self.vid, self.pid, (' SER={}').format(self.serial_number) if self.serial_number is not None else '', (' LOCATION={}').format(self.location) if self.location is not None else '')

    def apply_usb_info(self):
        """update description and hwid from USB data"""
        self.description = self.usb_description()
        self.hwid = self.usb_info()

    def __eq__(self, other):
        return self.device == other.device

    def __lt__(self, other):
        return numsplit(self.device) < numsplit(other.device)

    def __str__(self):
        return ('{} - {}').format(self.device, self.describe())

    def __getitem__(self, index):
        """Item access: backwards compatible -> (port, desc, hwid)"""
        if index == 0:
            return self.device
        if index == 1:
            return self.description
        if index == 2:
            return self.hwid
        raise IndexError(('{} > 2').format(index))


if __name__ == '__main__':
    print ListPortInfo('dummy')