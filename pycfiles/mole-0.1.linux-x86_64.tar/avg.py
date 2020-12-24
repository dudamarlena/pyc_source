# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/avg.py
# Compiled at: 2012-11-19 05:59:45
from mole.event import Event
from mole.action import Action, ActionSyntaxError

class ActionAvg(Action):
    """This action averages items in pipeline.

    :param `fields`: a :class:`list` with fields to be averaged in. If
        field is not present the line will be not averaged in.
    :param `groups`: a :class:`list` which provides the items to group
        average results.
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
                                _x[field]['count'] += 1
                                try:
                                    _x[field]['sum'] += float(event[field])
                                except ValueError:
                                    pass

                            else:
                                try:
                                    _x[field] = {'count': 1, 'sum': float(event[field])}
                                except ValueError:
                                    pass

            else:
                for field in self.fields:
                    if response.get(field, None):
                        response[field]['count'] += 1
                        try:
                            response[field]['sum'] += float(event[field])
                        except ValueError:
                            pass

                    else:
                        try:
                            response[field] = {'count': 1, 'sum': float(event[field])}
                        except ValueError:
                            response[field] = {'count': 1, 'sum': 0}

        if self.groups:
            for gkey, gval in response:
                for f in response[(gkey, gval)]:
                    r = response[(gkey, gval)][f]
                    yield Event({gkey: gval, 'avg(%s)' % f: r['sum'] / r['count']})

        else:
            for key in response:
                r = response[key]
                yield Event({'avg(%s)' % key: r['sum'] / r['count']})

        return