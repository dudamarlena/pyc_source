# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/transaction.py
# Compiled at: 2012-07-12 07:39:57
from mole.event import Event
from mole.action import Action, ActionSyntaxError
from mole.helper.timeformat import Timespan

class ActionTransaction(Action):
    """This action merge events in a transaction defined by field or another
    expresion."""
    REQUIRE_PARSER = True

    def __init__(self, fields=[], startswith=[''], endswith=[''], maxevents=[
 10000], maxspan=[None]):
        """Create a new transaction action.

        :param `fields`: a :class:`list` which contains the fields to make
            the transaction.
        :param `startsWith`: a string to be used to find the beginning of
            the transaction.
        :param `endsWith`: a string to be used to find the end of the
            transaction.
        """
        self.fields = fields
        self.startswith = startswith[0]
        self.endswith = endswith[0]
        self.maxspan = Timespan(maxspan[0]) if maxspan[0] else None
        self.maxevents = int(maxevents[0])
        if not self.fields:
            raise ActionSyntaxError('No fields provided')
        return

    def __call__(self, pipeline):
        ret = []
        for event in pipeline:
            if len(self.fields) == len(filter(lambda x: x in event, self.fields)):
                if len(ret) >= self.maxevents:
                    yield Event.merge(ret)
                    ret = [event]
                elif self.startswith and event._raw.startswith(self.startswith):
                    yield Event.merge(ret)
                    ret = [event]
                elif self.endswith and event._raw.endswith(self.endswith):
                    ret.append(event)
                    yield Event.merge(ret)
                elif self.maxspan and len(ret) and event.time - ret[0].time > self.maxspan.seconds:
                    yield Event.merge(ret)
                    ret = [event]
                else:
                    ret.append(event)

        if ret:
            yield Event.merge(ret)