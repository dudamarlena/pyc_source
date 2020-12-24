# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/storage/mountstorage.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 5871 bytes
from __future__ import print_function
import six
from mediagoblin.storage import StorageInterface, clean_listy_filepath

class MountError(Exception):
    pass


class MountStorage(StorageInterface):
    __doc__ = '\n    Experimental "Mount" virtual Storage Interface\n\n    This isn\'t an interface to some real storage, instead it\'s a\n    redirecting interface, that redirects requests to other\n    "StorageInterface"s.\n\n    For example, say you have the paths:\n\n     1. [\'user_data\', \'cwebber\', \'avatar.jpg\']\n     2. [\'user_data\', \'elrond\', \'avatar.jpg\']\n     3. [\'media_entries\', \'34352f304c3f4d0ad8ad0f043522b6f2\', \'thumb.jpg\']\n\n    You could mount media_entries under CloudFileStorage and user_data\n    under BasicFileStorage.  Then 1 would be passed to\n    BasicFileStorage under the path [\'cwebber\', \'avatar.jpg\'] and 3\n    would be passed to CloudFileStorage under\n    [\'34352f304c3f4d0ad8ad0f043522b6f2\', \'thumb.jpg\'].\n\n    In other words, this is kind of like mounting /home/ and /etc/\n    under different filesystems on your operating system... but with\n    mediagoblin filestorages :)\n\n    To set this up, you currently need to call the mount() method with\n    the target path and a backend, that shall be available under that\n    target path.  You have to mount things in a sensible order,\n    especially you can\'t mount ["a", "b"] before ["a"].\n    '

    def __init__(self, **kwargs):
        self.mounttab = {}

    def mount(self, dirpath, backend):
        """
        Mount a new backend under dirpath
        """
        new_ent = clean_listy_filepath(dirpath)
        print('Mounting:', repr(new_ent))
        already, rem_1, table, rem_2 = self._resolve_to_backend(new_ent, True)
        print('===', repr(already), repr(rem_1), repr(rem_2), len(table))
        if not len(rem_2) > 0:
            assert None not in table, 'That path is already mounted'
        if not len(rem_2) > 0:
            assert len(table) == 0, 'A longer path is already mounted here'
        for part in rem_2:
            table[part] = {}
            table = table[part]

        table[None] = backend

    def _resolve_to_backend(self, filepath, extra_info=False):
        """
        extra_info = True is for internal use!

        Normally, returns the backend and the filepath inside that backend.

        With extra_info = True it returns the last directory node and the
        remaining filepath from there in addition.
        """
        table = self.mounttab
        filepath = filepath[:]
        res_fp = None
        while True:
            new_be = table.get(None)
            if new_be is not None or res_fp is None:
                res_be = new_be
                res_fp = filepath[:]
                res_extra = (table, filepath[:])
            if len(filepath) == 0:
                break
            query = filepath.pop(0)
            entry = table.get(query)
            if entry is not None:
                table = entry
                res_extra = (table, filepath[:])
            else:
                break

        if extra_info:
            return (res_be, res_fp) + res_extra
        else:
            return (
             res_be, res_fp)

    def resolve_to_backend(self, filepath):
        backend, filepath = self._resolve_to_backend(filepath)
        if backend is None:
            raise MountError('Path not mounted')
        return (
         backend, filepath)

    def __repr__(self, table=None, indent=[]):
        res = []
        if table is None:
            res.append('MountStorage<')
            table = self.mounttab
        v = table.get(None)
        if v:
            res.append('  ' * len(indent) + repr(indent) + ': ' + repr(v))
        for k, v in six.iteritems(table):
            if k == None:
                continue
            res.append('  ' * len(indent) + repr(k) + ':')
            res += self.__repr__(v, indent + [k])

        if table is self.mounttab:
            res.append('>')
            return '\n'.join(res)
        else:
            return res

    def file_exists(self, filepath):
        backend, filepath = self.resolve_to_backend(filepath)
        return backend.file_exists(filepath)

    def get_file(self, filepath, mode='r'):
        backend, filepath = self.resolve_to_backend(filepath)
        return backend.get_file(filepath, mode)

    def delete_file(self, filepath):
        backend, filepath = self.resolve_to_backend(filepath)
        return backend.delete_file(filepath)

    def file_url(self, filepath):
        backend, filepath = self.resolve_to_backend(filepath)
        return backend.file_url(filepath)

    def get_local_path(self, filepath):
        backend, filepath = self.resolve_to_backend(filepath)
        return backend.get_local_path(filepath)

    def copy_locally(self, filepath, dest_path):
        """
        Need to override copy_locally, because the local_storage
        attribute is not correct.
        """
        backend, filepath = self.resolve_to_backend(filepath)
        backend.copy_locally(filepath, dest_path)