# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/uniq.py
# Compiled at: 2012-06-28 06:14:39
from mole.event import Event
from mole.action import Action, ActionSyntaxError

class ActionUniq(Action):
    """This action get the uniq values in pipeline."""
    REQUIRE_PLOTTER = True

    def __init__(self, fields=[
 '_raw']):
        """Create a new uniq action.

        :param `fields`: a list of fields to be uniq
        """
        self.fields = fields
        self._field = None
        if len(self.fields) == 1 and self.fields[0] == '_raw':
            self._field = True
        else:
            self.REQUIRE_PARSER = True
        return

    def __call__(self, pipeline):
        last = None
        for event in pipeline:
            if self._field:
                if last and last == event:
                    continue
                else:
                    last = event
                    yield event
            elif event.has_all(self.fields):
                field_values = map(lambda x: (x, event[x]), self.fields)
                if last == field_values:
                    continue
                else:
                    last = field_values
                    yield event

        return