# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/utils/timezone.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
import datetime
from django.conf import settings
try:
    from django.utils import timezone

    def make_aware(value):
        if getattr(settings, b'USE_TZ', False) and timezone.is_naive(value):
            default_tz = timezone.get_default_timezone()
            value = timezone.make_aware(value, default_tz)
        return value


    def make_naive(value):
        if getattr(settings, b'USE_TZ', False) and timezone.is_aware(value):
            default_tz = timezone.get_default_timezone()
            value = timezone.make_naive(value, default_tz)
        return value


    def now():
        d = timezone.now()
        if d.tzinfo:
            return timezone.localtime(timezone.now())
        return d


except ImportError:
    now = datetime.datetime.now
    make_aware = make_naive = lambda x: x

def aware_date(*args, **kwargs):
    return make_aware(datetime.date(*args, **kwargs))


def aware_datetime(*args, **kwargs):
    return make_aware(datetime.datetime(*args, **kwargs))