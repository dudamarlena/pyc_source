# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/actions/read/status.py
# Compiled at: 2020-03-21 10:42:53
# Size of source mod 2**32: 890 bytes
from __future__ import print_function
from tt.dataaccess.utils import get_data_store
from tt.dateutils.dateutils import *
from tt.actions.utils.utils import ensure_working

def action_status(colorizer):
    data = get_data_store().load()
    ensure_working(data)
    current = data['work'][(-1)]
    start_time = parse_isotime(current['start'])
    diff = timegap(start_time, datetime.utcnow())
    isotime_local = isotime_utc_to_local(current['start'])
    start_h_m = isotime_local.strftime('%H:%M')
    now_time_str = datetime.now().strftime('%H:%M')
    print('You have been working on {0} for {1}, since {2}; It is now {3}.'.format(colorizer.green(current['name']), colorizer.yellow(diff), colorizer.yellow(start_h_m), colorizer.yellow(now_time_str)))
    if 'notes' in current:
        for note in current['notes']:
            print('  * ', note)