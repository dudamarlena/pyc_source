# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\serial\tools\list_ports_posix.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 4495 bytes
"""The ``comports`` function is expected to return an iterable that yields tuples
of 3 strings: port name, human readable description and a hardware ID.

As currently no method is known to get the second two strings easily, they are
currently just identical to the port name.
"""
import glob, sys, os
from serial.tools import list_ports_common
plat = sys.platform.lower()
if plat[:5] == 'linux':
    from serial.tools.list_ports_linux import comports
else:
    if plat[:6] == 'darwin':
        from serial.tools.list_ports_osx import comports
    else:
        if plat == 'cygwin':

            def comports(include_links=False):
                devices = glob.glob('/dev/ttyS*')
                if include_links:
                    devices.extend(list_ports_common.list_links(devices))
                return [list_ports_common.ListPortInfo(d) for d in devices]


        else:
            if plat[:7] == 'openbsd':

                def comports(include_links=False):
                    devices = glob.glob('/dev/cua*')
                    if include_links:
                        devices.extend(list_ports_common.list_links(devices))
                    return [list_ports_common.ListPortInfo(d) for d in devices]


            else:
                if plat[:3] == 'bsd' or plat[:7] == 'freebsd':

                    def comports(include_links=False):
                        devices = glob.glob('/dev/cua*[!.init][!.lock]')
                        if include_links:
                            devices.extend(list_ports_common.list_links(devices))
                        return [list_ports_common.ListPortInfo(d) for d in devices]


                else:
                    if plat[:6] == 'netbsd':

                        def comports(include_links=False):
                            """scan for available ports. return a list of device names."""
                            devices = glob.glob('/dev/dty*')
                            if include_links:
                                devices.extend(list_ports_common.list_links(devices))
                            return [list_ports_common.ListPortInfo(d) for d in devices]


                    else:
                        if plat[:4] == 'irix':

                            def comports(include_links=False):
                                """scan for available ports. return a list of device names."""
                                devices = glob.glob('/dev/ttyf*')
                                if include_links:
                                    devices.extend(list_ports_common.list_links(devices))
                                return [list_ports_common.ListPortInfo(d) for d in devices]


                        else:
                            if plat[:2] == 'hp':

                                def comports(include_links=False):
                                    """scan for available ports. return a list of device names."""
                                    devices = glob.glob('/dev/tty*p0')
                                    if include_links:
                                        devices.extend(list_ports_common.list_links(devices))
                                    return [list_ports_common.ListPortInfo(d) for d in devices]


                            else:
                                if plat[:5] == 'sunos':

                                    def comports(include_links=False):
                                        """scan for available ports. return a list of device names."""
                                        devices = glob.glob('/dev/tty*c')
                                        if include_links:
                                            devices.extend(list_ports_common.list_links(devices))
                                        return [list_ports_common.ListPortInfo(d) for d in devices]


                                else:
                                    if plat[:3] == 'aix':

                                        def comports(include_links=False):
                                            """scan for available ports. return a list of device names."""
                                            devices = glob.glob('/dev/tty*')
                                            if include_links:
                                                devices.extend(list_ports_common.list_links(devices))
                                            return [list_ports_common.ListPortInfo(d) for d in devices]


                                    else:
                                        import serial
                                        sys.stderr.write("don't know how to enumerate ttys on this system.\n! I you know how the serial ports are named send this information to\n! the author of this module:\n\nsys.platform = {!r}\nos.name = {!r}\npySerial version = {}\n\nalso add the naming scheme of the serial ports and with a bit luck you can get\nthis module running...\n".format(sys.platform, os.name, serial.VERSION))
                                        raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))
if __name__ == '__main__':
    for port, desc, hwid in sorted(comports()):
        print('{}: {} [{}]'.format(port, desc, hwid))