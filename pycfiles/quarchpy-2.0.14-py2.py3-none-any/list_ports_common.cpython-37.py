# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\serial\tools\list_ports_common.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 3354 bytes
import re, glob, os, os.path

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
    __doc__ = 'Info collection base class for serial ports'

    def __init__(self, device=None):
        self.device = device
        self.name = os.path.basename(device)
        self.description = 'n/a'
        self.hwid = 'n/a'
        self.vid = None
        self.pid = None
        self.serial_number = None
        self.location = None
        self.manufacturer = None
        self.product = None
        self.interface = None
        if device is not None:
            if os.path.islink(device):
                self.hwid = 'LINK={}'.format(os.path.realpath(device))

    def usb_description(self):
        """return a short string to name the port based on USB info"""
        if self.interface is not None:
            return '{} - {}'.format(self.product, self.interface)
        if self.product is not None:
            return self.product
        return self.name

    def usb_info(self):
        """return a string with USB related information about device"""
        return 'USB VID:PID={:04X}:{:04X}{}{}'.format(self.vid or 0, self.pid or 0, ' SER={}'.format(self.serial_number) if self.serial_number is not None else '', ' LOCATION={}'.format(self.location) if self.location is not None else '')

    def apply_usb_info(self):
        """update description and hwid from USB data"""
        self.description = self.usb_description()
        self.hwid = self.usb_info()

    def __eq__(self, other):
        return self.device == other.device

    def __lt__(self, other):
        return numsplit(self.device) < numsplit(other.device)

    def __str__(self):
        return '{} - {}'.format(self.device, self.description)

    def __getitem__(self, index):
        """Item access: backwards compatible -> (port, desc, hwid)"""
        if index == 0:
            return self.device
        if index == 1:
            return self.description
        if index == 2:
            return self.hwid
        raise IndexError('{} > 2'.format(index))


def list_links(devices):
    """    search all /dev devices and look for symlinks to known ports already
    listed in devices.
    """
    links = []
    for device in glob.glob('/dev/*'):
        if os.path.islink(device) and os.path.realpath(device) in devices:
            links.append(device)

    return links


if __name__ == '__main__':
    print(ListPortInfo('dummy'))