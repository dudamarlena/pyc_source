# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/min.py
# Compiled at: 2012-07-13 05:35:33
from mole.event import Event
from mole.action import Action, ActionSyntaxError

class ActionMin(Action):
    """This action get the min value item in pipeline.

    :param `fields`: a :class:`list` with fields to get min value.
    :param `groups`: a :class:`list` which provides the items to group
        results.
    """
    REQUIRE_PARSER = True

    def __init__(self, fields=[], groups=[]):
        self.fields = fields
        self.groups = groups
        if not self.fields:
            raise ActionSyntaxError('No fields provided')

    def __call__(self, pipeline):
        response = {}
        for event in pipeline:
            if self.groups:
                for group in self.groups:
                    if group in event:
                        _key = (
                         group, event[group])
                        if _key not in response:
                            response[_key] = {}
                        for field in self.fields:
                            _x = response[_key]
                            if _x.get(field, None):
                                _x[field] = min(_x[field], event[field])
                            else:
                                _x[field] = event[field]

            else:
                for field in self.fields:
                    if response.get(field, None):
                        response[field] = min(response[field], event[field])
                    else:
                        response[field] = event[field]

        if self.groups:
            for gkey, gval in response:
                for f in response[(gkey, gval)]:
                    yield Event({gkey: gval, 'min(%s)' % f: response[(gkey, gval)][f]})

        else:
            for key in response:
                yield Event({'min(%s)' % key: response[key]})

        return