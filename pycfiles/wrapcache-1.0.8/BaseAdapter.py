# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\dev_ws\wrapcache\wrapcache\adapter\BaseAdapter.py
# Compiled at: 2016-01-03 22:41:22
"""
Base cache Adapter object.
"""

class BaseAdapter(object):
    db = None

    def __init__(self, timeout=-1):
        self.timeout = timeout

    def get(self, key):
        raise NotImplementedError()

    def set(self, key, value):
        raise NotImplementedError()

    def remove(self, key):
        raise NotImplementedError()

    def flush(self):
        raise NotImplementedError()