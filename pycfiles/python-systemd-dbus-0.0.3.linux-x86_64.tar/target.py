# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/systemd_dbus/target.py
# Compiled at: 2016-05-04 02:15:23
import dbus, dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
from systemd_dbus.property import Property
from systemd_dbus.exceptions import SystemdError

class Target(object):
    """Abstraction class to org.freedesktop.systemd1.Target interface"""

    def __init__(self, unit_path):
        self.__bus = dbus.SystemBus()
        self.__proxy = self.__bus.get_object('org.freedesktop.systemd1', unit_path)
        self.__interface = dbus.Interface(self.__proxy, 'org.freedesktop.systemd1.Target')