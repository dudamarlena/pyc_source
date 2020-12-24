# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/input.py
# Compiled at: 2012-07-13 05:36:23
from mole.event import Event
from mole.action import Action, ActionSyntaxError
from mole.input import Input

class ActionInput(Action):
    """This action puts events in pipeline from a declared input.

    :param `name`: a list with string representation of the input to be loaded.
    """

    def __init__(self, name, *args, **kwargs):
        if len(name) > 1:
            raise ActionSyntaxError('input command only allow one single parameter')
        self.item = None
        self.name = name[0]
        return

    def _init_item(self):
        if self.item is None:
            if self.context:
                self.item = self.context[self.name].index
            else:
                self.item = []
        return

    def __iter__(self):
        self._init_item()
        return iter(self.item)

    def __call__(self, pipeline):
        return iter(self)

    def get_object(self):
        return self.context[self.name]