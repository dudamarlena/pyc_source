# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/rename.py
# Compiled at: 2012-07-13 05:36:56
from mole.event import Event
from mole.action import Action, ActionSyntaxError

class ActionRename(Action):
    """This action rename a field.

    :param `field`: the field name to be renamed.
    :param `newname`: the new name to be used for this field
    """
    REQUIRE_PARSER = True

    def __init__(self, field, newname):
        self.field = field[0]
        self.newname = newname[0]

    def __call__(self, pipeline):
        for event in pipeline:
            if self.field in event:
                _value = event[self.field]
                event[self.newname] = _value
                del event[self.field]
            yield event