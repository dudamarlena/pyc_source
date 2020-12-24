# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/similarity/backends/abstract.py
# Compiled at: 2019-08-16 12:27:41
from __future__ import absolute_import
from abc import ABCMeta, abstractmethod
import six

@six.add_metaclass(ABCMeta)
class AbstractIndexBackend(object):

    @abstractmethod
    def classify(self, scope, items, limit=None, timestamp=None):
        pass

    @abstractmethod
    def compare(self, scope, key, items, limit=None, timestamp=None):
        pass

    @abstractmethod
    def record(self, scope, key, items, timestamp=None):
        pass

    @abstractmethod
    def merge(self, scope, destination, items, timestamp=None):
        pass

    @abstractmethod
    def delete(self, scope, items, timestamp=None):
        pass

    @abstractmethod
    def scan(self, scope, indices, batch=1000, timestamp=None):
        pass

    @abstractmethod
    def flush(self, scope, indices, batch=1000, timestamp=None):
        pass

    @abstractmethod
    def export(self, scope, items, timestamp=None):
        pass

    @abstractmethod
    def import_(self, scope, items, timestamp=None):
        pass