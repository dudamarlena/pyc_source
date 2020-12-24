# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/sort.py
# Compiled at: 2012-07-13 05:39:28
from mole.event import Event
from mole.action import Action, ActionSyntaxError
sort_asc = lambda x, y: cmp(x, y)
sort_des = lambda x, y: cmp(y, x)

class ActionSort(Action):
    """This action sort values in pipeline.

    :param `fields`: a :class:`list` with the fields names to used as
        sort key.
    """
    REQUIRE_PARSER = True

    def __init__(self, fields):
        self.fields = fields
        if self.fields is None:
            raise ActionSyntaxError('No fields provided')
        return

    def _sort(self, evx, evy):
        for field in self.fields:
            if field[0] == '-':
                field = field[1:]
                sfunc = sort_des
            else:
                sfunc = sort_asc
            if evx[field] and not evy[field]:
                return -1
            if not evx[field] and evy[field]:
                return 1
            if evx[field] == evy[field]:
                continue
            return sfunc(evx[field], evy[field])

        return 0

    def __call__(self, pipeline):
        return sorted(pipeline, self._sort)