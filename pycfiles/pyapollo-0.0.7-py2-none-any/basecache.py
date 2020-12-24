# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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