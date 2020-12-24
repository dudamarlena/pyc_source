# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dependencyinjection\internal\lock.py
# Compiled at: 2017-12-17 06:31:51
# Size of source mod 2**32: 481 bytes
import threading
from .common import ILock

class ThreadLock(ILock):

    def __init__(self):
        self._lock = threading.RLock()

    def __enter__(self):
        self._lock.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._lock.__exit__(exc_type, exc_value, traceback)