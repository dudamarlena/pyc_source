# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/stats.py
# Compiled at: 2018-10-08 11:55:52
# Size of source mod 2**32: 3966 bytes
from __future__ import absolute_import, division, print_function, with_statement
from functools import wraps
import time
from greplin import scales
from greplin.scales.meter import MeterStat
from tornado.concurrent import Future
from supercell.requesthandler import RequestHandler

def latency(fn):
    """Measure execution latency of a certain request method.

    In order to measure latency for GET requests of a request handler you
    simply have to add the :func:`latency` decorator to the declaration::

        @s.latency
        @s.async
        def get(self, *args, **kwargs):
            ...

    The latency is recorded along the request path, i.e. if the request handler
    is defined like this::

        env.add_handler('/test/this', LatencyExample)

    the latency of GET/POST/PUT etc methods are stored with the path. In order
    to access the stats you may call **/_system/stats/test/this** or
    **/_system/stats/test**, e.g.
    """

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self.__class__, '_stats_latency'):
            self.__class__._stats_latency = scales.NamedPmfDictStat('latency')
        if isinstance(self, RequestHandler):
            original_on_finish = self.on_finish

            def latency_on_finish(*args, **kwargs):
                latency = time.time() - start
                self._stats_latency[fn.__name__].addValue(latency)
                original_on_finish(*args, **kwargs)

            self.on_finish = latency_on_finish
            scales.init(self, self.request.path)
            start = time.time()
            return fn(self, *args, **kwargs)
        else:

            def done_callback(*args, **kwargs):
                latency = time.time() - start
                self._stats_latency[fn.__name__].addValue(latency)

            scales.init(self, '/'.join(['_internal', self.__module__,
             self.__class__.__name__]))
            start = time.time()
            result = fn(self, *args, **kwargs)
            if isinstance(result, Future):
                result.add_done_callback(done_callback)
            else:
                done_callback()
            return result

    return wrapper


def metered(fn):
    """Meter the execution of certain requests.

    The :func:`metered` stats will measure the 1/5/15 minutes averages for
    requests. This is also applied trivially::

        @s.metered
        @s.async
        def get(self, *args, **kwargs):
            ...

    As with the :func:`latency` stats, the :func:`metered` stats are recorded
    along the request path, i.e. you can get the stats values using the
    **/_system/stats/** route.
    """

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        attr_name = '_stats_metered_%s' % fn.__name__
        if not hasattr(self.__class__, '_stats_metered'):
            setattr(self.__class__, attr_name, MeterStat(fn.__name__))
        else:
            if isinstance(self, RequestHandler):
                scales.init(self, self.request.path)
            else:
                scales.init(self, '/'.join(['_internal', self.__module__,
                 self.__class__.__name__]))
        getattr(self, attr_name).mark()
        return fn(self, *args, **kwargs)

    return wrapper