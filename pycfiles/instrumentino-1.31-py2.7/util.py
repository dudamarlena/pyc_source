# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/util.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
__author__ = 'yoelk'
import sys, os, serial, glob
from serial.serialutil import SerialException
try:
    import _winreg as winreg
except ImportError:
    pass

import itertools

class Chdir:
    """
    Instantiating this class changes the current directory until the object is deleted
    """

    def __init__(self, newPath):
        self.savedPath = os.getcwd()
        os.chdir(newPath)

    def __del__(self):
        os.chdir(self.savedPath)


class SerialUtil:

    def enumerate_serial_ports(self):
        """ Uses the Win32 registry to return an
            iterator of serial (COM) ports
            existing on this computer.
        """
        path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        except WindowsError:
            raise IterationError

        for i in itertools.count():
            try:
                val = winreg.EnumValue(key, i)
                yield str(val[1])
            except EnvironmentError:
                break

    def full_port_name(self, portname):
        """ Given a port-name (of the form COM7,
            COM12, CNCA0, etc.) returns a full
            name suitable for opening with the
            Serial class.
        """
        m = re.match('^COM(\\d+)$', portname)
        if m and int(m.group(1)) < 10:
            return portname
        return '\\\\.\\' + portname

    def getSerialPortsList(self):
        ports = []
        if os.name == 'nt':
            for portname in self.enumerate_serial_ports():
                ports.append(portname)

        elif os.name == 'posix':
            ports = glob.glob('/dev/tty.*')
        return ports


if __name__ == '__main__':
    print SerialUtil().getSerialPortsList()