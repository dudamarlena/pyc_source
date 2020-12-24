# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/date.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 3605 bytes
"""Marrow Mongo Date field specialization.

Commentary on high-level management of timezone casting:

        https://groups.google.com/forum/#!topic/mongodb-user/GOMjTJON4cg
"""
from __future__ import unicode_literals
from datetime import datetime, timedelta, tzinfo
from bson import ObjectId as OID
from collections import MutableMapping
from datetime import datetime, timedelta
from .base import Field
from ...util import utc, utcnow
from ....schema import Attribute
try:
    from pytz import timezone as get_tz
except ImportError:
    get_tz = None

try:
    localtz = __import__('tzlocal').get_localzone()
except ImportError:
    localtz = None

log = __import__('logging').getLogger(__name__)

class Date(Field):
    __doc__ = 'MongoDB date/time storage.\n\t\n\tAccepts the following options in addition to the base Field options:\n\t\n\t`naive`: The timezone to interpret assigned "naive" datetime objects as.\n\t`timezone`: The timezone to cast objects retrieved from the database to.\n\t\n\tTimezone references may be, or may be a callback returning, a `tzinfo`-suitable object, the string name of a\n\ttimezone according to `pytz`, the alias \'naive\' (strip or ignore the timezone) or \'local\' (the local host\'s)\n\ttimezone explicitly. None values imply no conversion.\n\t\n\tAll dates are converted to and stored in UTC for storage within MongoDB; the original timezone is lost. As a\n\tresult if `naive` is `None` then assignment of naive `datetime` objects will fail.\n\t'
    __foreign__ = 'date'
    __disallowed_operators__ = {'#array'}
    naive = Attribute(default=utc)
    tz = Attribute(default=None)

    def _process_tz(self, dt, naive, tz):
        """Process timezone casting and conversion."""

        def _tz(t):
            if t in (None, 'naive'):
                return t
            else:
                if t == 'local':
                    if __debug__:
                        if not localtz:
                            raise ValueError('Requested conversion to local timezone, but `localtz` not installed.')
                    t = localtz
                else:
                    if not isinstance(t, tzinfo):
                        if __debug__:
                            if not localtz:
                                raise ValueError('The `pytz` package must be installed to look up timezone: ' + repr(t))
                        t = get_tz(t)
                    if not hasattr(t, 'normalize'):
                        if get_tz:
                            t = get_tz(t.tzname(dt))
                return t

        naive = _tz(naive)
        tz = _tz(tz)
        if not dt.tzinfo:
            if naive:
                if hasattr(naive, 'localize'):
                    dt = naive.localize(dt)
                else:
                    dt = dt.replace(tzinfo=naive)
            return tz or dt
        else:
            if hasattr(tz, 'normalize'):
                dt = tz.normalize(dt.astimezone(tz))
            else:
                if tz == 'naive':
                    dt = dt.replace(tzinfo=None)
                else:
                    dt = dt.astimezone(tz)
            return dt

    def to_native(self, obj, name, value):
        if not isinstance(value, datetime):
            log.warning(('Non-date stored in {}.{} field.'.format(self.__class__.__name__, self.__name__)), extra={'document':obj, 
             'field':self.__name__,  'value':value})
            return value
        else:
            return self._process_tz(value, self.naive, self.tz)

    def to_foreign(self, obj, name, value):
        if isinstance(value, MutableMapping):
            if '_id' in value:
                value = value['_id']
        if isinstance(value, OID):
            value = value.generation_time
        else:
            if isinstance(value, timedelta):
                value = utcnow() + value
        if not isinstance(value, datetime):
            raise ValueError('Value must be a datetime, ObjectId, or identified document, not: ' + repr(value))
        return self._process_tz(value, self.naive, utc)