# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/utils/timezone.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 261 bytes
from datetime import datetime
import pytz
from rest_framework.conf import settings
utc = pytz.utc

def now():
    now_time = datetime.now(tz=utc)
    to_zone = pytz.timezone(settings.TIME_ZONE)
    return now_time.astimezone(to_zone)