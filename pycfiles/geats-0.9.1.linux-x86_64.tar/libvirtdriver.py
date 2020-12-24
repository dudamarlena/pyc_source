# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/virtualmachine/libvirtdriver.py
# Compiled at: 2013-02-19 02:46:03
from vagoth.virt.exceptions import DriverException
import libvirt, mako

class Connection(object):

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None
        self.count = 0
        return

    def __enter__(self):
        if self.conn is None:
            self.conn = libvirt.open(self.connection_string)
        self.count += 1
        return

    def __exit__(self, *args):
        self.count -= 1
        if self.count > 0:
            return
        else:
            if self.conn != None:
                self.conn.close()
            self.conn = None
            return


class LibvirtDriver(object):

    def __init__(self, manager, local_config):
        self.config = local_config

    def provision(self, node, vm):
        pass

    def define(self, node, vm):
        pass

    def undefine(self, node, vm):
        pass

    def deprovision(self, node, vm):
        pass

    def start(self, node, vm):
        pass

    def reboot(self, node, vm):
        pass

    def stop(self, node, vm):
        pass

    def shutdown(self, node, vm):
        pass

    def info(self, node, vm):
        pass

    def status(self, node, vm):
        pass

    def migrate(self, node, vm):
        pass