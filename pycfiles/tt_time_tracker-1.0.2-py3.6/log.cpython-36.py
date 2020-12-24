# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/actions/read/log.py
# Compiled at: 2020-03-21 10:42:53
# Size of source mod 2**32: 1606 bytes
from __future__ import print_function
from collections import defaultdict
from tt.dataaccess.utils import get_data_store
from tt.dateutils.dateutils import *
from tt.colors.colors import *

def action_log(period):
    data = get_data_store().load()
    work = data['work']
    log = defaultdict(lambda : {'delta': timedelta()})
    current = None
    for item in work:
        start_time = parse_isotime(item['start'])
        if 'end' in item:
            log[item['name']]['delta'] += parse_isotime(item['end']) - start_time
        else:
            log[item['name']]['delta'] += datetime.utcnow() - start_time
            current = item['name']

    name_col_len = 0
    for name, item in log.items():
        name_col_len = max(name_col_len, len(strip_color(name)))
        secs = item['delta'].total_seconds()
        tmsg = []
        if secs > 3600:
            hours = int(secs // 3600)
            secs -= hours * 3600
            tmsg.append(str(hours) + ' hour' + ('s' if hours > 1 else ''))
        if secs > 60:
            mins = int(secs // 60)
            secs -= mins * 60
            tmsg.append(str(mins) + ' minute' + ('s' if mins > 1 else ''))
        if secs:
            tmsg.append(str(secs) + ' second' + ('s' if secs > 1 else ''))
        print(tmsg)
        log[name]['tmsg'] = ', '.join(tmsg)[::-1].replace(',', '& ', 1)[::-1]

    for name, item in sorted((log.items()), key=(lambda x: x[0]), reverse=True):
        print((ljust_with_color(name, name_col_len)), ' :: ', (item['tmsg']), end=(' <- working\n' if current == name else '\n'))