# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/parser.py
# Compiled at: 2012-10-06 13:42:16
from mole.event import Event
from mole.action import Action, ActionSyntaxError
from mole.parser import Parser

class ActionParser(Parser):
    """This action parse the pipeline using specific parser

    :param `name`: a list with string representation of the parser to be loaded.
    """

    def __init__(self, name, *args, **kwargs):
        if len(name) > 1:
            raise ActionSyntaxError('parser command only allow one single parameter')
        self.item = None
        self.name = name[0]
        return

    def _init_item(self):
        if self.item is None:
            if self.context:
                self.item = self.context[self.name].parser
            else:
                self.item = []
        return

    def __iter__(self):
        return iter(self.item)

    def __call__(self, pipeline):
        self._init_item()
        return self.item(pipeline)

    def get_object(self):
        return self.context[self.name]