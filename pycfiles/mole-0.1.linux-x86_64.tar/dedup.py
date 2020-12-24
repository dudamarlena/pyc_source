# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/dedup.py
# Compiled at: 2012-07-13 05:31:33
from mole.event import Event
from mole.action import Action, ActionSyntaxError

class ActionDedup(Action):
    """This action dedup(licate) values in pipeline.

    :param `fields`: a list of fields to be dedup(licate)
    """
    REQUIRE_PLOTTER = True

    def __init__(self, fields=[
 '_raw']):
        self.fields = fields
        self._field = None
        if len(self.fields) == 1 and self.fields[0] == '_raw':
            self._field = True
        else:
            self.REQUIRE_PARSER = True
        return

    def __call__(self, pipeline):
        last = []
        for event in pipeline:
            if self._field:
                if last and last == event:
                    continue
                else:
                    last = event
                    yield event
            elif event.has_all(self.fields):
                field_values = map(lambda x: (x, event[x]), self.fields)
                if field_values in last:
                    continue
                else:
                    last.append(field_values)
                    yield event