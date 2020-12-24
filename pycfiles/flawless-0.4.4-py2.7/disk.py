# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/lib/storage/disk.py
# Compiled at: 2017-12-22 12:31:47
import os, flawless.lib.config
from flawless.lib.data_structures.persistent_dictionary import PersistentDictionary
from flawless.lib.storage import StorageInterface

class DiskStorage(StorageInterface):

    def __init__(self, partition):
        super(DiskStorage, self).__init__(partition)
        config = flawless.lib.config.get()
        if self.partition:
            filepath = os.path.join(config.data_dir_path, 'flawless-errors-', partition)
        else:
            filepath = os.path.join(config.data_dir_path, 'flawless-whitelists-config')
        self.disk_dict = PersistentDictionary(filepath)

    def _proxyfunc_(self, attr, *args, **kwargs):
        try:
            return getattr(self.disk_dict, attr)(*args, **kwargs)
        except KeyError:
            return

        return

    def open(self):
        self.disk_dict.open()
        migrated_dict = dict()
        for key, value in self.disk_dict.dict.items():
            self.migrate_thrift_obj(key)
            self.migrate_thrift_obj(value)
            migrated_dict[key] = value

        self.disk_dict.dict = migrated_dict

    def sync(self):
        self.disk_dict.sync()

    def close(self):
        self.disk_dict.close()

    def iteritems(self):
        return self.disk_dict.dict.iteritems()

    def __setitem__(self, key, item):
        self.disk_dict[key] = item

    def __getitem__(self, key):
        try:
            return self.disk_dict[key]
        except KeyError:
            return

        return

    def __contains__(self, key):
        return key in self.disk_dict