# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/systemd_dbus/snapshot.py
# Compiled at: 2016-05-04 02:15:23
import dbus, dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
from systemd_dbus.property import Property
from systemd_dbus.exceptions import SystemdError

class Snapshot(object):
    """Abstraction class to org.freedesktop.systemd1.Snapshot interface"""

    def __init__(self, unit_path):
        self.__bus = dbus.SystemBus()
        self.__proxy = self.__bus.get_object('org.freedesktop.systemd1', unit_path)
        self.__interface = dbus.Interface(self.__proxy, 'org.freedesktop.systemd1.Snapshot')
        self.__properties_interface = dbus.Interface(self.__proxy, 'org.freedesktop.DBus.Properties')
        self.__properties()

    def __properties(self):
        properties = self.__properties_interface.GetAll(self.__interface.dbus_interface)
        attr_property = Property()
        for key, value in properties.items():
            setattr(attr_property, key, value)

        setattr(self, 'properties', attr_property)

    def remove(self):
        try:
            self.__interface.Remove()
        except dbus.exceptions.DBusException as error:
            raise SystemdError(error)