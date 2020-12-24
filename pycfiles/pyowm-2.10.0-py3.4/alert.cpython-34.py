# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/alertapi30/alert.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2441 bytes
from pyowm.utils import timeformatutils, stringutils

class AlertChannel:
    __doc__ = '\n    Base class representing a channel through which one can acknowledge that a weather alert has been issued.\n    Examples: OWM API polling, push notifications, email notifications, etc.\n    This feature is yet to be implemented by the OWM API.\n    :param name: name of the channel\n    :type name: str\n    :returns: an *AlertChannel* instance\n\n    '

    def __init__(self, name):
        self.name = name


class Alert:
    __doc__ = '\n    Represents the situation happening when any of the conditions bound to a `Trigger` is met. Whenever this happens, an\n    `Alert` object is created (or updated) and is bound to its parent `Trigger`. The trigger can then be polled to check\n    what alerts have been fired on it.\n    :param id: unique alert identifier\n    :type name: str\n    :param trigger_id: link back to parent `Trigger`\n    :type trigger_id: str\n    :param met_conditions: list of dict, each one referring to a `Condition` obj bound to the parent `Trigger` and reporting\n    the actual measured values that made this `Alert` fire\n    :type met_conditions: list of dict\n    :param coordinates: dict representing the geocoordinates where the `Condition` triggering the `Alert` was met\n    :type coordinates: dict\n    :param last_update: epoch of the last time when this `Alert` has been fired\n    :type last_update: int\n\n    '

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