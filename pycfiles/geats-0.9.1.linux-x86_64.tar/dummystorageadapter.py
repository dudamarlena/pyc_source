# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/storage/dummystorageadapter.py
# Compiled at: 2012-05-06 07:02:29
from abstractstorageadapter import AbstractStorageAdapter

class DummyStorageAdapter(AbstractStorageAdapter):
    """A no-op storage adapter"""

    def define(self):
        return self.wrapped_volume.define()

    def activate(self):
        return self.wrapped_volume.activate()

    def deactivate(self):
        return self.wrapped_volume.deactivate()

    def undefine(self):
        return self.wrapped_volume.undefine()

    def format(self):
        return self.wrapped_volume.format()

    def get_blockdevice(self):
        return self.wrapped_volume.get_blockdevice()

    def get_directory(self):
        return self.wrapped_volume.get_directory()

    def get_filename(self):
        return self.wrapped_volume.get_filename()

    def is_local(self):
        return self.wrapped_volume.is_local()

    def is_online(self):
        return self.wrapped_volume.is_online()