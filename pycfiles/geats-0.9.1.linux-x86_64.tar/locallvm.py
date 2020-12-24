# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/storage/locallvm.py
# Compiled at: 2012-05-06 01:27:39
from os.path import exists

class LocalLVMVolume:

    def __init__(self, name, definition, vm, config):
        self.name = name
        self.definition = definition
        self.vm = vm

    def get_name(self):
        return self.name

    def define(self):
        """lvcreate"""
        os.system("tar -C '%s' -xzpsSf '%s'" % (rootfs, targz))
        return

    def activate(self):
        """mount it"""
        return

    def deactivate(self):
        """unmount it"""
        return

    def undefine(self):
        """lvremove it"""
        return

    def format(self):
        return

    def get_blockdevice(self):
        return self.definition.get('blockdevice', '/dev/null')

    def is_local(self):
        return True

    def is_online(self):
        return os.path.exists(self.get_blockdevice())