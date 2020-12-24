# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/period.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 742 bytes
from __future__ import unicode_literals
from datetime import timedelta
from .date import Date
from ...util import utcnow, datetime_period
from ....schema import Attribute

class Period(Date):
    __doc__ = 'A specialized Date field used to store dates rounded down to the start of a given period.'
    hours = Attribute(default=None)
    minutes = Attribute(default=None)
    seconds = Attribute(default=None)

    @property
    def delta(self):
        return timedelta(hours=(self.hours or 0), minutes=(self.minutes or 0), seconds=(self.seconds or 0))

    def to_foreign(self, obj, name, value):
        value = super(Period, self).to_foreign(obj, name, value)
        return datetime_period(value, hours=(self.hours), minutes=(self.minutes), seconds=(self.seconds))