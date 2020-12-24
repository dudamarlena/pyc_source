# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/actions/write/note.py
# Compiled at: 2020-03-21 10:42:53
# Size of source mod 2**32: 453 bytes
from tt.dataaccess.utils import get_data_store
from tt.actions.utils.utils import ensure_working

def action_note(colorizer, content):
    data = get_data_store().load()
    ensure_working(data)
    current = data['work'][(-1)]
    if 'notes' not in current:
        current['notes'] = [
         content]
    else:
        current['notes'].append(content)
    get_data_store().dump(data)
    print('Yep, noted to ' + colorizer.yellow(current['name']) + '.')