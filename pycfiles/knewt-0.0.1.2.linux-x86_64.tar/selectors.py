# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sven/0/_sdks/python/sven-2.7/lib/python2.7/site-packages/knewt/selectors.py
# Compiled at: 2017-11-11 11:20:00
from debug import Debug
d = Debug()
log = d.get_logger()

class Linker:

    def __init__(self):
        self._curr_ = None
        self._prev_ = None
        return

    def on(self, n, e, context):
        if e is None:
            return (n, e)
        else:
            if self._prev_ is None:
                self._prev_ = e[1]
            self._curr_ = e[1]
            edge = (self._prev_, self._curr_)
            self._prev_ = self._curr_
            if edge[0] == edge[1]:
                return (n, None)
            return (
             n, edge)


class RankNeighbours:

    def __init__(self):
        self._prev_ = None
        self._curr_ = None
        self._vertex_context_ = None
        return

    def on(self, n, e, context):
        if e is None:
            return (n, e)
        else:
            if self._vertex_context_ is None or self._vertex_context_ != n:
                self._vertex_context_ = n
                self._prev_ = None
            if self._prev_ is None:
                self._prev_ = n
            self._curr_ = e[1]
            log('vertex_context = %s' % self._vertex_context_)
            log('node=%s' % n)
            log('edge=%s' % str(e))
            log('prev=%s' % self._prev_)
            log('curr=%s' % self._curr_)
            edge = (
             self._prev_, self._curr_)
            log('new edge: %s' % str(edge))
            self._prev_ = self._curr_
            log('-------------------------------__')
            return (n, edge)