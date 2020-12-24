# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/profiler.py
# Compiled at: 2020-05-13 19:28:40
# Size of source mod 2**32: 2508 bytes
"""
Utility methods related to profile Python code
"""
from __future__ import print_function, division, absolute_import
import time, pstats, cProfile as profile
from functools import wraps
from collections import defaultdict

def profile_function(sort_key='time', rows=30):

    def _(fn):

        @wraps(_)
        def __(*fargs, **fkwargs):
            prof = profile.Profile()
            ret = (prof.runcall)(f, *fargs, **fkwargs)
            pstats.Stats(prof).strip_dirs().sort_stats(sort_key).print_stats(rows)
            return ret

        return __

    return _


class LapCounter:
    LapTimes = 0
    LapList = list()

    def __init__(self):
        current_time = time.time()
        self._all_start = current_time
        self._start = current_time
        self._end = current_time

    def count(self, string=''):
        self._end = time.time()
        lap_str = ('lap_time : ', string, self.LapTimes, ':', self._end - self._start)
        self.LapList.append(lap_str)
        self.LapTimes += 1
        self._start = time.time()

    def lap_print(self, print_flag=True, window=None):
        total_time = time.time() - self._all_start
        if window:
            out_time = '{:.5f}'.format(total_time)
            try:
                window.time_label.setText('- Calculation Time - ' + out_time + ' sec')
            except Exception as e:
                pass

        if print_flag:
            print('----------------------------------')
            for lap_time in self.LapList:
                print(lap_time)

            print('Total time : {}'.format(total_time))

    def reset(self):
        self._all_start = time.time()
        self._start = time.time()
        self.LapList = list()


class IntegrationCounter:

    def __init__(self):
        current_time = time.time()
        self._all_start = current_time
        self._start = current_time
        self._end = current_time
        self._integration_dict = defaultdict(lambda : 0)

    def count(self, string=''):
        self._end = time.time()
        self._integration_dict[string] += self._end - self._start
        self._start = time.time()

    def integration_print(self):
        for string, integration in self._integration_dict.items():
            print('Integration time : ', string, integration)

    def reset(self):
        self._all_start = time.time()
        self._start = time.time()
        self._integration_dict = defaultdict(lambda : 0)