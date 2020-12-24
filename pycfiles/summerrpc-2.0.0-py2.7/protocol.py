# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/protocol.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'Protocol']
__authors__ = ['Tim Chow']
from .filter import Filter
from .invoker import Invoker

class Protocol(object):

    def __init__(self):
        self._filters = []
        self._invoker = None
        return

    def add_filter(self, filter):
        if not isinstance(filter, Filter):
            raise TypeError('expect Filter, not %s' % type(filter).__name__)
        self._filters.append(filter)
        return self

    def set_invoker(self, invoker):
        if not isinstance(invoker, Invoker):
            raise TypeError('expect Invoker, not %s' % type(invoker).__name__)
        self._invoker = invoker
        return self

    def invoke(self, request, connection, serializer, write_timeout, read_timeout):
        filters = sorted(self._filters, key=lambda f: f.get_order(), reverse=True)
        for filter in filters:
            filter.filter(request)

        return self._invoker.invoke(request, connection, serializer, write_timeout, read_timeout)