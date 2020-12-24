# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/database.py
# Compiled at: 2015-10-12 04:11:24
# Size of source mod 2**32: 2147 bytes
import sys, logging, copy, shelve
from threading import Lock
from . import config
from .chain.message import Message
logger = logging.getLogger(config.APP_NAME)

class Database:

    def __init__(self, f):
        self.shelve = shelve.open(f)

    def close(self):
        self.shelve.close()

    def sync(self):
        self.shelve.sync()

    def new(path):
        return Database(path)

    def _exists(self, key):
        return key in self.shelve

    def _delete(self, key):
        del self.shelve[key]

    def _get(self, key):
        if key in self.shelve:
            return self.shelve[key]
        else:
            return

    def _set(self, key, dictobj):
        self.shelve[key] = dictobj

    def exists(self, key):
        return self._exists(key)

    def get(self, key):
        return self._get(key)

    def set(self, key, dictobj):
        self._set(key, dictobj)
        self.sync()

    def delete(self, key):
        if self.exists(key):
            self._delete(key)
            self.sync()

    def intinc(self, key):
        self.set(key, int(self.get(key)) + 1)

    def intdec(self, key):
        self.set(key, int(self.get(key)) + 1)

    def listappend(self, key, data):
        d = self.get(key)
        d.append(data)
        self.set(key, d)

    def listremove(self, key, data):
        li = self.get(key)
        li.remove(data)
        self.set(key, li)

    def listcontains(self, key, data):
        return data in self.get(key)

    def getinit(self, key, dictobj):
        if not self.exists(key):
            self.set(key, dictobj)
            return dictobj
        else:
            return self.get(key)

    def init(self, key, dictobj):
        if not self.exists(key):
            self.set(key, dictobj)