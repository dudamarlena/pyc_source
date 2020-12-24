# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/omphalos/render_timezone.py
# Compiled at: 2012-10-12 07:02:39
from dateutil.tz import gettz
from coils.core import *
from render_object import *

def render_timezone(code, ctx):
    utctime = ctx.get_utctime()
    for tz_def in COILS_TIMEZONES:
        if code == tz_def['code']:
            tz = gettz(tz_def['code'])
            break
        else:
            tz = gettz('UTC')

    is_dst = 0
    if tz.dst(utctime).seconds > 0:
        is_dst = 1
    return {'abbreviation': tz_def['abbreviation'], 'description': tz_def['description'], 'entityName': 'timeZone', 
       'isCurrentlyDST': is_dst, 
       'offsetFromGMT': as_integer((86400 - tz.utcoffset(utctime).seconds) * -1), 
       'serverDateTime': utctime.astimezone(tz)}