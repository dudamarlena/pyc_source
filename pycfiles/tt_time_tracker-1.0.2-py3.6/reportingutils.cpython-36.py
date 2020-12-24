# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/actions/utils/reportingutils.py
# Compiled at: 2020-03-21 10:42:53
# Size of source mod 2**32: 563 bytes
from tt.dateutils.dateutils import *

def get_notes_from_workitem(item):
    notes = ''
    if 'notes' in item:
        for note in item['notes']:
            notes += note + ' ; '

    return notes


def extract_day_custom_formatter(datetime_local_tz, format_string):
    local_dt = isotime_utc_to_local(datetime_local_tz)
    return local_dt.strftime(format_string)


def extract_day(datetime_local_tz):
    return extract_day_custom_formatter(datetime_local_tz, '%Y-%m-%d')


def remove_seconds(timedelta):
    return ':'.join(str(timedelta).split(':')[:2])