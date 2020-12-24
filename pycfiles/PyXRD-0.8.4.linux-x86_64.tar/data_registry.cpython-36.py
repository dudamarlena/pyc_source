# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/io/data_registry.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 5029 bytes
import os
from pkg_resources import resource_filename
from pyxrd.generic.exceptions import AlreadyRegistered, NotRegistered

class DataRegistry(object):
    __doc__ = "\n        Class for registering data directories and files so they're\n        not hard-coded everywhere.\n    "
    _DataRegistry__data_directories = None
    _DataRegistry__data_files = None
    _base_dir = None

    def __init__(self, dirs=[], files=[], *args, **kwargs):
        (super(DataRegistry, self).__init__)(*args, **kwargs)
        self._DataRegistry__data_directories = {}
        self._DataRegistry__data_files = {}
        for name, path, parent in dirs:
            self.register_data_directory(name, path, parent=parent)

        for name, path, parent in files:
            self.register_data_file(name, path, parent=parent)

    def __parse_parent(self, path, parent=None):
        if parent is not None:
            if parent is not None:
                try:
                    path = os.path.join(self._DataRegistry__data_directories[parent], path)
                except KeyError:
                    raise NotRegistered("The data directory named '%s' was not found in the registry" % parent)

        else:
            if path.startswith('./'):
                path = resource_filename('pyxrd.data', path)
            return path

    def register_data_file(self, name, path, parent=None):
        """
            Registers a data file at 'path' called 'name'.
            If this file is inside a registered data directory, you
            can use a relative path by setting the 'parent' keyword argument
            to the name of the parent data-directory. The parent path
            will then be appended to the file's path. Paths are considered to be
            relative to data package.
            
            Note: names are always made full-caps!
            
            If you try to re-register an existing data file, an AlreadyRegistered
            exception will be raised. Similarly if you pass in an unregistered
            parent directory name, NotRegistered will be raised.
        """
        name = name.upper()
        if name not in self._DataRegistry__data_files:
            path = self._DataRegistry__parse_parent(path, parent=parent)
            self._DataRegistry__data_files[name] = path
        else:
            raise AlreadyRegistered("the data file named '%s' was already registered" % name)

    def register_data_directory(self, name, path, parent=None):
        """
            Registers a data directory at 'path' called 'name'.
            If this is a sub-directory of another registered data directory, you
            can use a relative path by setting the 'parent' keyword argument
            to the name of the parent data-directory. The parent path
            will then be appended to the child's path. Paths are considered to be
            relative to data package.
            
            Note: names are always made full-caps!
            
            If you try to re-register an existing data directory, an AlreadyRegistered
            exception will be raised. Similarly if you pass in an unregistered
            parent directory name, NotRegistered will be raised.
        """
        name = name.upper()
        if name not in self._DataRegistry__data_directories:
            path = self._DataRegistry__parse_parent(path, parent=parent)
            self._DataRegistry__data_directories[name] = path
            try:
                os.makedirs(path)
            except OSError:
                pass

        else:
            raise AlreadyRegistered("The data directory named '%s' was already registered" % name)

    def get_directory_path(self, name):
        """
            Gets the absolute path to a data directory named 'name'
        """
        try:
            path = self._DataRegistry__data_directories[name]
            if not os.path.isdir(path):
                return path
            else:
                return path
        except KeyError:
            raise NotRegistered("The data directory named '%s' was not found in the registry" % name)

    def get_all_directories(self):
        """
            Returns a generator looping over all directories in the registry,
            excluding the project path.
        """
        for path in list(self._DataRegistry__data_directories.values()):
            yield path

    def get_file_path(self, name):
        """
            Gets the absolute path to a data file named 'name'
        """
        try:
            return self._DataRegistry__data_files[name]
        except KeyError:
            raise NotRegistered("The data file named '%s' was not found in the registry" % name)

    def get_all_files(self):
        """
            Returns a generator looping over all directories in the registry,
            excluding the project path.
        """
        for path in list(self._DataRegistry__data_directories.values()):
            yield resource_filename('pyxrd.data', path)