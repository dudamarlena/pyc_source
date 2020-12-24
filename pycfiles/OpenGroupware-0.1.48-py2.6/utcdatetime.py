# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/utcdatetime.py
# Compiled at: 2012-10-12 07:02:39
from datetime import tzinfo, timedelta
import sqlalchemy as sqla

class UniversalTimeZone(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'UTC'

    def dst(self, dt):
        return timedelta(0)


class UTCDateTime(sqla.types.TypeDecorator):
    impl = sqla.types.DateTime

    def convert_bind_param(self, value, engine):
        return value

    def convert_result_value(self, value, engine):
        if value is None:
            return
        else:
            return value.replace(tzinfo=UniversalTimeZone())