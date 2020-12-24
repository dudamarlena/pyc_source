# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/canoe/canoe.py
# Compiled at: 2013-01-13 00:25:24


def lift_iter(xs):
    if not xs:
        return []
    if hasattr(xs, '__iter__'):
        return xs
    return [xs]


class Canoe(object):

    def __init__(self, filters=None, route=None):
        self._filters = lift_iter(filters)
        self._route = route

    def send(self, line, buffer):
        for f in self._filters:
            nline, nbuffer = f(line, buffer)
            if nline is None or nbuffer is None:
                break

        if nline != None and nbuffer != None:
            if self._route:
                return self._route(line, buffer)
        return

    def add_filter(self, filter):
        self._filters.append(filters)

    def set_route(self, route):
        self._route = route