# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sunguangran/code/gitlab/sgran/pyapollo/pyapollo/cache/basecache.py
# Compiled at: 2018-08-11 06:16:42
import abc
from six import with_metaclass

class BaseCache(with_metaclass(abc.ABCMeta, object)):

    def __init__(self):
        pass

    def refresh(self, namespace, value):
        raise NotImplementedError('')

    def exists(self, namespace):
        raise NotImplementedError('')

    def load(self, namespace, default=None):
        raise NotImplementedError('')

    def delete(self, namespace):
        raise NotImplementedError('')

    def clear(self):
        raise NotImplementedError('')