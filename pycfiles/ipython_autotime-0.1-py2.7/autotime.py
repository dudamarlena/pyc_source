# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/autotime.py
# Compiled at: 2016-01-13 07:49:14
from __future__ import print_function
import time
from IPython.core.magics.execution import _format_time as format_delta

class LineWatcher(object):
    """Class that implements a basic timer.

    Notes
    -----
    * Register the `start` and `stop` methods with the IPython events API.
    """

    def __init__(self):
        self.start_time = 0.0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time:
            diff = time.time() - self.start_time
            assert diff > 0
            print('time: %s' % format_delta(diff))


timer = LineWatcher()

def load_ipython_extension(ip):
    ip.events.register('pre_run_cell', timer.start)
    ip.events.register('post_run_cell', timer.stop)


def unload_ipython_extension(ip):
    ip.events.unregister('pre_run_cell', timer.start)
    ip.events.unregister('post_run_cell', timer.stop)