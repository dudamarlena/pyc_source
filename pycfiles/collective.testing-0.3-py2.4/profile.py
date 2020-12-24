# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/collective/testing/profile.py
# Compiled at: 2007-04-17 11:47:01
from test import pystone
import hotshot, time, timeit

def local_pystone():
    return pystone.pystones(loops=pystone.LOOPS)


REPORT = {}
current_pystone = local_pystone()

def timer(f):

    def timedf(*args, **kw):
        start_time = time.time()
        try:
            return f(*args, **kw)
        finally:
            total_time = time.time() - start_time
            pystone_rate = current_pystone[0] / current_pystone[1]
            pystone_total_time = total_time / pystone_rate
            REPORT[f.__name__] = pystone_total_time

    return timedf


class profile(object):
    """ fname == profile file """
    __module__ = __name__

    def __init__(self, fname, signature=lambda *a, **kw: True):
        self.prof = hotshot.Profile(fname)
        self.signature = signature

    def __call__(self, func):

        def wrapprofiler(*args, **kwargs):
            if not hasattr(self, '_hasrun') and self.signature(*args, **kwargs):
                try:
                    return self.prof.runcall(func, *args, **kwargs)
                finally:
                    self.prof.close()
                    self._hasrun = True
            else:
                return func(*args, **kwargs)

        return wrapprofiler


class BestOf(object):
    """
    based on chrism's profiling madness

    This class takes a number of loops to run over a callable and on call returns
    a wrapper that times the original function

    @return dict(message="pretty print out times",
                 raw="pystone best result")
    """
    __module__ = __name__

    def __init__(self, howmany):
        self.howmany = howmany

    def timeit(self, func):
        t = timeit.Timer('func(*cargs, **ckw)', 'from __main__ import %s as func; from __main__ import cargs, ckw' % func.__name__)
        repeat = self.howmany
        number = self.howmany
        result = t.repeat(repeat, 1)
        best = min(result)
        usec = best * 1000000.0 / number
        msec = usec / 1000
        pystone_rate = current_pystone[0] / current_pystone[1]
        pystone_total_time = best / pystone_rate
        return dict(message='%.*g msec per loop' % (8, msec), pystone=pystone_total_time)