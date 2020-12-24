# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pytrack_analysis/benchmark.py
# Compiled at: 2017-07-25 11:31:15
# Size of source mod 2**32: 2138 bytes
from timeit import default_timer as timer
import numpy as np

class benchmark(object):

    def __init__(self, msg, fmt='%0.9g'):
        """
        Creates benchmark test object with message msg and format fmt

        args:
        * msg [str] : message for the print-out (e.g.: "Performed test XXX in")
        kwargs:
        * fmt [str] : string formatter for time (default: decimal precision to ns)
        return:
        * None
        """
        self.msg = msg
        self.fmt = fmt

    def __enter__(self):
        """ Starts default timer """
        self.start = timer()
        return self

    def __exit__(self, *args):
        """ Stops timer and prints message and times in given format """
        t = timer() - self.start
        if len(self.msg) > 0:
            print(('%s : ' + self.fmt + ' seconds') % (self.msg, t))
        self.time = t


class multibench(object):
    __doc__ = '\n    Creates multiple (times) benchmark tests object with message msg and format fmt\n\n    kwargs:\n    * times [int] : number of times\n    * msg [str] : message for the print-out (e.g.: "Performed test XXX in"); note that _SILENT may overwrite this option\n    * fmt [str] : string formatter for time (default: decimal precision to ns)\n    * SILENT [bool] : option for silenced tests (no individual printouts)\n    '

    def __init__(self, times=1, msg='', fmt='%0.9g', SILENT=True):
        print('Starting benchmark:')
        if not SILENT:
            self.msg = msg
        else:
            self.msg = ''
            self.t = np.zeros(times)

    def __call__(self, f):
        self.f = f
        for i, thistime in enumerate(self.t):
            with benchmark(self.msg) as (result):
                self.f()
            self.t[i] = result.time

    def __del__(self):
        print('Test {:} for {:} repititions. Total time: {:} s. Avg: {:} s. Max: {:} s.'.format(self.f.__name__, len(self.t), np.sum(self.t), np.mean(self.t), np.max(self.t)))