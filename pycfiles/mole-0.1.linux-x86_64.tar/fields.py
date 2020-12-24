# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/fields.py
# Compiled at: 2012-07-13 05:33:56
from mole.event import Event
from mole.action import Action

class ActionFields(Action):
    """This action return only a subset of the specified fields.

    :param `fields`: a :class:`list` of fields to be included
        in output.
    """
    REQUIRE_PARSER = True

    def __init__(self, fields=[]):
        self.fields = fields

    def __call__(self, pipeline):
        for event in pipeline:
            new_event = Event()
            for field in self.fields:
                if field in event:
                    new_event[field] = event[field]
                    yield new_event