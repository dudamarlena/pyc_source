# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/actions/read/csv.py
# Compiled at: 2020-03-21 10:42:53
# Size of source mod 2**32: 1259 bytes
from __future__ import print_function
from tt.dataaccess.utils import get_data_store
from tt.dateutils.dateutils import *
from tt.actions.utils import reportingutils

def action_csv():
    sep = '|'
    data = get_data_store().load()
    work = data['work']
    for item in work:
        if 'end' in item:
            notes = reportingutils.get_notes_from_workitem(item)
            duration = parse_isotime(item['end']) - parse_isotime(item['start'])
            duration_total = reportingutils.remove_seconds(duration)
            date = reportingutils.extract_day(item['start'])
            name = item['name']
            start = format_csv_time(item['start'])
            end = format_csv_time(item['end'])
            tags = ''
            if 'tags' in item:
                tags = item['tags']
            print_elements(date, name, start, end, duration_total, notes, tags, sep)


def print_elements(date, name, start, end, total_duration, notes, tags, sep):
    print(date, sep, start, sep, end, sep, '', sep, notes, sep, name)


def format_csv_time(somedatetime):
    local_dt = isotime_utc_to_local(somedatetime)
    return local_dt.strftime('%H:%M')