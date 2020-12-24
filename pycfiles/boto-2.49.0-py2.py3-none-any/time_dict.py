# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/process/time_dict.py
# Compiled at: 2012-06-14 10:29:18
__doc__ = '\nWrapper class over standard dictionary\n'
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