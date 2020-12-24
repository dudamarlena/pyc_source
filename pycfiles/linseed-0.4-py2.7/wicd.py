# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/wicd.py
# Compiled at: 2012-02-12 08:57:04
from .exceptions import DataNotAvailable
import dbus

class Interface(object):

    def __init__(self, interface, ip):
        self._interface = interface
        self._ip = ip
        self._connected = bool(self.ip)

    @property
    def interface(self):
        """The interface ID."""
        return self._interface

    @property
    def ip(self):
        """The IP address of the interface."""
        return self._ip

    @property
    def connected(self):
        """Whether the interface is connected."""
        return self._connected


class Wireless(Interface):
    """Information for a single Wireless interface."""

    def __init__(self, proxy, iface):
        ip = proxy.GetWirelessIP(0)
        super(Wireless, self).__init__(iface, ip)
        if self.connected:
            netid = proxy.GetCurrentNetworkID(0)
            self._essid = proxy.GetWirelessProperty(netid, 'essid')
            self._quality = proxy.GetWirelessProperty(netid, 'quality')
        else:
            self._essid = ''
            self._quality = ''

    @property
    def essid(self):
        """The ESSID to which the interface is connected."""
        return self._essid

    @property
    def quality(self):
        """The quality of the connetion."""
        return self._quality


class Wired(Interface):
    """Information on a single wired interface."""

    def __init__(self, proxy, iface, idx):
        try:
            ip = proxy.wired.GetWiredIP(idx)
        except Exception:
            ip = ''

        super(Wired, self).__init__(iface, ip)


class WICD(object):

    def __init__(self):
        try:
            self.bus = dbus.SystemBus()
            self.daemon = self.bus.get_object('org.wicd.daemon', '/org/wicd/daemon')
            wireless = dbus.Interface(self.bus.get_object('org.wicd.daemon', '/org/wicd/daemon/wireless'), 'org.wicd.daemon.wireless')
            if wireless and wireless.DetectWirelessInterface() != 'None':
                self.wireless = [
                 Wireless(wireless, 'wifi')]
            else:
                self.wireless = []
            wired = dbus.Interface(self.bus.get_object('org.wicd.daemon', '/org/wicd/daemon/wired'), 'org.wicd.daemon.wired')
            if wired:
                self.wired = [ Wired(wired, iface, idx) for idx, iface in enumerate(wired.GetWiredInterfaces()) ]
            else:
                self.wired = []
        except dbus.DBusException as e:
            raise DataNotAvailable(str(e))

    def __str__(self):
        rslt = []
        for w in self.wired:
            if w.connected:
                rslt.append(('[{0}] {1}').format(w.interface, w.ip))

        for w in self.wireless:
            if w.connected:
                rslt.append(('[{0}] {1} {2}% ({3})').format(w.interface, w.essid, w.quality, w.ip))

        return (' ').join(rslt)

    @staticmethod
    def name():
        return 'linseed_wicd'

    @staticmethod
    def description():
        return 'WICD connection status'


def main():
    w = WICD()
    print w.display()


if __name__ == '__main__':
    main()