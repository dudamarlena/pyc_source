# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/timesearch.py
# Compiled at: 2012-10-07 06:03:29
from fnmatch import fnmatch
from mole.event import Event
from mole.action import Action, ActionSyntaxError
from mole.helper.timeformat import TimeFormat

class ActionTimesearch(Action):
    """This action filters pipeline due to time of events"""
    REQUIRE_PARSER = True

    def __init__(self, start=[
 0], stop=[None]):
        """Create a new timesearch action.

        :param `start`: the timeformat for start time point.
        :param `stop`: the timeformat for end time point.
        """
        if len(start) != 1 or len(stop) > 1:
            raise ActionSyntaxError('timesearch requires one parameter,  second one is optional')
        self.start = TimeFormat(start[0])
        if stop[0]:
            self.stop = TimeFormat(stop[0])
        else:
            self.stop = None
        return

    def __call__(self, pipeline):
        for event in pipeline:
            if event.time >= self.start:
                if self.stop:
                    if event.time <= self.stop:
                        yield event
                else:
                    yield event