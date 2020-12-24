# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/datas/h5.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 2073 bytes
from dexy.data import Generic
from dexy.storage import GenericStorage
try:
    import tables
    AVAILABLE = True
except ImportError:
    AVAILABLE = False

class H5(Generic):
    __doc__ = '\n    Data type for reading HDF5 files using pytables.\n    '
    aliases = ['h5']
    _settings = {'storage-type': 'h5storage'}

    def is_active(self):
        return AVAILABLE

    def root(self):
        return self.data().root

    def walk_groups(self, path=None):
        if path:
            return self.data().walk_groups(path)
        return self.data().walk_groups()

    def walk_nodes(self, path=None, node_type=None):
        if path:
            if node_type:
                return self.data().walk_nodes(path, node_type)
        if path:
            return self.data().walk_nodes(path)
        return self.data().walk_nodes()


class H5Storage(GenericStorage):
    __doc__ = '\n    Storage backend representing HDF5 files.\n    '
    aliases = ['h5storage']

    def is_active(self):
        return AVAILABLE

    def read_data(self):
        return tables.open_file(self.data_file(read=True), 'r')


if AVAILABLE:

    def my_close_open_files(verbose):
        try:
            open_files = tables.file._open_files
            are_open_files = len(open_files) > 0
            if verbose:
                if are_open_files:
                    print('Closing remaining open files:', end=' ', file=(sys.stderr))
            for fileh in open_files.keys():
                if verbose:
                    print(('%s...' % (open_files[fileh].filename,)), end=' ', file=(sys.stderr))
                open_files[fileh].close()
                if verbose:
                    print('done', end=' ', file=(sys.stderr))

            if verbose:
                if are_open_files:
                    print(file=(sys.stderr))
        except Exception:
            pass


    import sys, atexit
    atexit.register(my_close_open_files, False)