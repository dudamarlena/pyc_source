# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\actions\action_pause.py
# Compiled at: 2009-02-02 02:43:30
"""
Pause action -- wait for a specific amount of time
============================================================================

"""
import time
from dragonfly.actions.action_base import DynStrActionBase

class Pause(DynStrActionBase):
    """
        Pause for the given amount of time.

        The *spec* constructor argument should be a *string* giving the 
        time to wait.  It should be given in hundredths of a second.  For 
        example, the following code will pause for 20/100s = 0.2
        seconds: ::

            Pause("20").execute()

        The reason the *spec* must be given as a *string* is because it 
        can then be used in dynamic value evaluation.  For example, the 
        following code determines the time to pause at execution time: ::

            action = Pause("%(time)d")
            data = {"time": 37}
            action.execute(data)

    """

    def _parse_spec(self, spec):
        interval = float(spec) / 100
        return interval

    def _execute_events(self, interval):
        time.sleep(interval)
        return True