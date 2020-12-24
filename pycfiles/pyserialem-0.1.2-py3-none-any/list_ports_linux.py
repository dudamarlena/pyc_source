# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/tools/list_ports_linux.py
# Compiled at: 2015-09-26 22:26:34
import glob, os
from serial.tools import list_ports_common

class SysFS(list_ports_common.ListPortInfo):
    """Wrapper for easy sysfs access and device info"""

    def __init__(self, device):
        super(SysFS, self).__init__(device)
        self.name = os.path.basename(device)
        self.usb_device_path = None
        if os.path.exists('/sys/class/tty/%s/device' % (self.name,)):
            self.device_path = os.path.realpath('/sys/class/tty/%s/device' % (self.name,))
            self.subsystem = os.path.basename(os.path.realpath(os.path.join(self.device_path, 'subsystem')))
        else:
            self.device_path = None
            self.subsystem = None
        if self.subsystem == 'usb-serial':
            self.usb_device_path = os.path.dirname(os.path.dirname(self.device_path))
        elif self.subsystem == 'usb':
            self.usb_device_path = os.path.dirname(self.device_path)
        else:
            self.usb_device_path = None
        if self.usb_device_path is not None:
            self.vid = int(self.read_line(self.usb_device_path, 'idVendor'), 16)
            self.pid = int(self.read_line(self.usb_device_path, 'idProduct'), 16)
            self.serial_number = self.read_line(self.usb_device_path, 'serial')
            self.location = os.path.basename(self.usb_device_path)
            self.manufacturer = self.read_line(self.usb_device_path, 'manufacturer')
            self.product = self.read_line(self.usb_device_path, 'product')
            self.interface = self.read_line(self.device_path, 'interface')
        if self.subsystem in ('usb', 'usb-serial'):
            self.apply_usb_info()
        elif self.subsystem == 'pnp':
            self.description = self.name
            self.hwid = self.read_line(self.device_path, 'id')
        elif self.subsystem == 'amba':
            self.description = self.name
            self.hwid = os.path.basename(self.device_path)
        return

    def read_line(self, *args):
        """        Helper function to read a single line from a file.
        One or more parameters are allowed, they are joined with os.path.join.
        Returns None on errors..
        """
        try:
            with open(os.path.join(*args)) as (f):
                line = f.readline().strip()
            return line
        except IOError:
            return

        return


def comports():
    devices = glob.glob('/dev/ttyS*')
    devices.extend(glob.glob('/dev/ttyUSB*'))
    devices.extend(glob.glob('/dev/ttyACM*'))
    devices.extend(glob.glob('/dev/ttyAMA*'))
    devices.extend(glob.glob('/dev/rfcomm*'))
    return [ info for info in [ SysFS(d) for d in devices ] if info.subsystem != 'platform'
           ]


if __name__ == '__main__':
    for port, desc, hwid in sorted(comports()):
        print '%s: %s [%s]' % (port, desc, hwid)