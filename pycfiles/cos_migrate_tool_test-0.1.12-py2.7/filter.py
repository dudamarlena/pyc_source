# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/migrate_tool/filter.py
# Compiled at: 2017-03-29 00:21:31
import leveldb
from os import path
from time import time

class Filter(object):

    def __init__(self, work_dir):
        self._workdir = work_dir
        self._db = leveldb.LevelDB(path.join(self._workdir, 'leveldb'))

    def add(self, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self._db.Put(value, str(time()))

    def query(self, value):
        try:
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            self._db.Get(value)
            return True
        except KeyError:
            return False