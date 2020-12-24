# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/head.py
# Compiled at: 2012-07-13 05:34:14
from mole.event import Event
from mole.action import Action, ActionSyntaxError

class ActionHead(Action):
    """This action get the head values in pipeline.

    :param `num`: a :class:`list` with the number of lines to expose in
            pipeline.
    """
    REQUIRE_PLOTTER = True

    def __init__(self, num=[
 10]):
        self.num = int(num[0])
        if self.num is None:
            raise ActionSyntaxError('No head limit provided')
        return

    def __call__(self, pipeline):
        for event in pipeline:
            if self.num:
                yield event
                self.num -= 1
            else:
                break