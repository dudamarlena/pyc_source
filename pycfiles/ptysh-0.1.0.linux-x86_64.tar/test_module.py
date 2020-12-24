# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/modules/test_module.py
# Compiled at: 2016-08-03 23:00:14
import dbus
from sys import path
from ptysh_module import PtyshModule
from ptysh_util import Singleton
DBUS_BUS_NAME = 'com.kssim.test'
DBUS_OBJECT_PATH = '/com/kssim/test'

class test_module(PtyshModule, Singleton):

    def __init__(self):
        PtyshModule.__init__(self)
        PtyshModule.set_node_name(self, 'hello')
        PtyshModule.set_command(self, 'hello', 'say hello', self.cmd_print_hello, False, True)
        PtyshModule.set_command(self, 'hello_world', 'say hello world', self.cmd_print_hello_world, True, True)
        PtyshModule.set_command(self, 'change_msg', 'change print msg', self.cmd_send_msg_to_daemon, False, True)

    def cmd_print_hello(self):
        print 'hello'

    def cmd_print_hello_world(self):
        print 'hello world'

    def cmd_send_msg_to_daemon(self, in_msg):
        try:
            bus = dbus.SystemBus()
            bus_object = bus.get_object(DBUS_BUS_NAME, DBUS_OBJECT_PATH)
            bus_interface = dbus.Interface(bus_object, DBUS_BUS_NAME)
            bus_interface.receive_signal(in_msg)
        except:
            print 'The daemon is not loaded.'