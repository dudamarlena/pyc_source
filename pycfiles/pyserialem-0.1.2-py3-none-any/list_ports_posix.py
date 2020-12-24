# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/tools/list_ports_posix.py
# Compiled at: 2015-09-24 22:14:42
__doc__ = 'The ``comports`` function is expected to return an iterable that yields tuples\nof 3 strings: port name, human readable description and a hardware ID.\n\nAs currently no method is known to get the second two strings easily, they are\ncurrently just identical to the port name.\n'
import glob, sys, os
from serial.tools import list_ports_common
plat = sys.platform.lower()
if plat[:5] == 'linux':
    from serial.tools.list_ports_linux import comports
elif plat[:6] == 'darwin':
    from serial.tools.list_ports_osx import comports
elif plat == 'cygwin':

    def comports():
        devices = glob.glob('/dev/ttyS*')
        return [ list_ports_common.ListPortInfo(d) for d in devices ]


elif plat[:7] == 'openbsd':

    def comports():
        devices = glob.glob('/dev/cua*')
        return [ list_ports_common.ListPortInfo(d) for d in devices ]


elif plat[:3] == 'bsd' or plat[:7] == 'freebsd':

    def comports():
        devices = glob.glob('/dev/cua*[!.init][!.lock]')
        return [ list_ports_common.ListPortInfo(d) for d in devices ]


elif plat[:6] == 'netbsd':

    def comports():
        """scan for available ports. return a list of device names."""
        devices = glob.glob('/dev/dty*')
        return [ list_ports_common.ListPortInfo(d) for d in devices ]


elif plat[:4] == 'irix':

    def comports():
        """scan for available ports. return a list of device names."""
        devices = glob.glob('/dev/ttyf*')
        return [ list_ports_common.ListPortInfo(d) for d in devices ]


elif plat[:2] == 'hp':

    def comports():
        """scan for available ports. return a list of device names."""
        devices = glob.glob('/dev/tty*p0')
        return [ list_ports_common.ListPortInfo(d) for d in devices ]


elif plat[:5] == 'sunos':

    def comports():
        """scan for available ports. return a list of device names."""
        devices = glob.glob('/dev/tty*c')
        return [ list_ports_common.ListPortInfo(d) for d in devices ]


elif plat[:3] == 'aix':

    def comports():
        """scan for available ports. return a list of device names."""
        devices = glob.glob('/dev/tty*')
        return [ list_ports_common.ListPortInfo(d) for d in devices ]


else:
    import serial
    sys.stderr.write("don't know how to enumerate ttys on this system.\n! I you know how the serial ports are named send this information to\n! the author of this module:\n\nsys.platform = %r\nos.name = %r\npySerial version = %s\n\nalso add the naming scheme of the serial ports and with a bit luck you can get\nthis module running...\n" % (sys.platform, os.name, serial.VERSION))
    raise ImportError("Sorry: no implementation for your platform ('%s') available" % (os.name,))
if __name__ == '__main__':
    for port, desc, hwid in sorted(comports()):
        print '%s: %s [%s]' % (port, desc, hwid)