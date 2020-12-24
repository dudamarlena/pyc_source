# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/process/time_dict.py
# Compiled at: 2012-06-14 10:29:18
"""
Wrapper class over standard dictionary
"""
from ordereddict import OrderedDict
from botnee import debug
import botnee_config

class TimeDict(OrderedDict):

    def __init__(self, start_time=None):
        OrderedDict.__init__(self)
        self.start_time = start_time

    def write_csv(self, verbose=False, logger=None):
        with debug.Timer(None, None, verbose, logger):
            if not self.start_time:
                return
            fname = botnee_config.LOG_DIRECTORY + 'time_dict_' + self.start_time + '.csv'
            debug.write_csv(fname, [ (k, v) for (k, v) in self.items() ])
        return