# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/output.py
# Compiled at: 2012-07-13 05:36:14
from mole.event import Event
from mole.action import Action, ActionSyntaxError
from mole.output import Output

class ActionOutput(Action):
    """This action get events in pipeline and return a string output.

    :param `type`: a list with string representation of the output to be loaded.
    """
    REQUIRE_PLOTTER = True

    def __init__(self, type=[
 'basic'], *args, **kwargs):
        if len(type) > 1:
            raise ActionSyntaxError('output command only allow one single parameter')
        self.type = Output.from_type(type[0], *args, **kwargs)

    def __call__(self, pipeline):
        return self.type(pipeline)