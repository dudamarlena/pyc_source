# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/whoosh/store.py
# Compiled at: 2015-06-30 06:52:38


class LockError(Exception):
    pass


class Storage(object):
    """Abstract base class for storage objects.
    """

    def create_index(self, schema, indexname=None):
        raise NotImplementedError

    def open_index(self, indexname=None, schema=None):
        raise NotImplementedError

    def close(self):
        pass

    def optimize(self):
        pass