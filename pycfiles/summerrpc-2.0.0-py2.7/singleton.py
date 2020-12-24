# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/helper/singleton.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'Singleton']
__authors__ = ['Tim Chow']
import threading

class Singleton(object):
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, *a, **kw):
        if cls in Singleton._instances:
            return Singleton._instances[cls]
        with Singleton._lock:
            if cls in Singleton._instances:
                return Singleton._instances[cls]
            else:
                instance = super(Singleton, cls).__new__(cls, *a, **kw)
                Singleton._instances[cls] = instance
                return instance