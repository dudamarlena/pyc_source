# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/pytap/__init__.py
# Compiled at: 2010-09-05 15:04:55
"""
PyTap module that wraps the Linux TUN/TAP device

@author: Dominik George
"""
from fcntl import ioctl
import os, struct, atexit
TUNSETIFF = 1074025674
IFF_TUN = 1
IFF_TAP = 2
DEFAULT_MTU = 1500

class TapDevice:
    """ TUN/TAP device object """

    def __init__(self, mode=IFF_TUN, name='', dev='/dev/net/tun'):
        """
        Initialize TUN/TAP device object

        mode is either IFF_TUN or IFF_TAP to select tun or tap device mode.

        name is the name of the new device. An integer will be added to
        build the real device name.

        dev is the device node name the control channel is connected to.
        """
        self.mode = mode
        if name == '':
            if self.mode == IFF_TUN:
                self.name = 'tun%d'
            elif self.mode == IFF_TAP:
                self.name = 'tap%d'
        elif name.endswith('%d'):
            self.name = name
        else:
            self.name = name + '%d'
        fd = os.open(dev, os.O_RDWR)
        ifs = ioctl(fd, TUNSETIFF, struct.pack('16sH', self.name, self.mode))
        self.name = ifs[:16].strip('\x00')
        self.mtu = DEFAULT_MTU
        self.__fd__ = fd
        atexit.register(self.close)

    def read(self):
        """
        Read data from the device. The device mtu determines how many bytes
        will be read.

        The data read from the device is returned in its raw form.
        """
        data = os.read(self.__fd__, self.mtu)
        return data

    def write(self, data):
        """
        Write data to the device. No care is taken for MTU limitations or similar.
        """
        os.write(self.__fd__, data)

    def ifconfig(self, **args):
        """
        Issue ifconfig command on the device. The method takes the following
        keyword arguments:

         address   => IP address of the device, can be in CIDR notation (see man ifconfig)
         netmask   => Network mask
         network   => Network base address, normally set automatically
         broadcast => Broadcast address, normally set automatically
         mtu       => Link MTU, this will also affect the read() method
         hwclass   => Hardware class, normally ether for ethernet
         hwaddress => Hardware (MAC) address, in conjunction with hwclass
        """
        ifconfig = 'ifconfig ' + self.name + ' '
        try:
            ifconfig = ifconfig + args['address'] + ' '
        except KeyError:
            pass

        try:
            ifconfig = ifconfig + 'netmask ' + args['netmask'] + ' '
        except KeyError:
            pass

        try:
            ifconfig = ifconfig + 'network ' + args['network'] + ' '
        except KeyError:
            pass

        try:
            ifconfig = ifconfig + 'broadcast ' + args['broadcast'] + ' '
        except KeyError:
            pass

        try:
            ifconfig = ifconfig + 'mtu ' + str(args['mtu']) + ' '
        except KeyError:
            pass

        try:
            ifconfig = ifconfig + 'hw ' + args['hwclass'] + ' ' + args['hwaddress'] + ' '
        except KeyError:
            pass

        ret = os.system(ifconfig)
        if ret != 0:
            raise IfconfigError()
        try:
            self.mtu = args['mtu']
        except KeyError:
            pass

    def up(self):
        """
        Bring up device. This will effectively run "ifconfig up" on the device.
        """
        ret = os.system('ifconfig ' + self.name + ' up')
        if ret != 0:
            raise IfconfigError()

    def down(self):
        """
        Bring down device. This will effectively call "ifconfig down" on the device.
        """
        ret = os.system('ifconfig ' + self.name + ' down')
        if ret != 0:
            raise IfconfigError()

    def close(self):
        """
        Close the control channel. This will effectively drop all locks and remove the
        TUN/TAP device.

        You must manually take care that your code does not try to operate on the interface
        after closing the control channel.
        """
        os.close(self.__fd__)


class IfconfigError(Exception):
    """ Exception thrown if an ifconfig command returns with a non-zero exit status. """
    pass