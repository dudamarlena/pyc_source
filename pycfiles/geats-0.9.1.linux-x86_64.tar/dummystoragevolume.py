# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/storage/dummystoragevolume.py
# Compiled at: 2012-05-06 02:42:23
from abstractstoragevolume import AbstractStorageVolume

class DummyStorageVolume(AbstractStorageVolume):

    def __init__(self, name, definition, vm, config):
        self.name = name
        self.definition = definition
        self.vm = vm

    def get_name(self):
        return self.name

    def define(self):
        return

    def activate(self):
        return

    def deactivate(self):
        return

    def undefine(self):
        return

    def format(self):
        return

    def get_blockdevice(self):
        return self.definition.get('blockdevice', None)

    def get_directory(self):
        return self.definition.get('directory', None)

    def get_filename(self):
        return self.definition.get('filename', None)

    def is_local(self):
        return True

    def is_online(self):
        return True