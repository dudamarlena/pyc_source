# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mico/lib/python2.7/site-packages/mico/util/mutex.py
# Compiled at: 2013-05-03 06:34:17
from threading import Lock

class Mutex(object):
    _current_mutex = {}

    def __init__(self, name):
        self._lock = Lock()
        self.name = name

    @classmethod
    def get_mutex(cls, name='_default'):
        if name not in Mutex._current_mutex:
            Mutex._current_mutex[name] = Mutex(name)
        return Mutex._current_mutex[name]

    def __del__(self):
        Lock.__del__(self)
        if self.name in Mutex._current_mutex:
            del Mutex._current_mutex[self.name]

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, typ, value, traceback):
        return self._lock.__exit__()