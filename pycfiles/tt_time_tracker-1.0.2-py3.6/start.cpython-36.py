# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/actions/write/start.py
# Compiled at: 2020-03-21 10:42:53
# Size of source mod 2**32: 724 bytes
from tt.exceptz.exceptz import AlreadyOn
from tt.dataaccess.utils import get_data_store
from tt.dateutils.dateutils import formatted_str_for_isotime_str

def action_start(colorizer, name, time):
    data = get_data_store().load()
    work = data['work']
    if work:
        if 'end' not in work[(-1)]:
            raise AlreadyOn('You are already working on %s. Stop it or use a different sheet.' % (
             colorizer.yellow(work[(-1)]['name']),))
    entry = {'name':name,  'start':time}
    work.append(entry)
    get_data_store().dump(data)
    print('Started working on ' + colorizer.green(name) + ' at ' + colorizer.yellow(formatted_str_for_isotime_str(time, '%H:%M')) + '.')