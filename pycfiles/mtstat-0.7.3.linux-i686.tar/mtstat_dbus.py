# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/mtstat/plugins/mtstat_dbus.py
# Compiled at: 2006-12-12 18:59:17
from mtstat.mtstat import mtstat

class mtstat_dbus(mtstat):

    def __init__(self):
        self.name = 'dbus'
        self.format = ('d', 3, 100)
        self.nick = ('sys', 'ses')
        self.vars = ('system', 'session')
        self.init(self.vars, 1)

    def check(self):
        global dbus
        try:
            import dbus
        except:
            raise Exception, 'Module needs the python-dbus module.'

        try:
            self.sysbus = dbus.Bus(dbus.Bus.TYPE_SYSTEM).get_service('org.freedesktop.DBus').get_object('/org/freedesktop/DBus', 'org.freedesktop.DBus')
            try:
                self.sesbus = dbus.Bus(dbus.Bus.TYPE_SESSION).get_service('org.freedesktop.DBus').get_object('/org/freedesktop/DBus', 'org.freedesktop.DBus')
            except:
                self.sesbus = None

        except:
            raise Exception, 'Module is unable to connect to dbus message bus.'

        return True

    def extract(self):
        self.val['system'] = len(self.sysbus.ListServices()) - 1
        try:
            self.val['session'] = len(self.sesbus.ListServices()) - 1
        except:
            self.val['session'] = -1