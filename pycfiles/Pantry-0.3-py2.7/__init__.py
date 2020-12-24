# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pantry/__init__.py
# Compiled at: 2016-02-05 08:30:19
import os.path, pickle

class pantry(object):

    def __init__(self, filename):
        self.filename = filename

    @classmethod
    def open(cls, filename):
        p = cls(filename)
        p._open_pantry()
        return p

    def close(self):
        self._close_pantry()

    def __enter__(self):
        self._open_pantry()
        return self.db

    def __exit__(self, *args, **kwargs):
        self._close_pantry()

    def _open_pantry(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as (f):
                data = f.read()
                if data:
                    self.db = pickle.loads(data)
                else:
                    self.db = {}
        else:
            self.db = {}

    def _close_pantry(self):
        with open(self.filename, 'wb') as (f):
            data = pickle.dumps(self.db)
            f.write(data)