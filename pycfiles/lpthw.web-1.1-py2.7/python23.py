# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/web/python23.py
# Compiled at: 2011-06-21 16:54:55
"""Python 2.3 compatabilty"""
import threading

class threadlocal(object):
    """Implementation of threading.local for python2.3.
    """

    def __getattribute__(self, name):
        if name == '__dict__':
            return threadlocal._getd(self)
        if name.startswith('__'):
            return object.__getattribute__(self, name)
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError, name

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __delattr__(self, name):
        try:
            del self.__dict__[name]
        except KeyError:
            raise AttributeError, name

    def _getd(self):
        t = threading.currentThread()
        if not hasattr(t, '_d'):
            t._d = {}
        _id = id(self)
        if _id not in t._d:
            t._d[_id] = {}
        return t._d[_id]


if __name__ == '__main__':
    d = threadlocal()
    d.x = 1
    print d.__dict__
    print d.x