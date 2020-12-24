# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/alertapi30/alert.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2441 bytes
from pyowm.utils import timeformatutils, stringutils

class AlertChannel:
    """AlertChannel"""

    def __init__(self, name):
        self.name = name


class Alert:
    """Alert"""

    def __init__(self, id, trigger_id, met_conditions, coordinates, last_update=None):
        assert id is not None
        assert isinstance(id, str), 'Value must be a string'
        self.id = id
        assert trigger_id is not None
        assert isinstance(trigger_id, str), 'Value must be a string'
        self.trigger_id = trigger_id
        assert met_conditions is not None
        assert isinstance(met_conditions, list)
        self.met_conditions = met_conditions
        assert coordinates is not None
        assert isinstance(coordinates, dict)
        self.coordinates = coordinates
        if last_update is not None:
            assert isinstance(last_update, int)
        self.last_update = last_update

    def __repr__(self):
        return '<%s.%s - id=%s, trigger id=%s, last update=%s>' % (
         __name__,
         self.__class__.__name__,
         self.id,
         self.trigger_id,
         timeformatutils.to_ISO8601(self.last_update))