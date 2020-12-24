# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/utils/timezone.py
# Compiled at: 2018-03-26 19:55:30
# Size of source mod 2**32: 1000 bytes
from django.conf import settings
from django.utils.timezone import make_naive, make_aware, is_naive, is_aware, localtime

def ensure_timezone(dateTime, timeZone=None):
    """
    Since this project is designed to be used in both time-zone aware
    and naive environments, this utility just returns a datetime as either
    aware or naive depending on whether time zone support is enabled.
    """
    if is_aware(dateTime) and not getattr(settings, 'USE_TZ', False):
        return make_naive(dateTime, timezone=timeZone)
    if is_naive(dateTime) and getattr(settings, 'USE_TZ', False):
        return make_aware(dateTime, timezone=timeZone)
    return dateTime


def ensure_localtime(dateTime):
    if not getattr(settings, 'USE_TZ', False):
        if is_aware(dateTime):
            return make_naive(dateTime)
        return dateTime
    else:
        return localtime(make_aware(dateTime) if is_naive(dateTime) else dateTime)