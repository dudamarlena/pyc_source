# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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