# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/utils/datetime_utils.py
# Compiled at: 2018-07-11 18:15:31
from datetime import *
import django
from django.conf import settings
if django.VERSION[:2] >= (1, 4) and getattr(settings, 'USE_TZ', False):
    from django.utils import timezone
    from datetime import datetime as _datetime

    class datetime(_datetime):
        """
        A custom datetime.datetime class which acts as a compatibility
        layer between South and Django 1.4's timezone aware datetime
        instances.

        It basically adds the default timezone (as configured in Django's
        settings) automatically if no tzinfo is given.
        """

        def __new__(cls, year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
            dt = _datetime(year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo)
            if tzinfo is None:
                default_timezone = timezone.get_default_timezone()
                dt = timezone.make_aware(dt, default_timezone)
            return dt