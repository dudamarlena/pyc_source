# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/lib/db/handlers/json.py
# Compiled at: 2018-12-07 08:05:34
# Size of source mod 2**32: 1533 bytes
from __future__ import absolute_import
from .python import Database as PythonDatabase
from .python import Container as PythonContainer
import os.path, json

class Database(PythonDatabase):

    def __init__(self, name, params=None):
        self.name = name
        self.containers = {}
        self.directory = '/tmp'

    def list(self):
        return [Container(self, key) for key in self.containers]

    def put(self, name):
        self.containers[name] = Container(self, name)
        return self.containers[name]


class Container(PythonContainer):

    def __init__(self, db, name):
        self.name = name
        self.filepath = db.directory + '/%s.json' % name
        if not os.path.isfile(self.filepath):
            with open(self.filepath, 'w') as (f):
                json.dump(dict(), f)
        with open(self.filepath) as (f):
            self.data = json.load(f)

    def put(self, *args, **kwargs):
        (PythonContainer.put)(self, *args, **kwargs)
        self.commit()

    def update(self, *args, **kwargs):
        (PythonContainer.update)(self, *args, **kwargs)
        self.commit()

    def truncate(self, *args, **kwargs):
        (PythonContainer.truncate)(self, *args, **kwargs)
        self.commit()

    def delete(self, *args, **kwargs):
        (PythonContainer.delete)(self, *args, **kwargs)
        self.commit()

    def commit(self):
        with open(self.filepath, 'w') as (f):
            json.dump((self.data), f, indent=4)