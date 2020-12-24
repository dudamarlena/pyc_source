# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjharries/Code/@wizardsoftheweb/py-rofi-bus/py_rofi_bus/main_dbus_daemon.py
# Compiled at: 2018-06-02 23:19:29
from py_rofi_bus.components import Daemon as DaemonProcess
from py_rofi_bus.dbus import Daemon as DaemonServer

class MainDbusDaemon(DaemonProcess):

    def main(self):
        DaemonServer.bootstrap()


if '__main__' == __name__:
    MainDbusDaemon.bootstrap()