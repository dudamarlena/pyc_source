# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mico/lib/python2.7/site-packages/mico/util/storage.py
# Compiled at: 2013-04-22 11:40:09
"""This module provides different ways to store metadata on persistent and
volalile storage."""
import os, git, json, hashlib
from __builtin__ import env

class Storage(dict):
    """Models a basic storage. Just an abstraction, see other implementations
    for real use."""
    pass


class FileStorage(Storage):
    """Wrapper to storage in plain JSON files."""

    def __init__(self, path):
        super(FileStorage, self).__init__()
        self.path = path
        try:
            os.makedirs(self.path)
        except OSError:
            pass

    def __setitem__(self, key, value):
        key = hashlib.sha1(str(key)).hexdigest()
        with open(os.path.join(self.path, key), 'w') as (f):
            json.dump(value, f)
        self[key] = value

    def __getitem__(self, key):
        key = hashlib.sha1(str(key)).hexdigest()
        if self.get(key, None):
            return self[key]
        else:
            with open(os.path.join(self.path, key), 'r') as (f):
                _x = json.load(f)
                self[key] = _x
                return _x
            return


class RevisionStorage(Storage):
    """Wrapper to storage which use revision system."""
    REVISION_MESSAGE = 'Automatic update: %(filename)s'

    def __init__(self, path):
        """Create a new revision storage with Git backend.

        :type path: str
        :param path: the path to folder where storage will lives.
        """
        super(RevisionStorage, self).__init__()
        self.path = path
        self.repo = git.Repo.init(self.path, mkdir=True)
        writer = self.repo.config_writer()
        writer.set_value('user', 'name', 'mico')
        writer.set_value('user', 'email', 'mico@localhost')

    def __setitem__(self, key, value):
        _path = os.path.join(self.path, os.path.dirname(key).strip('/'))
        try:
            os.makedirs(_path)
        except OSError:
            pass

        _path = os.path.join(self.path, key.strip('/'))
        with open(_path, 'w') as (f):
            f.write(value)
        self.repo.git.add(_path)
        self.repo.git.commit(m=self.REVISION_MESSAGE % {'filename': _path})

    def __getitem__(self, key):
        with open(os.path.join(self.path, key.strip('/')), 'r') as (f):
            return f.read()

    def __contains__(self, key):
        return os.path.exists(os.path.join(self.path, key.lstrip('/')))